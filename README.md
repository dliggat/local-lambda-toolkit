# New Project

Clone this repo as a starting point for Lambda development.

---

# Local Lambda Toolkit
A set of conventions for local AWS Lambda software development.

## Directory Structure

```bash
.
├── Makefile                           # Definition of `make` targets.
├── builds                             # Builds directory.
│   ├── deploy-2016-08-15_16-50.zip
│   └── deploy-2016-08-15_16-54.zip
├── cloudformation                     # CloudFormation template and parameters.
│   └── parameters.json
│   └── template.yaml
├── config.yaml                        # Static config and ParameterStore lookups.
├── index.py                           # Entry point for the Lambda function.
├── requirements                       # External dependencies.
│   ├── common.txt
│   ├── dev.txt
│   └── lambda.txt
└── tests                              # Unit tests for the package.
    ├── __init__.py
    └── utils
        ├── __init__.py
        ├── test_localcontext.py
        └── test_helpers.py
├── utils                              # Python package `utils`.
│   ├── __init__.py
│   ├── config.py
│   ├── localcontext.py
│   ├── helpers.py
```

## 1. Initial AWS Setup

Creates a CloudFormation stack with the Lambda function, an execution role, and an optional CloudWatch event to run on a recurring basis.

### A) Stack Naming and Parameters

Edit `cloudformation/parameters.json`, and supply appropriate parameters.

In particular, Select appropriate values for `ProjectName` and `EnvironmentName` in `cloudformation/parameters.json`.

**Important: The resulting CloudFormation stack will be named `${ProjectName}-${EnvironmentName}-stack`, and a stack name of this form will be presumed for future CloudFormation operations.**

### B) Permissioning

Edit `cloudformation/template.yaml` and ensure that the Lambda function is appropriately permissioned via the policies attached to the `LambdaFunctionExecutionRole`.

### C) Optional: Set Values in Parameter Store

If this Lambda function should have access to values in Parameter Store, set these on the CLI (or console); e.g.:

```bash
 aws ssm put-parameter --name "common.preferred-salutation" \
 --value "Hello" \
 --type String

 aws ssm put-parameter --name "my-project.development.dynamo_table" \
 --value "stack-ResultTable-16KAA4B56PNEP" \
 --type String
```

Ensure that the `AllowParameterAccess` policy in `cloudformation/template.yaml` is uncommented and updated to reflect an appropriate parameter namespace(s); e.g.

```yaml
# cloudformation/template.yaml
# ...
  - PolicyName: "ParameterStore"
    PolicyDocument:
      Version: "2012-10-17"
      Id: "AllowParameterAccess"
      Statement:
        - Sid: "AllowUnencryptedParameters"
          Effect: "Allow"
          Action: "ssm:GetParameter"
          Resource:
            - "Fn::Sub": "arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/my-namespace.*"
            - "Fn::Sub": "arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/${ProjectName}.common.*"
# ...
```


When these steps are complete:

```bash
make create-stack
```

### Updates

Update the stack as required:

```bash
make update-stack
```

## 2. Set Configuration Values

The values in `config.yaml` will be available as a dictionary returned by the `configuration()` function (as shown in `index.py`).

Note that environment variables will be expanded, and any key prefixed with `parameterstore_` will incur a ParameterStore `GetParameter` on that value. If encrypted, that value will be decrypted if `kms:Decrypt` is available to the executing role for the given key.


## 3. Initial Local Setup

Sets up your local environment for local Python development by installing the development requirements from `requirements/dev.txt`.

Set up a new `virtualenv` ([pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv) is great):

```bash
pyenv virtualenv my-project
pyenv activate my-project
```

And then install the local dependencies:

```bash
make init
```

### Optional: Assume the Lambda Role
To simulate permissioning parity between the Lambda environment and local, assume the Lambda role created by CloudFormation by creating a new entry in `~/.aws/config`:

```conf
# ~/.aws/config

[profile regular]
output = json
region = us-west-2

[profile development]
output = json
region = us-west-2
source_profile = regular
role_arn = arn:aws:iam::111111111111:role/LambdaFunctionExecutionRo-34K8PIBFMONR
```

Set `development` as the current profile via `export AWS_PROFILE=development`.

## 4. Run tests

Runs all the unit tests in the `tests/` directory.

```bash
make test
```

## 4. Invoke the function locally

Runs the Python code on your local machine.

```bash
make invoke
```

## 5. Build a package for Lambda

Creates a deployable Lambda zip file, and places into `builds`. Note that:

* Only `requirements/lambda.txt` dependencies will be included
* `.pyc` are removed from the repo before `build` is initiated
* All directories save for a blacklist (`.git/`, `tests/`, etc) will be included, as will any `.py` and `.yaml` files

```bash
make build
```

## 6. Deploy

Sends the build to a Lambda ARN. Note that `$ARN` must be set, or this will result in an error. It can be easily retrieved via `make describe-stack`.

```bash
ARN=arn:aws:lambda:us-west-2:111111111111:function:my-function-name make deploy
```

## 7. Delete Everything

Deletes the CloudFormation stack.

```bash
STACK=my-stack make delete-stack
```
