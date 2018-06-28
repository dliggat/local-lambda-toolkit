import mock
import unittest
from mock import patch, Mock, MagicMock
import boto3
from botocore.stub import Stubber

import sys
sys.path.append("..")
import index


class TestHandler(unittest.TestCase):
    @mock.patch('index.Helpers.aws_account_id')
    def test_handler(self, aws_account_id):
        """
        Test the handler operates as expected.
        """
        # test_event = MagicMock()
        # test_context = MagicMock()

        # aws_account_id.return_value = '1234567890'
        # index.handler(test_event, test_context)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
