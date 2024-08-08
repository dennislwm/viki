.PHONY: default install_new apply fetch plan shell_clean test test_verbose

default: test

install_new:
	pipenv install paramiko==3.4.0 pyyaml==6.0.1
	pipenv install --dev pytest==8.2.2

apply:
	python viki.py -p $(DIR) apply

fetch:
	python viki.py -p $(DIR) fetch

plan:
	python viki.py -p $(DIR) plan

shell_clean:
	pipenv --rm

test:
	PYTHONPATH=.:../ pytest

test_verbose:
	PYTHONPATH=.:../ pytest -v -s