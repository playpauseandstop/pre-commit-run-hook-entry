.PHONY: install lint lint-only test test-only

POETRY ?= poetry
PRE_COMMIT ?= pre-commit
PYTHON ?= $(POETRY) run python

install: .install
.install: pyproject.toml poetry.toml poetry.lock
	$(POETRY) install
	touch $@

lint: install lint-only
lint-only:
	SKIP=$(SKIP) $(PRE_COMMIT) run --all $(HOOK)

poetry.toml:
	$(POETRY) config --local virtualenvs.create true
	$(POETRY) config --local virtualenvs.in-project true

test: lint test-only
test-only:
	$(PYTHON) -m pytest
