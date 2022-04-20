# from campaignresourcecentre.scheduler.runapscheduler import resend_verification_emails, start, delete_old_job_executions
# from campaignresourcecentre.paragon_users.models import VerificationEmail, PasswordResetEmail
# from django.test import TestCase
# import unittest
#
# class TestScheduler(TestCase):
#
#     def test_verification_none(self):
#         with self.assertLogs("campaignresourcecentre.scheduler.runapscheduler","INFO") as cm:
#
#             resend_verification_emails()
#
#             self.assertIn(
#                 "INFO:campaignresourcecentre.scheduler.runapscheduler:ran 'resend_verification_emails' : no emails",
#                 cm.output
#                 )
#
#
#     def test_verification(self):
#
#         VerificationEmail.objects.create(
#             user_token="x",
#             email="email@email.com",
#             url="www.nhs.net",
#             first_name="test")
#
#         with self.assertLogs("campaignresourcecentre.scheduler.runapscheduler","INFO") as cm:
#
#             resend_verification_emails()
#
#             self.assertIn("INFO:campaignresourcecentre.scheduler.runapscheduler:ran 'resend_verification_emails' : 1 emails",
#                 cm.output
#                 )
#
#         VerificationEmail.objects.all().delete()
