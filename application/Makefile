# Include project environment variables
include ../.env
export $(shell sed 's/=.*//' ../.env)

IMAGE_TAG = $(COMPOSE_PROJECT_NAME)/node-tools:1.0

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

RECIPE_GEN_MD5_OF_OUTPUT_FILE = MD5=$$(md5sum $@ | cut -c -7);

all: $(CSS_OUT_FILES) $(SCSS_OUT_FILES) $(JS_OUT_FILES)

$(DIST_DIR)/%.css: $(CSS_DIR)/%.css | $(DIST_DIR)
	cp $< $@
	@$(RECIPE_GEN_MD5_OF_OUTPUT_FILE) \
	file="$@"; mv $@ $${file%.css}.$${MD5}.css

$(DIST_DIR)/%.css: $(SCSS_DIR)/%.scss | $(DIST_DIR)
	$(TOOL_CMD) sh -c "sass $< $@ --style compressed --no-source-map"
	@$(RECIPE_GEN_MD5_OF_OUTPUT_FILE) \
	file="$@"; mv $@ $${file%.css}.$${MD5}.css

$(DIST_DIR)/%.js: $(JS_DIR)/%.js | $(DIST_DIR)
	$(TOOL_CMD) sh -c "uglifyjs $< --compress --mangle -o $@"
	@$(RECIPE_GEN_MD5_OF_OUTPUT_FILE) \
	file="$@"; mv $@ $${file%.js}.$${MD5}.js

$(DIST_DIR):
	mkdir -p $@

clean:
	rm -rf $(DIST_DIR)

.PHONY: all clean

print-%:
	@echo '$*=$($*)'
