import mock
import unittest

import sys
sys.path.append("..")

from awslambda.utils.localcontext import LocalContext


class TestLocalContext(unittest.TestCase):

    def testInvokedFunctionArn(self):
        """Tests the output of LocalContext.invoked_function_arn."""
        obj = LocalContext()
        self.assertEqual(obj.invoked_function_arn,
            'arn:aws:lambda:us-east-1:localcontext:function:func-name')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
