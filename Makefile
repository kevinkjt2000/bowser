.PHONY: test
test:
	docker-compose run --rm bowser pytest -v
