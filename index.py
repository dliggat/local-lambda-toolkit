import logging
import os
import yaml

from utils.helpers import Helpers
from utils.config import configuration


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



def handler(event, context):
    """Entry point for the Lambda function."""
    config = configuration()

    # Used to differentiate local vs Lambda.
    if bool(os.getenv('STUB')):
        logger.debug('$STUB set; likely running in development')
    else:
        logger.debug('No $STUB set; likely running in Lambda')

    logger.info('This is being invoked from AWS account: {0}'.format(
        Helpers.aws_account_id()))


if __name__ == '__main__':
    from utils.localcontext import LocalContext
    handler(None, LocalContext())
