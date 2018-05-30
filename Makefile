SRCS := $(shell find -type f -name "*.py")
SHELL := /bin/bash

.PHONY : test
test : tests-unit

.PHONY : package
package : dist/bowser.pex

.PHONY : requirements
requirements : Pipfile.lock

.PHONY : tests-unit
tests-unit : .coverage

.coverage : $(SRCS)
	pipenv run pytest tests/unit

dist/bowser.pex : dist/requirements.pex $(SRCS)
	pipenv run pex . --script=bowser --output-file=dist/bowser.pex --pex-path=dist/requirements.pex

dist/requirements.pex : requirements
	pipenv run pex --output-file=dist/requirements.pex --requirement=<(pipenv lock --requirements | awk '{print $$1}') --index-url=https://test.pypi.org/simple

Pipfile.lock : Pipfile
	pipenv install --dev

.PHONY : travis-install
travis-install :
	pip install --upgrade --force-reinstall pip "pipenv<11.1" pex
	# Need to install setuptools twice because of some quirk in the 3.6 virtualenv on travis
	# https://github.com/travis-ci/travis-ci/issues/9582
	pip install --upgrade --force-reinstall "setuptools<34.0,>=20.3"
	pip install --upgrade --force-reinstall "setuptools<34.0,>=20.3"
	pipenv install --dev

.PHONY : travis-script
travis-script : test
	pipenv run pip check

.PHONY : clean
clean :
	find -name "*.pyc" -delete
	rm -rf dist/ bowser.egg-info/ .eggs/ .coverage .pytest_cache/ .ropeproject/
	pipenv --rm
