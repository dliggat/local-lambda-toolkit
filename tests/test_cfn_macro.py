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
        request_id = 'fad23d4b-277d-4977-955b-36d2ba887577'
        test_event = {
            "transformId": "123456789012::TestMacro",
            "templateParameterValues": {
                "SomeKey": "SomeValue"
            },
            "fragment": {},
            "region": "ca-central-1",
            "params": {
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

    def test_required_parameters_missing(self):
        request_id = 'fad23d4b-277d-4977-955b-36d2ba887577'
        test_event = {
            "transformId": "123456789012::TestMacro",
            "templateParameterValues": {
                "SomeKey": "SomeValue"
            },
            "fragment": {},
            "region": "ca-central-1",
            "params": {
            },
            "requestId": request_id,
            "accountId": "123456789012"
        }
        test_context = MagicMock()

        class MyTestMacro(CFNMacro):
            required_params = {'Required1', 'Required2'}

        with self.assertRaises(KeyError):
            MyTestMacro(test_event, test_context)

    def test_required_parameters(self):
        request_id = 'fad23d4b-277d-4977-955b-36d2ba887577'
        test_event = {
            "transformId": "123456789012::TestMacro",
            "templateParameterValues": {
                "SomeKey": "SomeValue"
            },
            "fragment": {},
            "region": "ca-central-1",
            "params": {
                "Required1": "SomeValue",
                "Required2": "SomeOtherValue"
            },
            "requestId": request_id,
            "accountId": "123456789012"
        }
        test_context = MagicMock()

        class MyTestMacro(CFNMacro):
            required_params = {'Required1', 'Required2'}

        cfn_macro = MyTestMacro(test_event, test_context)

        result = cfn_macro.success({'test_fragment': 'test_fragment_value'})

        self.assertEquals(result, {'fragment': {'test_fragment': 'test_fragment_value'},
                                   'requestId': 'fad23d4b-277d-4977-955b-36d2ba887577',
                                   'status': 'success'})

    def test_unknown_parameters(self):
        request_id = 'fad23d4b-277d-4977-955b-36d2ba887577'
        test_event = {
            "transformId": "123456789012::TestMacro",
            "templateParameterValues": {
                "SomeKey": "SomeValue"
            },
            "fragment": {},
            "region": "ca-central-1",
            "params": {
                "Required1": "SomeValue",
                "Required2": "SomeOtherValue",
                "UnknownParam": "SomeValue"
            },
            "requestId": request_id,
            "accountId": "123456789012"
        }
        test_context = MagicMock()

        class MyTestMacro(CFNMacro):
            required_params = {'Required1', 'Required2'}

        with self.assertRaises(KeyError):
            MyTestMacro(test_event, test_context)

    def test_optional_parameters_missing(self):
        request_id = 'fad23d4b-277d-4977-955b-36d2ba887577'
        test_event = {
            "transformId": "123456789012::TestMacro",
            "templateParameterValues": {
                "SomeKey": "SomeValue"
            },
            "fragment": {},
            "region": "ca-central-1",
            "params": {
                "Required1": "SomeValue",
                "Required2": "SomeOtherValue"
            },
            "requestId": request_id,
            "accountId": "123456789012"
        }
        test_context = MagicMock()

        class MyTestMacro(CFNMacro):
            required_params = {'Required1', 'Required2'}
            optional_params = {'Optional1'}

        cfn_macro = MyTestMacro(test_event, test_context)

        result = cfn_macro.success({'test_fragment': 'test_fragment_value'})

        self.assertEquals(result, {'fragment': {'test_fragment': 'test_fragment_value'},
                                   'requestId': 'fad23d4b-277d-4977-955b-36d2ba887577',
                                   'status': 'success'})

    def test_optional_parameters_included(self):
        request_id = 'fad23d4b-277d-4977-955b-36d2ba887577'
        test_event = {
            "transformId": "123456789012::TestMacro",
            "templateParameterValues": {
                "SomeKey": "SomeValue"
            },
            "fragment": {},
            "region": "ca-central-1",
            "params": {
                "Required1": "SomeValue",
                "Required2": "SomeOtherValue",
                "Optional1": "SomeValue"
            },
            "requestId": request_id,
            "accountId": "123456789012"
        }
        test_context = MagicMock()

        class MyTestMacro(CFNMacro):
            required_params = {'Required1', 'Required2'}
            optional_params = {'Optional1'}

        cfn_macro = MyTestMacro(test_event, test_context)

        result = cfn_macro.success({'test_fragment': 'test_fragment_value'})
        self.assertEquals(cfn_macro.optional_params.union(cfn_macro.required_params), test_event.get('params').keys())

        self.assertEquals(result, {'fragment': {'test_fragment': 'test_fragment_value'},
                                   'requestId': 'fad23d4b-277d-4977-955b-36d2ba887577',
                                   'status': 'success'})
