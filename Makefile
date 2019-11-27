IMAGE_NAME = acolyte
COMMIT = $(shell git rev-parse --short=8 HEAD)
BUILD = docker build -t $(IMAGE_NAME):$(COMMIT) .
COMPOSE_RUN = COMMIT=$(COMMIT) docker-compose -f docker-compose.yaml run --rm


upgrade-requirements:
	pip-compile requirements.in -o requirements.txt -U

format:
	isort -y
	black --target-version py36 .

check:
	flake8
	mypy .
	isort --check --diff
	black . --check --diff

build:
	$(BUILD)

run: build
	$(COMPOSE_RUN) acolyte
