import logging
import os
import yaml
import pprint

from utils.helpers import Helpers
from utils.config import configuration


def setup_logging(request_id, level=logging.INFO):
    """Creates the logging formatter.

    Args:
        request_id: (str) The id of the execution context (i.e. the Lambda execution ID).
        level: logging level to use.
    """
    logger = logging.getLogger()
    logger.info('Setting up logging')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(levelname)s] %(asctime)s {0} [%(module)s:%(lineno)d]: %(message)s'.format(request_id))
    console_handler.setFormatter(formatter)

    logger.handlers = []  # Get rid of any default handlers (Lambda apparently adds one).
    logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger


def handler(event, context):
    """Entry point for the Lambda function."""
    logger = setup_logging(context.aws_request_id)
    config = configuration()

    pprint.pprint(config)

    # Used to differentiate local vs Lambda.
    if bool(os.getenv('IS_LOCAL')):
        logger.debug('$IS_LOCAL set; likely running in development')
    else:
        logger.debug('No $IS_LOCAL set; likely running in Lambda')

    logger.info('This is being invoked from AWS account: {0}'.format(
        Helpers.aws_account_id()))

    return {'Success': True}


if __name__ == '__main__':
    from utils.localcontext import LocalContext
    handler(None, LocalContext())
