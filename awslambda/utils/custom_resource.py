import os
import signal
import json
try:
    from urllib2 import build_opener, HTTPHandler, Request
except ImportError:
    from urllib.request import build_opener, HTTPHandler, Request

from awslambda.utils.helpers import Helpers
from awslambda.utils.config import configuration


class CFNCustomResource(object):
    RESULT_SUCCESS = "SUCCESS"
    RESULT_FAILURE = "FAILURE"

    REQUEST_TYPE_CREATE = "Create"
    REQUEST_TYPE_DELETE = "Delete"
    REQUEST_TYPE_UPDATE = "Update"

    def __init__(self, event, context):
        if None in (event, context):
            message = 'Lambda event or context cannot be None'
            self.logger.error(message)
            raise ValueError(message)

        self.event = event
        self.context = context

        self.logger = Helpers.setup_logging(context.aws_request_id)
        if bool(os.getenv('IS_LOCAL')):
            self.logger.debug('$IS_LOCAL set; likely running in development')
            self.is_local = True
        else:
            self.logger.debug('No $IS_LOCAL set; likely running in Lambda')
            self.is_local = False

        self.request_type = event.get('RequestType')
        if not self.request_type:
            raise ValueError('CustomResources require a "RequestType"')
        if self.request_type not in (self.REQUEST_TYPE_CREATE, self.REQUEST_TYPE_DELETE, self.REQUEST_TYPE_UPDATE):
            raise ValueError('Unknown Request Type: {}'.format(self.request_type))

        self.request_functions = {
            self.REQUEST_TYPE_CREATE: self.create,
            self.REQUEST_TYPE_DELETE: self.delete,
            self.REQUEST_TYPE_UPDATE: self.update,
        }

        return

    def handler(self):
        self.config = configuration()

        # Setup alarm for remaining runtime minus a second
        signal.alarm(int(self.context.get_remaining_time_in_millis() / 1000) - 1)

        try:
            self.logger.info('REQUEST RECEIVED:\n %s', self.event)
            self.logger.info('REQUEST RECEIVED:\n %s', self.context)
            self.logger.info('REQUEST TYPE: %s', self.request_type)

            # execute request
            return self.request_functions[self.request_type]()
        except Exception as e:
            self.logger.error('FAILED!')
            self.logger.exception(e)
            return self.return_failure("Exception during processing.")

    def create(self):
        return self.return_success("Resource creation successful!")

    def update(self):
        return self.return_success("Resource update successful!")

    def delete(self):
        return self.return_success("Resource deletion successful!")

    def return_success(self, message):
        return self._send_response(self.RESULT_SUCCESS, {"Message": message})

    def return_failure(self, message):
        return self._send_response(self.RESULT_FAILURE, {"Message": message})

    def _send_response(self, response_status, response_data):
        '''Send a resource manipulation status response to CloudFormation'''

        response_body = json.dumps({
            "Status": response_status,
            "Reason": "See the details in CloudWatch Log Stream: " + self.context.log_stream_name,
            "PhysicalResourceId": self.context.log_stream_name,
            "StackId": self.event['StackId'],
            "RequestId": self.event['RequestId'],
            "LogicalResourceId": self.event['LogicalResourceId'],
            "Data": response_data
        })

        self.logger.info('ResponseURL: %s', self.event['ResponseURL'])
        self.logger.info('ResponseBody: %s', response_body)

        opener = build_opener(HTTPHandler)
        request = Request(self.event['ResponseURL'], data=response_body.encode("utf-8"))
        request.add_header('Content-Type', '')
        request.add_header('Content-Length', len(response_body))
        request.get_method = lambda: 'PUT'
        response = opener.open(request)
        self.logger.info("Status code: %s", response.getcode())
        self.logger.info("Status message: %s", response.msg)

        return {'Success': False} if response_status == self.RESPONSE_FAILURE else {'Success': True}
