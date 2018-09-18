import mock
import unittest
from mock import patch, Mock, MagicMock
import boto3
from botocore.stub import Stubber

import sys
sys.path.append("..")
import awslambda


class TestHandler(unittest.TestCase):
    def test_handler(self):
        """
        Test the handler operates as expected.
        """
        pass
        # test_event = MagicMock()
        # test_context = MagicMock()

        # aws_account_id.return_value = '1234567890'
        # index.handler(test_event, test_context)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
