
class MockLambdaContext(object):
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


class MockLambdaEvents(object):
    cloudformation_creation = {
        "StackId": "arn:aws:cloudformation:us-west-2:EXAMPLE/stack-name/guid",
        "ResponseURL": "http://pre-signed-S3-url-for-response",
        "ResourceProperties": {
            "StackName": "stack-name",
            "List": [
                "1",
                "2",
                "3"
            ]
        },
        "RequestType": "Create",
        "ResourceType": "Custom::TestResource",
        "RequestId": "unique id for this create request",
        "LogicalResourceId": "MyTestResource"
    }

    cloudformation_update = {
        "StackId": "arn:aws:cloudformation:us-west-2:EXAMPLE/stack-name/guid",
        "ResponseURL": "http://pre-signed-S3-url-for-response",
        "ResourceProperties": {
            "StackName": "stack-name",
            "List": [
                "1",
                "2",
                "3"
            ]
        },
        "RequestType": "Update",
        "ResourceType": "Custom::TestResource",
        "RequestId": "unique id for this create request",
        "LogicalResourceId": "MyTestResource"
    }

    cloudformation_deletion = {
        "StackId": "arn:aws:cloudformation:us-west-2:EXAMPLE/stack-name/guid",
        "ResponseURL": "http://pre-signed-S3-url-for-response",
        "ResourceProperties": {
            "StackName": "stack-name",
            "List": [
                "1",
                "2",
                "3"
            ]
        },
        "RequestType": "Delete",
        "ResourceType": "Custom::TestResource",
        "RequestId": "unique id for this create request",
        "LogicalResourceId": "MyTestResource"
    }
