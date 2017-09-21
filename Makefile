STAGING_DIR := package
BUILDS_DIR  := builds
STACK_NAME  := local-lambda-stack
STACK_FILE  := .stack-name
MODULE      := utils
PIP         := pip install -r

.PHONY: init set-stack create-stack update-stack invoke test clean build check-vars deploy

init:
	$(PIP) requirements/dev.txt

_retrieve-stack-name:
	# Get the value of the stack from .stack-name.txt so update-stack can use it
	# $(eval $@STACK := $(shell head -n1 $(STACK_FILE)))
	# @echo $($@STACK)

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
	mkdir -p $(STAGING_DIR)
	mkdir -p $(BUILDS_DIR)
	$(PIP) requirements/lambda.txt -t $(STAGING_DIR)
	cp *.py $(STAGING_DIR)
	cp *.yaml $(STAGING_DIR)
	cp -R $(MODULE) $(STAGING_DIR)
	$(eval $@FILE := deploy-$(shell date +%Y-%m-%d_%H-%M).zip)
	cd $(STAGING_DIR); zip -r $($@FILE) ./*; mv *.zip ../$(BUILDS_DIR)
	@echo "Built $(BUILDS_DIR)/$($@FILE)"
	rm -rf $(STAGING_DIR)

check-vars:  # Ensure that an ARN is set before we can deploy to it.
ifndef ARN
	$(error ARN is undefined)
endif

deploy: build check-vars
	$(eval $@FILE := $(shell ls -t $(BUILDS_DIR) | head -n1 ))
	aws lambda update-function-code --function-name $(ARN) --zip-file "fileb://$(BUILDS_DIR)/$($@FILE)"
	@echo "Deployed $(BUILDS_DIR)/$($@FILE) to $(ARN)"
