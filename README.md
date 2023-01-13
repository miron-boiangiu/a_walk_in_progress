 # A Walk In Progress - BestEM 2022, Adobe's Task

### Pre-Requisites:

* Docker
* Docker compose
* Python 3.8+
* Direnv

You need to have a .envrc file in the root of the project, which contains the
following:

```bash
export API_KEY=<your_api_key>
```

### How to run:

Using the Makefile in the root of the project, you can run the following:

* `make run` - Runs the application locally (you need to replace the API key 
manually in the Game.html file)
* `make docker-build` - Builds the docker image
* `make docker-up` - Runs the docker image
* `make docker-down` - Stops the docker image
* `make docker-clean` - Removes the docker image

### To do:

* deploy to __Kubernetes__ (?)
* quest creation (?)
* write readme properly

Presentation: https://youtu.be/Iyc9XD3X7kE
