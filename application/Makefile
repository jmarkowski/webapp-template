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

STYLE_SRC_DIR  = static/styles
SCSS_PARTIALS = $(wildcard $(STYLE_SRC_DIR)/_*.scss)
# STYLE_SRCS excludes _*.scss files as these are partial files that are included
# by the top-level scss files.
STYLE_SRCS = $(filter-out $(SCSS_PARTIALS), $(wildcard $(STYLE_SRC_DIR)/*.*))
STYLE_OBJS = $(addprefix $(DIST_DIR)/,$(addsuffix .css, $(basename $(notdir $(STYLE_SRCS)))))

SCRIPT_SRC_DIR = static/scripts
SCRIPT_SRCS = $(wildcard $(SCRIPT_SRC_DIR)/*.*)
SCRIPT_OBJS = $(addprefix $(DIST_DIR)/,$(addsuffix .js, $(basename $(notdir $(SCRIPT_SRCS)))))

DIST_DIR = static/dist

all: clean styles scripts

styles: | $(DIST_DIR)
	$(TOOL_CMD) npx parcel build $(STYLE_SRCS) --dist-dir $(DIST_DIR) --public-url /$(DIST_DIR)
	./hashfile -r $(STYLE_OBJS)

scripts: | $(DIST_DIR)
	$(TOOL_CMD) npx parcel build $(SCRIPT_SRCS) --dist-dir $(DIST_DIR) --public-url /$(DIST_DIR)
	./hashfile -r $(SCRIPT_OBJS)

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
