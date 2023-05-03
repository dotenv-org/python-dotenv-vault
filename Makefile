.PHONY: clean-pyc clean-build test

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr src/*.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

build: clean
	python -m build

uninstall_local:
	pip uninstall python-dotenv-vault -y

install_local:
	pip install .

test: install_local
	python -m unittest -v dotenv_vault.test_vault

release: build
	twine check dist/*
	twine upload dist/*
