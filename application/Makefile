# Include project environment variables
include ../.env
export $(shell sed 's/=.*//' ../.env)

IMAGE_TAG = $(COMPOSE_PROJECT_NAME)/node-tools:2.0

IMAGE_EXISTS = $(shell docker image ls -q $(IMAGE_TAG) 2> /dev/null)

ifneq ($(IMAGE_EXISTS),)
MNT_PATH = $(shell pwd)
TOOL_CMD = docker container run --rm \
   --volume=$(MNT_PATH):/application \
   --workdir=/application \
   --user $(shell id -u):$(shell id -g) \
   $(IMAGE_TAG)
endif

STYLES_DIR  = static/styles
STYLES = $(notdir $(wildcard $(STYLES_DIR)/*.*))
STYLES_CSS = $(addprefix $(DIST_DIR)/,$(addsuffix .css, $(basename $(STYLES))))

SCRIPTS_DIR = static/scripts
SCRIPTS = $(notdir $(wildcard $(SCRIPTS_DIR)/*.*))
SCRIPTS_JS = $(addprefix $(DIST_DIR)/,$(addsuffix .js, $(basename $(SCRIPTS))))

DIST_DIR = static/dist

all: clean styles scripts

styles: | $(DIST_DIR)
	$(TOOL_CMD) npx parcel build $(STYLES_DIR)/*.* --dist-dir $(DIST_DIR) --public-url /$(DIST_DIR)
	./hashfile -r $(STYLES_CSS)

scripts: | $(DIST_DIR)
	$(TOOL_CMD) npx parcel build $(SCRIPTS_DIR)/*.* --dist-dir $(DIST_DIR) --public-url /$(DIST_DIR)
	./hashfile -r $(SCRIPTS_JS)

install:
	$(TOOL_CMD) npm install

$(DIST_DIR):
	mkdir -p $@

clean:
	rm -rf $(DIST_DIR)

.PHONY: \
	all \
	clean \
	install \
	scripts \
	styles

print-%:
	@echo '$*=$($*)'
