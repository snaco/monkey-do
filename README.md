# monkey-do
Tool for rapid prototyping of functional REST APIs.
#
### Prerequisites:
- python 3.9 installed
- pipenv installed
- docker installed
### Hello world set up steps:
1. To build and run the docker image first run ```make config-link``` to create a local config for monkey-do in ~/.config/monkey-do
2. Run ```make monkey-do``` to build and run the service
3. run ```curl localhost:8484/hello/world.json``` to get a json response
4. open http://localhost:8484/hello/world in your browser
### Configuring Monkey-do
Refer to the sample_config folder to see how everything is used. the config.mnkc file is the configuration for the api and it's endpoints, routes etc. This is where you will tell monkey-do to use raw text, json, scripts etc when a certain enpoint is hit.
#
## Makefle:
```make init-config``` - makes a copy of the sample_config into config folder which is used for the app WILL OVERRIDE ANY EXISTING CONFIGS

```make monkey-do``` - build and run monkey-do

```make docker-build``` - makes requirements and builds the docker image

```make docker-run``` - run monkey-do as a docker container

```make docker-rm``` - deletes the docker container (must be stopped first) and deletes the image. use this between builds

```make help``` - show this stuff
