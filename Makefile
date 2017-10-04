STAGING_DIR   := package
BUILDS_DIR    := builds
PARAMS_FILE   := cloudformation/parameters.json
EXCLUDE_DIRS  := .git|tests|cloudformation|requirements|$(STAGING_DIR)|$(BUILDS_DIR)
PIP_COMMAND   := pip install -r

.PHONY: init create-stack update-stack delete-stack describe-stack invoke test clean build _check-arn deploy

# Read the cloudformation/parameters.json file for the ProjectName and EnvionmentName.
# Use these to name the CloudFormation stack.
PROJECT_NAME = $(shell cat $(PARAMS_FILE) | python -c 'import sys, json; j = [i for i in json.load(sys.stdin) if i["ParameterKey"]=="ProjectName"][0]["ParameterValue"]; print j')
ENVIRONMENT_NAME = $(shell cat $(PARAMS_FILE) | python -c 'import sys, json; j = [i for i in json.load(sys.stdin) if i["ParameterKey"]=="EnvironmentName"][0]["ParameterValue"]; print j')
STACK_NAME = $(PROJECT_NAME)-$(ENVIRONMENT_NAME)-stack


init:
	$(PIP_COMMAND) requirements/dev.txt

create-stack:
	aws cloudformation create-stack \
	  --stack-name $(STACK_NAME) \
	  --template-body file://cloudformation/template.yaml \
	  --parameters file://cloudformation/parameters.json \
	  --capabilities CAPABILITY_IAM

update-stack:
	aws cloudformation update-stack \
	  --stack-name $(STACK_NAME) \
	  --template-body file://cloudformation/template.yaml \
	  --parameters file://cloudformation/parameters.json \
	  --capabilities CAPABILITY_IAM

delete-stack:
	aws cloudformation delete-stack \
	  --stack-name $(STACK_NAME)

describe-stack:
	aws cloudformation describe-stacks \
	  --stack-name $(STACK_NAME)

invoke:
	IS_LOCAL=true ProjectName=$(PROJECT_NAME) EnvironmentName=$(ENVIRONMENT_NAME) python index.py

test:
	py.test -rsxX -q -s tests

clean:
	rm -rf $(STAGING_DIR)
	rm -rf $(BUILDS_DIR)

build: test
	mkdir -p $(STAGING_DIR)
	mkdir -p $(BUILDS_DIR)
	$(PIP_COMMAND) requirements/lambda.txt -t $(STAGING_DIR)
	cp *.py $(STAGING_DIR)
	cp *.yaml $(STAGING_DIR)
        # Copy all other directories, excluding the blacklist.
	$(eval $@DEPLOY_DIRS := $(shell find . -type d -maxdepth 1 -mindepth 1 | grep -v  -E '$(EXCLUDE_DIRS)'))
	cp -R $($@DEPLOY_DIRS) $(STAGING_DIR)
	find $(STAGING_DIR) -type f -ipath '*.pyc' -delete  # Get rid of unnecessary .pyc files.
	$(eval $@FILE := deploy-$(shell date +%Y-%m-%d_%H-%M).zip)
	cd $(STAGING_DIR); zip -r $($@FILE) ./*; mv *.zip ../$(BUILDS_DIR)
	@echo "Built $(BUILDS_DIR)/$($@FILE)"
	rm -rf $(STAGING_DIR)

_check-arn:  # Ensure that an ARN is set before we can deploy to it.
ifndef ARN
	$(error ARN is undefined; set to the appropriate Lambda ARN to deploy to. View with `make describe-stack`)
endif

deploy: build _check-arn
	$(eval $@FILE := $(shell ls -t $(BUILDS_DIR) | head -n1 ))
	aws lambda update-function-code --function-name $(ARN) --zip-file "fileb://$(BUILDS_DIR)/$($@FILE)"
	@echo "Deployed $(BUILDS_DIR)/$($@FILE) to $(ARN)"
