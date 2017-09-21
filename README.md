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
├── index.py                           # Entry point for the Lambda function.
├── utils                              # Python package `utils`.
│   ├── __init__.py
│   ├── localcontext.py
│   ├── helpers.py
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
```

## 1. Initial AWS Setup

Creates a CloudFormation stack with the Lambda function, an execution role, and an optional CloudWatch event to run on a recurring basis.

```
make create-stack
```


## 2. Initial Local Setup

Sets up your local environment for local Python development.

### IAM
Assume the role created by CloudFormation by creating a new entry in `~/.aws/config`:

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

### Python

Installs the development requirements from `requirements/dev.txt`.

In a new `virtualenv` ([pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv) is great), install the local dependencies:

```bash
cd local-lambda-toolkit
make init
```

## 3. Run tests

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

Creates a deployable Lambda zip file, and places into `builds`.

```bash
make build
```

## 6. Deploy

Sends the build to a Lambda ARN.

```bash
ARN=arn:aws:lambda:us-west-2:111111111111:function:my-function-name make deploy
```
