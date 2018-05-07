SRCS := Pipfile.lock $(shell find -type f -name "*.py")
SHELL := /bin/bash

.PHONY : test
test : .coverage

.PHONY : package
package : dist/bowser.pex

.PHONY : requirements
requirements : Pipfile.lock
	pipenv install --dev --keep-outdated

.coverage : $(SRCS)
	pipenv run pytest

dist/bowser.pex : $(SRCS)
	pipenv run pex -c bowser -o dist/bowser.pex .

Pipfile.lock : Pipfile
	pipenv lock

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
