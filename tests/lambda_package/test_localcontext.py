import mock
import unittest

from my_lambda_package.localcontext import LocalContext


class TestLocalContext(unittest.TestCase):

    @mock.patch('my_lambda_package.localcontext.Utility')
    def testInvokedFunctionArn(self, mock_utility):
        """Tests the output of LocalContext.invoked_function_arn."""
        mock_utility.aws_account_id.return_value = 123456654321
        obj = LocalContext()
        self.assertEqual(obj.invoked_function_arn,
            'arn:aws:lambda:us-east-1:123456654321:function:func-name')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
