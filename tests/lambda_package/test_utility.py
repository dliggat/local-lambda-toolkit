import mock
import unittest

from my_lambda_package.utility import Utility


class TestUtility(unittest.TestCase):

    @mock.patch('boto3.client')
    def testAwsAccountId(self, patched_boto):
        """Tests the output of Utility.aws_account_id."""
        patched_boto.return_value.describe_security_groups.return_value = {
          'SecurityGroups': [{ 'OwnerId': '123456654321' }]
        }

        # Query for the account id; first to generate, second for a cache hit.
        self.assertEqual(Utility.aws_account_id(), 123456654321)
        self.assertEqual(Utility.aws_account_id(), 123456654321)

        # We should only ever the boto code once; the account value should
        # be memoized in the class after the initial invocation.
        patched_boto.assert_called_once_with('ec2')
        patched_boto.return_value.describe_security_groups.assert_called_once_with(
            GroupNames=['default'])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
