import logging

from campaignresourcecentre.paragon.client import Client
from campaignresourcecentre.paragon.exceptions import ParagonClientError

logger = logging.getLogger(__name__)


def get_current_num_users(previous_num_users=0):
    """
    Find current number of Paragon users
    Paragon doesn't provide a number of users API so we have to
    make use of the search API to find this
    This function uses the following algorithm:
    1. Do Paragon search with offset set to previous_num_users and limit set to 100
    2. If reponse is a 400 error, previous_num_users is potentially greater than
        number of users, so reduce number by 50 and go to step 1
    3. If number of users returned is less than 100, we've found the end of the users
        list, add number of users returned to previous_num_users and return
    4. If number of users returned equals 100, there are potentially more users, add
        100 to the previous_num_users and go to step 1
    """

    logger.info(f"Previous number of users: {previous_num_users}")

    paragon_client = Client()

    try:
        response = paragon_client.search_users(
            offset=previous_num_users,
            limit=100,
            string="",
        )
        num_users_returned = len(response["content"])
        logger.info(f"Number of users returned: {num_users_returned}")

        new_num_users = previous_num_users + num_users_returned - 1
        logger.info(f"New number of users {new_num_users}")

        if num_users_returned < 100:
            return new_num_users
        else:
            return get_current_num_users(new_num_users)

    except ParagonClientError as PCE:
        if PCE.args[0] != "No records match the criteria":
            # Paragon error, return previous number of users
            logger.info("Error fetching users from Paragon")
            return previous_num_users

        # previous_num_users is potentially greater than the current
        # number of users causing Paragon to return
        # "No records match the criteria"
        # reduce previous_num_users and retry
        logger.info("previous number of users greater than Paragon number of users")
        return get_current_num_users(previous_num_users - 50)
