STAGING_DIR := package
BUILDS_DIR  := builds
STACK_NAME  := local-lambda-stack
MODULE      := my_lambda_package
PIP         := pip install -r

.PHONY: init provision invoke test clean build check_vars deploy

init:
	$(PIP) requirements/dev.txt

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

check_vars:  # Ensure that an ARN is set before we can deploy to it.
ifndef ARN
	$(error ARN is undefined)
endif

deploy: build check_vars
	$(eval $@FILE := $(shell ls -t $(BUILDS_DIR) | head -n1 ))
	aws lambda update-function-code --function-name $(ARN) --zip-file "fileb://$(BUILDS_DIR)/$($@FILE)"
	@echo "Deployed $(BUILDS_DIR)/$($@FILE) to $(ARN)"
