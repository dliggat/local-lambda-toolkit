import logging
import boto3


class Helpers(object):
    """A container class for convenience functions."""

    _aws_account_id = None

    @classmethod
    def aws_account_id(cls):
        """Query for the current account ID by inspecting the caller identity."""
        if cls._aws_account_id is None:
            caller_data = boto3.client('sts').get_caller_identity()
            cls._aws_account_id = caller_data['Arn'].split(':')[4]
        return cls._aws_account_id

    @staticmethod
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
