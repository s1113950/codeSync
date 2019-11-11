SHELL := bash

.PHONY: \
       clean \
       dev \
       dist \
       install \
       lint \
       release \
       uninstall \
       venv

all: dev

dev:
	@tox -e dev

test:
	@tox -e unit

lint:
	@echo "Running lint with flake8"
	@tox -e lint

install:
	@python3 setup.py install

uninstall:
	@pip3 uninstall -y codesync

clean:
	rm -rf .tox/venv
	find . -name '*.pyc' -delete

dist: dev
	.tox/venv/bin/pip wheel --wheel-dir=dist .

release: dist
	. .tox/venv/bin/activate && twine upload dist/codesync* ; deactivate
