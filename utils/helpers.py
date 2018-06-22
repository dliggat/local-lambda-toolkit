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
