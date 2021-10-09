# VARIABLES..

DEFAULT_GOAL = help
VENV := venv
PROJECT_NAME := palza_market
AWS_ACCOUNT_ID := master-hdh
AWS_IAM_USERNAME := ali
AWS_IAM_PASSWORD := Jbany159!
AWS_ACCESS_KEY_ID := AKIAW7OMABNVE2ZGIP6J
AWS_SECRET_ACCESS_KEY := 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
AWS_SERVER_HOST := ec2-3-34-197-3.ap-northeast-2.compute.amazonaws.com
AWS_SERVER_PUBLIC_IP := 3.34.197.3
AWS_SSH_PRIVATE_KEY := secret/paljamarket-keypair.pem
AWS_DOCUMENTDB_PRIVATE_KEY := secret/rds-combined-ca-bundle.pem
AWS_DOCUMENTDB_USERNAME := master
AWS_DOCUMENTDB_PASSWORD := 12345678
AWS_DOCUMENTDB_ENDPOINT := palza-market-db.cluster-cxz5zqdhkz22.ap-northeast-2.docdb.amazonaws.com:27017

help:
	@echo "make initialize: will initialize the project environment such as (MongoDB documents, s3 images store, and server environment)."
	@echo "make server: 	will run the server."
	@echo "make crontab:    will run the crontab job to collect the realstate data from the government api."

ssh:
	# ssh -i "paljamarket-keypair.pem" ubuntu@3.34.197.3
	# ssh -i "paljamarket-keypair.pem" ubuntu@ec2-3-34-197-3.ap-northeast-2.compute.amazonaws.com
	@ ssh -i $(AWS_SSH_PRIVATE_KEY) ubuntu@$(AWS_SERVER_HOST)

nginx.install.ubuntu:
	@sudo apt-get update
	@sudo apt-get install nginx -y

nginx.install.mac:
	@brew update
	@brew install nginx -y

py.setup:
	@python3 -m venv $(VENV)
	@. $(VENV)/bin/activate; \
		$(VENV)/bin/pip3 install -r requirements.txt; \
		$(VENV)/bin/pip3 install -r requirements.dev.txt; 	

py.format:
	@black . --exclude '$(VENV)'
	@flake8 \
		--ignore E501,C901,E203 \
        --exclude .git,__pycache__,$(VENV),build,dist \
        --max-complexity 10

py.clean:
	@rm -rf build; \
		rm -rf dist; \
		rm -rf */*.egg-info; \
		rm -rf *.egg-info; \
		find . -type f -name "*.py[co]" -delete; \
		find . -type d -name "__pycache__" -delete;

run.server:
	@uvicorn src.server:app --reload

db.setup:
	@brew install wget
	@wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem -O ./secret/rds-combined-ca-bundle.pem

db.connect:
	@mongo --ssl --host $(AWS_DOCUMENTDB_ENDPOINT) --sslCAFile rds-combined-ca-bundle.pem --username $(AWS_DOCUMENTDB_USERNAME) --password $(AWS_DOCUMENTDB_PASSWORD)