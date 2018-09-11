import logging
import mock
import unittest
from mock import patch, Mock, MagicMock
import boto3
from botocore.stub import Stubber

import sys
sys.path.append("..")
import awslambda

from .lambda_helpers import MockLambdaContext, MockLambdaEvents
from awslambda.utils.cfn_macro import CFNMacro


class TestCFNMacroHandler(unittest.TestCase):
    def test_handler(self):
        """
        Test the handler operates as expected.
        """
        request_id = 'fad23d4b-277d-4977-955b-36d2ba887577'
        test_event = {
            "transformId": "123456789012::TestMacro",
            "templateParameterValues": {
                "SomeKey": "SomeValue"
            },
            "fragment": {},
            "region": "ca-central-1",
            "params": {
                "SomeOtherKey": ["SomeOtherValue"]
            },
            "requestId": request_id,
            "accountId": "123456789012"
        }
        test_context = MagicMock()

        cfn_macro = CFNMacro(test_event, test_context)
        result = cfn_macro.success({'test_fragment': 'test_fragment_value'})
        self.assertEquals(result, {'fragment': {'test_fragment': 'test_fragment_value'},
                                   'requestId': 'fad23d4b-277d-4977-955b-36d2ba887577',
                                   'status': 'success'})
