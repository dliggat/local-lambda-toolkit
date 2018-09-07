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


@patch('awslambda.custom_resource.CFNCustomResource._send_response')
class TestCustomResourceHandler(unittest.TestCase):
    def test_handler_create(self, mock_send_response):
        """
        Test the custom resource handler creation operates as expected.
        """

        test_context = MockLambdaContext()
        test_event = MockLambdaEvents.cloudformation_creation

        custom_resource = awslambda.custom_resource.CFNCustomResource(test_event, test_context)
        custom_resource.handler()
        mock_send_response.assert_called_with('SUCCESS', {'Message': 'Resource creation successful!'})

        return

    def test_handler_update(self, mock_send_response):
        """
        Test the custom resource handler update operates as expected.
        """

        test_context = MockLambdaContext()
        test_event = MockLambdaEvents.cloudformation_update

        custom_resource = awslambda.custom_resource.CFNCustomResource(test_event, test_context)
        custom_resource.handler()
        mock_send_response.assert_called_with('SUCCESS', {'Message': 'Resource update successful!'})

        return

    def test_handler_delete(self, mock_send_response):
        """
        Test the custom resource handler deletion operates as expected.
        """

        test_context = MockLambdaContext()
        test_event = MockLambdaEvents.cloudformation_deletion

        custom_resource = awslambda.custom_resource.CFNCustomResource(test_event, test_context)
        custom_resource.handler()
        mock_send_response.assert_called_with('SUCCESS', {'Message': 'Resource deletion successful!'})

        return
