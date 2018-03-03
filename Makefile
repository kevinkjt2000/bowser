COMPOSE ?= docker-compose

.PHONY: test
test:
	$(COMPOSE) run --rm bowser pytest -v

.PHONY: build
build:
	$(COMPOSE) build

.PHONY: coveralls
coveralls:
	$(COMPOSE) run --rm bowser coveralls
