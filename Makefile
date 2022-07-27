help:           ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

docker-build:	## makes requirements and builds the docker image
	@docker build --tag snaco/monkey-do .

docker-rm:	## deletes the docker container (must be stopped first) and deletes the image. use this between builds
	@docker container prune
	@docker rmi monkey-do

docker-run:	## run monkey-do as a docker container
	@docker run -p 8484:8484 \
	 -v $$HOME/.config/monkey-do:/app/config \
	 monkey-do-docker

init-sample-config:    ## make a copy of the sample_config into config folder which is used for the app
	@mkdir -p ./config
	@cp -r ./sample_config/. ./config

monkey-do:	## run docker-build and docker-run
monkey-do: docker-build
monkey-do: docker-run

lint:	## run linting on src/
	@pylint src/ --fail-under 10

bootstrap:	## setup the local dev environment
	@pipenv install --dev
	@cp .githooks/pre-commit .git/hooks/pre-commit
bootstrap: init-sample-config
