.PHONY: test tests install pep8 clean delete

SERVICE_NAME := origin_financial_challenge

DOCKER_COMPOSE_EXEC := docker-compose exec $(SERVICE_NAME) su -c

NAME := -g
LIB := -g

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

poetry:
	poetry install

poetry-add:
	poetry add $(LIB)

pre-commit:
	poetry run pre-commit install
	poetry run pre-commit run -a

virtualenv:
	virtualenv -p python3 .venv

up:
	docker-compose up -d

build:
	poetry run pre-commit install
	docker-compose up --build -d
	docker-compose ps
	docker network ls

restart:
	docker-compose restart $(SERVICE_NAME) $(DB_SERVICE_NAME)

stop:
	docker-compose stop
	docker-compose ps

logs:
	docker-compose logs -f $(SERVICE_NAME)

ps:
	docker-compose ps

report:
	docker-compose "pytest --cov=$(SERVICE_NAME) --color=yes app/tests/"
	docker-compose "coverage report"
	docker-compose "coverage html -d coverage_html"

shell:
	docker-compose "ipython"

tests:
	$(DOCKER_COMPOSE_EXEC) "pytest -v --color=yes app/tests/"

list-env:
	$(DOCKER_COMPOSE_EXEC) "env"

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .coverage
	rm -rf  coverage_html
	rm -rf .pytest_cache
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
	rm -rf celerybeat-schedule
	rm -rf *.pyc
	rm -rf *__pycache__
