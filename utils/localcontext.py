import uuid

from utils.helpers import Helpers

class LocalContext(object):
    """A class to simulate the Lambda context locally."""

    @property
    def invoked_function_arn(self):
        """Simulate the Lambda ARN that comes into the context object. """
        return 'arn:aws:lambda:us-east-1:{0}:function:func-name'.format(
            Helpers.aws_account_id())

    @property
    def aws_request_id(self):
        """Simulate the request guid that comes into the context object."""
        return str(uuid.uuid1())

    def __str__(self):
      return str((self.invoked_function_arn, self.aws_request_id))
