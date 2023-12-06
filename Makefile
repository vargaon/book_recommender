NAME := book_recommender

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Welcome to $(NAME)!"
	@echo "Use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  build		build docker image"
	@echo "  down		down docker container"
	@echo "  start		start docker container"
	@echo "  stop		stop docker container"
	@echo "  up		up docker container"
	@echo ""


.PHONY: build
build:
	docker-compose -p $(NAME) build --no-cache $(s)

.PHONY: up
up:
	docker-compose -p $(NAME) up -d $(s)

.PHONY: down
down:
	docker-compose -p $(NAME) down $(s)

.PHONY: start
start:
	docker-compose -p $(NAME) start $(s)

.PHONY: stop
stop:
	docker-compose -p $(NAME) stop $(s)
