# Check if running inside a Pixi environment
ifndef PIXI_PROJECT_NAME
$(error Pixi environment is not active. Run 'pixi run make' or 'pixi shell' first)
endif

.PHONY: all cv resume

all: cv resume

cv:
	$(MAKE) -C assets/cv all

resume:
	$(MAKE) -C assets/resume all
