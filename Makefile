# VARIABLES..

DEFAULT_GOAL = help
VENV := venv
PROJECT_NAME := palza_market
AWS_ACCOUNT_ID := master-hdh
AWS_IAM_USERNAME := ali
AWS_IAM_PASSWORD := Jbany159!
AWS_ACCESS_KEY_ID := AKIAW7OMABNVE2ZGIP6J
AWS_SECRET_ACCESS_KEY := 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
AWS_SERVER_PUBLIC_IP := 13.125.147.119
AWS_SSH_PRIVATE_KEY := ./secret/paljamarket-keypair.pem
LOCALHOST_MONGODB_USERNAME := master
LOCALHOST_MONGODB_PASSWORD := 12345678
LOCALHOST_MONGODB_ENDPOINT := localhost:27017
LOCALHOST_MONGODB_DATABASE := palza_market

help:
	@echo "make initialize: will initialize the project environment such as (MongoDB documents, s3 images store, and server environment)."
	@echo "make server: 	will run the server."
	@echo "make crontab:    will run the crontab job to collect the realstate data from the government api."

proj.initialize:
	@brew install -y zip
	@brew install -y unzip
	@brew install -y wget

ssh.access:
	# ssh -i "paljamarket-keypair.pem" ubuntu@13.125.147.119
	@ssh -i $(AWS_SSH_PRIVATE_KEY) ubuntu@$(AWS_SERVER_PUBLIC_IP)

ssh.upload:
	@zip --exclude=*venv* --exclude=*.git* -r project.zip ./ 
	@scp -i $(AWS_SSH_PRIVATE_KEY) project.zip ubuntu@$(AWS_SERVER_PUBLIC_IP):project.zip
	@scp -i $(AWS_SSH_PRIVATE_KEY) ./src/scripts/setup.sh ubuntu@$(AWS_SERVER_PUBLIC_IP):setup.sh
	@scp -i $(AWS_SSH_PRIVATE_KEY) ./src/scripts/refresh.sh ubuntu@$(AWS_SERVER_PUBLIC_IP):refresh.sh
	@rm project.zip

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

py.run:
	@ENV=DEV uvicorn src.server:app --reload --host 0.0.0.0 &

db.install:
	@brew tap mongodb/brew
	@brew install mongodb-community@5.0
	@brew services start mongodb-community@5.0

db.setup:
	@mongo --eval "db.getSiblingDB('$(LOCALHOST_MONGODB_DATABASE)').createUser({user: '$(LOCALHOST_MONGODB_USERNAME)', pwd: '$(LOCALHOST_MONGODB_PASSWORD)', roles: [{ role: 'readWrite', db: '$(LOCALHOST_MONGODB_DATABASE)' }, { role: 'read', db: 'reporting' }] })"

db.connect:
	@mongo --host $(LOCALHOST_MONGODB_ENDPOINT) --username $(LOCALHOST_MONGODB_USERNAME) --password $(LOCALHOST_MONGODB_PASSWORD) --authenticationDatabase $(LOCALHOST_MONGODB_DATABASE)

ssl.secret:
	@openssl rand -hex 32