NAME := 42_python_modules

VENV := .venv
PYTHON := python

FLAKE8 := $(VENV)/bin/flake8
PIP := $(VENV)/bin/pip
MYPY := $(VENV)/bin/mypy

all: lint

clean:
	@echo "cleaning pycaches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "clean done"

lint: $(VENV)
	@echo "checking flake8..."
	@$(FLAKE8) module_0[0-9]/
	@echo "checking mypy..."
	@$(MYPY) module_0[0-9]/
	@echo "all already! :)"

$(VENV):
	@echo "Creating venv..."
	@$(PYTHON) -m venv $(VENV)
	@echo "Installing dependency..."
	$(PIP) install flake8 mypy

fclean: clean
	@echo "Removing .venv..."
	@rm -rf $(VENV)
	@echo "fclean done"

requiremnts: $(VENV)
	@echo "Generating requirements.txt..."
	@$(PIP) freeze > requirements.txt
	@echo "requirements.txt updated!"

install: $(VENV)
	@echo "Installing dependency from requirements.txt..."
	$(PIP) install -r requirements.txt

.PHONY: all clean fclean lint requirements install
