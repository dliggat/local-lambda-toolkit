import mock
import unittest

from utils.localcontext import LocalContext


class TestLocalContext(unittest.TestCase):

    @mock.patch('utils.localcontext.Helpers')
    def testInvokedFunctionArn(self, mock_helpers):
        """Tests the output of LocalContext.invoked_function_arn."""
        mock_helpers.aws_account_id.return_value = 123456654321
        obj = LocalContext()
        self.assertEqual(obj.invoked_function_arn,
            'arn:aws:lambda:us-east-1:123456654321:function:func-name')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
