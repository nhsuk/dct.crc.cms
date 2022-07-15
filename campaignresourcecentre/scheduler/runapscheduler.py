import logging

from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from campaignresourcecentre.paragon_users.helpers.verification import send_verification
from campaignresourcecentre.paragon_users.models import VerificationEmail

logger = logging.getLogger(__name__)


def resend_verification_emails():
    emails = VerificationEmail.objects.all()
    count = len(emails)
    if len(emails) > 0:
        for email in emails:
            send_verification(
                email.user_token, email.url, email.email, email.first_name
            )
        emails.delete()
        logger.info("ran 'resend_verification_emails' : " + str(count) + " emails")
    else:
        logger.info("ran 'resend_verification_emails' : no emails")


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
    logger.info("ran 'delete_old_job_executions'")


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        resend_verification_emails,
        trigger=CronTrigger(minute="*/30"),  # Every 30 minutes
        id="resend_verification_emails",  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'resend_verification_emails'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added weekly job: 'delete_old_job_executions'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
