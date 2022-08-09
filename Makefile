.PHONY: \
	clean \
	distclean \
	install \
	lint \
	lint-and-test \
	list-outdated \
	test \
	test-only

PROJECT = pre_commit_run_hook_entry

include python.mk

TOX ?= tox

all: install

clean: clean-python

distclean: distclean-python

install: install-python

lint: lint-python

lint-and-test: lint test

list-outdated: list-outdated-python

test: install clean test-only

test-only:
	TOXENV=$(TOXENV) $(TOX)
