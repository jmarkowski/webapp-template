# Include project environment variables
include ../.env
export $(shell sed 's/=.*//' ../.env)

IMAGE_TAG = $(COMPOSE_PROJECT_NAME)/node-tools:1.0

IMAGE_EXISTS = $(shell docker image ls -q $(IMAGE_TAG) 2> /dev/null)

ifneq ($(IMAGE_EXISTS),)
MNT_PATH = $(shell pwd)
TOOL_CMD = docker container run --rm \
   --volume=$(MNT_PATH):/mnt \
   --workdir=/mnt \
   --user $(shell id -u):$(shell id -g) \
   $(IMAGE_TAG)
endif

CSS_DIR  = static/css
CSS_FILES = $(notdir $(wildcard $(CSS_DIR)/*.css))
CSS_OUT_FILES = $(addprefix $(DIST_DIR)/,$(CSS_FILES))

SCSS_DIR = scss
SCSS_FILES += custom-bootstrap.scss
SCSS_OUT_FILES = $(addprefix $(DIST_DIR)/,$(SCSS_FILES:.scss=.css))

JS_DIR = static/js
JS_FILES = $(notdir $(wildcard $(JS_DIR)/*.js))
JS_OUT_FILES = $(addprefix $(DIST_DIR)/,$(JS_FILES))

DIST_DIR = static/dist

all: css_styles scss_styles scripts

css_styles: | $(DIST_DIR)
	$(TOOL_CMD) npx parcel build $(CSS_DIR)/*.css --dist-dir $(DIST_DIR) --public-url /$(DIST_DIR)
	./hashfile -r $(CSS_OUT_FILES)

scss_styles: | $(DIST_DIR)
	$(TOOL_CMD) npx parcel build $(SCSS_DIR)/*.scss --dist-dir $(DIST_DIR) --public-url /$(DIST_DIR)
	./hashfile -r $(SCSS_OUT_FILES)

scripts: | $(DIST_DIR)
	$(TOOL_CMD) npx parcel build $(JS_DIR)/*.js --dist-dir $(DIST_DIR) --public-url /$(DIST_DIR)
	./hashfile -r $(JS_OUT_FILES)

$(DIST_DIR):
	mkdir -p $@

clean:
	rm -rf $(DIST_DIR)

.PHONY: all clean

print-%:
	@echo '$*=$($*)'
