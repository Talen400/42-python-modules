NAME := 42_python_modules
PYTHON := python

VENV ?= .venv

SRC = module_0[0-9]/

DEPS = flake8 mypy

FLAKE8 := $(VENV)/bin/flake8
PIP := $(VENV)/bin/pip
MYPY := $(VENV)/bin/mypy

MYPY_MANDATORY_FLAGS := --warn-return-any \
						--warn-unused-ignores \
						--ignore-missing-imports \
						--disallow-untyped-defs \
						--check-untyped-defs

MYPY_EXTRA_FLAGS := --strict

LINK_PIP := https://pypi.org/simple/


all: install

install: $(VENV)

$(VENV):
	@echo "Creating venv..."
	$(PYTHON) -m venv $(VENV)
	@echo "Upgrading pip..."
	$(PIP) install --upgrade pip --index-url $(LINK_PIP)
	@echo "Installing dependency..."
	$(PIP) install --index-url $(LINK_PIP) $(DEPS)

run:
	@echo "Not running"

debug:
	@echo "Not debug"

lint: $(VENV)
	@echo "Normal lint..."
	@echo "Checking flake8..."
	$(FLAKE8) $(SRC)
	@echo "'flake8' all already! :)"
	@echo "Checking mypy..."
	$(MYPY) $(MYPY_MANDATORY_FLAGS) $(SRC)
	@echo "'mypy' all already! :)"

lint-strict: $(VENV)
	@echo "Extra lint..."
	@echo "checking flake8..."
	$(FLAKE8) $(SRC)
	@echo "'flake8' all already! :)"
	@echo "Checking mypy..."
	$(MYPY) $(MYPY_EXTRA_FLAGS) $(SRC)
	@echo "'mypy' all already! :)"

clean:
	@echo "Cleaning pycaches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@echo "Clean done"

fclean: clean
	@echo "Removing .venv..."
	rm -rf $(VENV)
	@echo "fclean done"

re: fclean all

.PHONY: all clean fclean re run debug lint lint-strict install
.DEFAULT_GOAL = all
