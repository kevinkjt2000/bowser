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
	pip install --upgrade --force-reinstall pip
	pip install --upgrade --force-reinstall "pipenv<11.1"
	pip install --upgrade --force-reinstall pex
	pipenv install --dev

.PHONY : travis-script
travis-script : test
	pipenv run pip check

.PHONY : clean
clean :
	find -name "*.pyc" -delete
	rm -rf dist/ bowser.egg-info/ .eggs/ .coverage .pytest_cache/ .ropeproject/
	pipenv --rm
