import logging
import mock
import unittest
from mock import patch, Mock, MagicMock
import boto3
from botocore.stub import Stubber

import sys
sys.path.append("..")
import index


class SampleContext(object):
    aws_request_id = 'a3de505e-f16b-42f4-b3e6-bcd2e4a73903'
    log_stream_name = '2015/10/26/[$LATEST]c71058d852474b9895a0f221f73402ad'
    invoked_function_arn = 'arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F'
    client_context = None
    log_group_name = '/aws/lambda/ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F'
    function_name = 'ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F'
    function_version = '$LATEST'
    identity = {}
    memory_limit_in_mb = 128

    def get_remaining_time_in_millis(self):
        v = int(10000)
        print(type(v))
        return v


class TestHandler(unittest.TestCase):
    @patch('index.send_response')
    def test_handler(self, mock_send_response):
        """
        Test the handler operates as expected.
        """
        test_event = {
           "RequestType": "Create",
           "ResponseURL": "http://pre-signed-S3-url-for-response",
           "StackId": "arn:aws:cloudformation:us-west-2:localcontext:stack/stack-name/guid",
           "RequestId": "unique id for this create request",
           "ResourceType": "Custom::TestResource",
           "LogicalResourceId": "MyTestResource",
           "ResourceProperties": {
              "Name": "Value",
              "List": ["1", "2", "3"]
           }
        }

        test_context = SampleContext()

        retval = index.handler(test_event, test_context)
        mock_send_response.assert_called_with(test_event, test_context, 'SUCCESS',
                                              {'Message': 'Resource creation successful!'},
                                              logging.getLogger())

        self.assertEquals(retval, {'Success': True})

        return


def main():
    unittest.main()


if __name__ == '__main__':
    main()
