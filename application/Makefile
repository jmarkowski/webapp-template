# Include project environment variables
include ../.env
export $(shell sed 's/=.*//' ../.env)

IMAGE_TAG = $(COMPOSE_PROJECT_NAME)/css-tools:1.0

IMAGE_EXISTS = $(shell docker image ls -q $(IMAGE_TAG) 2> /dev/null)

ifneq ($(IMAGE_EXISTS),)
MNT_PATH = $(shell pwd)
SRC_PATH = /home/node/scss
TOOL_CMD = docker container run --rm \
   --volume=$(MNT_PATH):/mnt \
   --workdir=/mnt \
   --user $(shell id -u):$(shell id -g) \
   $(IMAGE_TAG)
endif

SCSS_FILES += custom-bootstrap.scss

SCSS_DIR = scss
CSS_DIR  = webapp/static/css

CSS_FILES = $(addprefix $(CSS_DIR)/,$(SCSS_FILES:.scss=.css))

all: $(CSS_FILES)

$(CSS_DIR)/%.css: $(SCSS_DIR)/%.scss | $(CSS_DIR)
	$(TOOL_CMD) sh -c "sass $< $@"
	$(TOOL_CMD) sh -c "sass $< $(@:.css=.min.css) --style compressed"

$(CSS_DIR):
	mkdir -p $@

clean:
	rm -f $(CSS_FILES)
	rm -f $(CSS_FILES).map
	rm -f $(CSS_FILES:.css=.min.css)
	rm -f $(CSS_FILES:.css=.min.css).map

.PHONY: all clean