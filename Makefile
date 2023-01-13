IMG=map-app-server-image
APP=map-app-server
DOCKERHUB_USER=gabilb
IMG_TAG=$(DOCKERHUB_USER)/$(IMG)

all: run

PHONY: run
run:
	python3 server.py

PHONY: docker-build
docker-build:
	docker compose build

PHONY: docker-up
docker-up:
	docker compose up

PHONY: docker-down
docker-down:
	docker compose down --remove-orphans 2>/dev/null

PHONY: docker-push
docker-push:
	docker image tag $(IMG) $(IMG_TAG)
	docker image push $(IMG_TAG)

PHONY: docker-clean
docker-clean: docker-down
	docker image rm -f $(IMG) 2> /dev/null
	@docker image prune -f