from utils.helpers import Helpers

class LocalContext(object):
    """A class to simulate the Lambda context locally."""

    @property
    def invoked_function_arn(self):
        """Simulate the Lambda ARN that comes into the context object. """
        return 'arn:aws:lambda:us-east-1:{0}:function:func-name'.format(
            Helpers.aws_account_id())
