import os
from awslambda.utils.helpers import Helpers


class CFNMacro(object):
    RESULT_SUCCESS = "success"
    RESULT_FAILURE = "failure"

    def __init__(self, event, context):
        if None in (event, context):
            message = 'Lambda event or context cannot be None'
            self.logger.error(message)
            raise ValueError(message)

        self.event = event
        self.context = context

        self.params = self.event['params']
        self.region = self.event['region']
        self.account_id = self.event['accountId']
        self.fragment = self.event['fragment']
        self.transform_id = self.event['transformId']
        self.template_parameter_values = self.event['templateParameterValues']
        self.request_id = self.event['requestId']

        self.logger = Helpers.setup_logging(context.aws_request_id)
        if bool(os.getenv('IS_LOCAL')):
            self.logger.debug('$IS_LOCAL set; likely running in development')
            self.is_local = True
        else:
            self.logger.debug('No $IS_LOCAL set; likely running in Lambda')
            self.is_local = False

        return

    def success(self, fragment):
        return {
            "requestId": self.request_id,
            "status": self.RESULT_SUCCESS,
            "fragment": fragment
        }

    def failure(self):
        return {
            "requestId": self.request_id,
            "status": self.RESULT_FAILURE
        }
