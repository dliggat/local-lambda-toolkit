import mock
import unittest

from utils.helpers import Helpers


class TestHelpers(unittest.TestCase):

    @mock.patch('boto3.client')
    def testAwsAccountId(self, patched_boto):
        """Tests the output of Helpers.aws_account_id."""
        patched_boto.return_value.get_caller_identity.return_value = {
            'Arn': 'arn:aws:iam::localcontext:user/dliggat' }

        # Query for the account id; first to generate, second for a cache hit.
        self.assertEqual(Helpers.aws_account_id(), 'localcontext')
        self.assertEqual(Helpers.aws_account_id(), 'localcontext')

        # We should only ever the boto code once; the account value should
        # be memoized in the class after the initial invocation.
        patched_boto.assert_called_once_with('sts')
        patched_boto.return_value.get_caller_identity.assert_called_once_with()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
