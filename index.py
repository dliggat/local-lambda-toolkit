import logging
import os
import yaml

from my_lambda_package.utility import Utility


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _load_config(filename='config.yaml'):
    """Loads the configuration file."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)), 'r') as f:
        config = yaml.load(f)
        logger.info('Loaded config: {0}'.format(config))
    return config


def handler(event, context):
    """Entry point for the Lambda function."""
    config = _load_config()

    # Used to differentiate local vs Lambda.
    if bool(os.getenv('STUB')):
        logger.debug('$STUB set; likely running in development')
    else:
        logger.debug('No $STUB set; likely running in Lambda')

    logger.info('This is being invoked from AWS account: {0}'.format(
        Utility.aws_account_id()))


if __name__ == '__main__':
    from my_lambda_package.localcontext import LocalContext
    handler(None, LocalContext())
