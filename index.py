import logging
import os
import yaml
import pprint
import signal
import json
try:
    from urllib2 import build_opener, HTTPHandler, Request
except ImportError:
    from urllib.request import build_opener, HTTPHandler, Request

from utils.helpers import Helpers
from utils.config import configuration


def handler(event, context):
    """Entry point for the Lambda function."""

    logger = Helpers.setup_logging(context.aws_request_id)
    config = configuration()

    # Setup alarm for remaining runtime minus a second
    signal.alarm(int(context.get_remaining_time_in_millis() / 1000) - 1)

    if bool(os.getenv('IS_LOCAL')):
        logger.debug('$IS_LOCAL set; likely running in development')
    else:
        logger.debug('No $IS_LOCAL set; likely running in Lambda')

    if None in (event, context):
        message = 'Lambda event or context cannot be None'
        logger.error(message)
        return {'Success': False, 'Message': message}

    try:
        logger.info('REQUEST RECEIVED:\n %s', event)
        logger.info('REQUEST RECEIVED:\n %s', context)
        if 'RequestType' not in event:
            raise KeyError('CustomResources require a "RequestType"')

        if event['RequestType'] == 'Create':
            logger.info('CREATE!')
            send_response(event, context, "SUCCESS",
                          {"Message": "Resource creation successful!"},
                          logger)
        elif event['RequestType'] == 'Update':
            logger.info('UPDATE!')
            send_response(event, context, "SUCCESS",
                          {"Message": "Resource update successful!"},
                          logger)
        elif event['RequestType'] == 'Delete':
            logger.info('DELETE!')
            send_response(event, context, "SUCCESS",
                          {"Message": "Resource deletion successful!"},
                          logger)
        else:
            logger.info('FAILED!')
            send_response(event, context, "FAILED",
                          {"Message": "Unexpected event received from CloudFormation"},
                          logger)
    except:
        logger.info('FAILED!')
        send_response(event, context, "FAILED",
                      {"Message": "Exception during processing"},
                      logger)

    return {'Success': True}


def send_response(event, context, response_status, response_data, logger):
    '''Send a resource manipulation status response to CloudFormation'''

    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": response_data
    })

    logger.info('ResponseURL: %s', event['ResponseURL'])
    logger.info('ResponseBody: %s', response_body)

    opener = build_opener(HTTPHandler)
    request = Request(event['ResponseURL'], data=response_body.encode("utf-8"))
    request.add_header('Content-Type', '')
    request.add_header('Content-Length', len(response_body))
    request.get_method = lambda: 'PUT'
    response = opener.open(request)
    logger.info("Status code: %s", response.getcode())
    logger.info("Status message: %s", response.msg)


if __name__ == '__main__':
    from utils.localcontext import LocalContext
    handler(None, LocalContext())
