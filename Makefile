IMAGE := data-pirate
PACKAGE := data_pirate
PWD := $(shell pwd)
CONTAINER := /project
VOLUME := $(PWD)/dados
HOST := $(CONTAINER)/dados


##### CREATE DOCKER IMAGE #####
mkdir-%:
	mkdir -p $(PWD)/$*
	chmod a+w $(PWD)/$*

build: mkdir-dados
	echo "CREATE DOCKER IMAGE"
	docker build -t $(IMAGE) .


##### EXECUTE DOCKER #####
run:
	docker run -it \
		-v $(VOLUME):$(HOST) $(IMAGE)
