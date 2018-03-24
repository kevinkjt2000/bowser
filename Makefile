COMPOSE ?= docker-compose

.PHONY: test
test:
	$(COMPOSE) run --rm bowser pytest

.PHONY: build
build:
	$(COMPOSE) build

.PHONY: coverage
coverage:
	$(COMPOSE) run --rm bowser codecov
