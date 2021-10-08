DEFAULT_GOAL = help
VENV := venv
PROJECT_NAME := palza_market

help:
	@echo "make initialize: will initialize the project environment such as (MongoDB documents, s3 images store, and server environment)."
	@echo "make server: 	will run the server."
	@echo "make crontab:    will run the crontab job to collect the realstate data from the government api."

# Python commands..

setup:
	@python3 -m venv $(VENV)
	@. $(VENV)/bin/activate; \
		$(VENV)/bin/pip3 install -r requirements.txt; \
		$(VENV)/bin/pip3 install -r requirements.dev.txt; 	
	@. $(VENV)/bin/activate; python3 -m playwright install

format:
	@black . --exclude './$(VENV)'
	@flake8 \
		--ignore E501,C901,E203 \
        --exclude .git,__pycache__,$(VENV),build,dist \
        --max-complexity 10

clean:
	@rm -rf build; \
		rm -rf dist; \
		rm -rf */*.egg-info; \
		rm -rf *.egg-info; \
		find . -type f -name "*.py[co]" -delete; \
		find . -type d -name "__pycache__" -delete;

# Project commands..

run.initialize:
	@python3 -m src.initialize

run.server:
	@python3 -m src.server

run.crontab:
	@python3 -m src.crontab


# MongoDB commands..

# 