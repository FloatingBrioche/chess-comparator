#################################################################################
#
# Makefile to build the project
#
#################################################################################

PROJECT_NAME = chess-comparator
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PIP := pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> Checking python version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && export PYTHONPATH=${PYTHONPATH} && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################

## Run the black code check
run-black:
	$(call execute_in_env, black  ./main.py ./helpers/*.py ./test/*.py)

## Run the unit tests
unit-test:
	$(call execute_in_env, pytest test/* -vv --testdox)

## Run the coverage check
coverage:
	rm ./docs/coverage.svg
	$(call execute_in_env, coverage run --omit 'venv/*' -m pytest test/* && coverage report -m > ./docs/coverage.txt && coverage-badge -o ./docs/coverage.svg)

## Run all checks
run-checks: run-black unit-test coverage