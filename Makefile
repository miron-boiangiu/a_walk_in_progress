IMG=map-app-server-image
APP=map-app-server
DOCKERHUB_USER=gabilb
IMG_TAG=$(DOCKERHUB_USER)/$(IMG)

all: run

run:
	python3 server.py

docker-build:
	docker compose build

docker-up:
	docker compose up

docker-down:
	docker compose down

docker-push:
	docker image tag $(IMG) $(IMG_TAG)
	docker image push $(IMG_TAG)

docker-clean: docker-down
	docker image rm -f $(IMG) 2> /dev/null
	@docker image prune -f