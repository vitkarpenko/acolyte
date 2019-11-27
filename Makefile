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

