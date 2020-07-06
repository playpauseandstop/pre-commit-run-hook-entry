.PHONY: install lint lint-only test test-only

POETRY ?= poetry
PRE_COMMIT ?= pre-commit
PYTHON ?= $(POETRY) run python

install: .install
.install: pyproject.toml poetry.lock
	$(POETRY) config --local virtualenvs.create true
	$(POETRY) config --local virtualenvs.in-project true
	$(POETRY) install
	touch $@

lint: install lint-only
lint-only:
	SKIP=$(SKIP) $(PRE_COMMIT) run --all $(HOOK)

test: lint test-only
test-only:
	$(PYTHON) -m pytest --cov --no-cov-on-fail
