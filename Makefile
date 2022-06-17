.PHONY: \
	install \
	lint \
	lint-and-test \
	list-outdated \
	test

include python.mk

install: install-python

lint: lint-python

lint-and-test: lint test

list-outdated: list-outdated-python

test: test-python
