STAGING_DIR   := package
BUILDS_DIR    := builds
EXCLUDE_DIRS  := .git|tests|cloudformation|requirements|$(STAGING_DIR)|$(BUILDS_DIR)
STACK_FILE    := .stack-name
PIP_COMMAND   := pip install -r

.PHONY: init set-stack create-stack update-stack invoke test clean build _check-vars deploy


init:

	$(PIP_COMMAND) requirements/dev.txt

_retrieve-stack-name:
	# Get the value of the stack from .stack-name.txt so update-stack can use it
	# $(eval $@STACK_NAME := $(shell head -n1 $(STACK_FILE)))
	# @echo $($@STACK_NAME)

_set-stack-name-file:
	# If no .stack-name, ask the user to set it.


create-stack: _set-stack-name-file
	aws cloudformation create-stack \
	  --stack-name $(STACK_NAME) \
	  --template-body file://cloudformation/template.yaml \
	  --parameters file://cloudformation/parameters.json \
	  --capabilities CAPABILITY_IAM

update-stack: _retrieve-stack-name
	aws cloudformation update-stack \
	  --stack-name $(STACK_NAME) \
	  --template-body file://cloudformation/template.yaml \
	  --parameters file://cloudformation/parameters.json \
	  --capabilities CAPABILITY_IAM

# delete-stack: _retrieve-stack-name
# 	aws cloudformation delete-stack \
# 	  --stack-name $(STACK_NAME) \

invoke:
	STUB=true python index.py

test:
	py.test -rsxX -q -s tests

clean:
	rm -rf $(STAGING_DIR)
	rm -rf $(BUILDS_DIR)


build: test
	find . -type f -ipath '*.pyc' -delete  # Get rid of unnecessary .pyc files.
	mkdir -p $(STAGING_DIR)
	mkdir -p $(BUILDS_DIR)
	$(PIP_COMMAND) requirements/lambda.txt -t $(STAGING_DIR)
	cp *.py $(STAGING_DIR)
	cp *.yaml $(STAGING_DIR)
        # Copy all other directories, excluding the blacklist.
	$(eval $@DEPLOY_DIRS := $(shell find . -type d -depth 1 | grep -v  -E '$(EXCLUDE_DIRS)'   ))
	cp -R $($@DEPLOY_DIRS) $(STAGING_DIR)
	$(eval $@FILE := deploy-$(shell date +%Y-%m-%d_%H-%M).zip)
	cd $(STAGING_DIR); zip -r $($@FILE) ./*; mv *.zip ../$(BUILDS_DIR)
	@echo "Built $(BUILDS_DIR)/$($@FILE)"
	rm -rf $(STAGING_DIR)

_check-vars:  # Ensure that an ARN is set before we can deploy to it.
ifndef ARN
	$(error ARN is undefined)
endif

deploy: build _check-vars
	$(eval $@FILE := $(shell ls -t $(BUILDS_DIR) | head -n1 ))
	aws lambda update-function-code --function-name $(ARN) --zip-file "fileb://$(BUILDS_DIR)/$($@FILE)"
	@echo "Deployed $(BUILDS_DIR)/$($@FILE) to $(ARN)"
