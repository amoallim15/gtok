.PHONY: format
.DEFAULT_GOAL := help
VENV := venv

# 
format:
	@black . --exclude '$(VENV)'