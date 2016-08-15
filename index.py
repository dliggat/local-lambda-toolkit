import logging
import os

from my_lambda_package.utility import Utility


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    """Entry point for the Lambda function."""
    logger.info('This is being invoked from AWS account: {0}'.format(
        Utility.aws_account_id()))


if __name__ == '__main__':
    from my_lambda_package.localcontext import LocalContext
    handler(None, LocalContext())
