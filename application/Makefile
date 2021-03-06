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

SCSS_FILES += custom-bootstrap.scss

SCSS_DIR = scss
CSS_DIR  = static/css
JS_DIR = static/js

CSS_FILES = $(addprefix $(CSS_DIR)/,$(SCSS_FILES:.scss=.css))
CSS_MIN_FILES = $(addprefix $(CSS_DIR)/,$(SCSS_FILES:.scss=.min.css))

# JS Files (the source and output files are in the same directory)
JS_ALL_FILES = $(wildcard $(JS_DIR)/*.js)
JS_FILES = $(filter-out $(wildcard $(JS_DIR)/*.min.js),$(JS_ALL_FILES))
JS_MIN_FILES = $(JS_FILES:.js=.min.js)

RECIPE_GEN_MD5_OF_OUTPUT_FILE = MD5=$$(md5sum $@ | cut -c -7);

ifeq ($(CONFIG_STRATEGY),production)
TARGETS=$(CSS_MIN_FILES) $(JS_MIN_FILES)
else
TARGETS=$(CSS_FILES) $(CSS_MIN_FILES) $(JS_MIN_FILES)
endif

all: $(TARGETS)

$(CSS_DIR)/%.css: $(SCSS_DIR)/%.scss FORCE | $(CSS_DIR)
	$(TOOL_CMD) sh -c "sass $< $@"
	@$(RECIPE_GEN_MD5_OF_OUTPUT_FILE) \
	file="$@"; mv $@ $${file%.css}.$${MD5}.css

$(CSS_DIR)/%.min.css: $(SCSS_DIR)/%.scss FORCE | $(CSS_DIR)
	$(TOOL_CMD) sh -c "sass $< $@ --style compressed"
	@$(RECIPE_GEN_MD5_OF_OUTPUT_FILE) \
	file="$@"; mv $@ $${file%.min.css}.$${MD5}.min.css

$(JS_DIR)/%.min.js: $(JS_DIR)/%.js FORCE | $(JS_DIR)
	$(TOOL_CMD) sh -c "uglifyjs $< --compress --mangle -o $@"
	@$(RECIPE_GEN_MD5_OF_OUTPUT_FILE) \
	file="$@"; mv $@ $${file%.min.js}.$${MD5}.min.js

$(CSS_DIR):
	mkdir -p $@

clean:
	rm -f $(CSS_FILES:.css=*.css)
	rm -f $(CSS_FILES:.css=*.css.map)
	rm -f $(CSS_FILES:.css=*.min.css)
	rm -f $(CSS_FILES:.css=*.min.css.map)
	rm -f $(JS_MIN_FILES:.min.js=*.min.js)

FORCE:

.PHONY: all clean FORCE

print-%:
	@echo '$*=$($*)'
