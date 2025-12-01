#!make
install:
	pip3 install -e .

remove:
	pip3 uninstall image_sitemap -y

lint:
	pip install .[style]
	black src/ --check
	isort src/ --check-only
	autoflake --in-place --recursive src/ --check-diff

refactor:
	pip install .[style]
	autoflake --in-place \
				--recursive \
				--remove-unused-variables \
				--remove-duplicate-keys \
				--remove-all-unused-imports \
				--ignore-init-module-imports \
				src/
	black src/
	isort src/

build:
	pip3 install --upgrade build setuptools
	python3 -m build

upload:
	pip3 install wheel setuptools build
	pip3 install twine==6.1.0
	twine upload dist/*

# Testing commands
test:
	coverage run --rcfile=.coveragerc -m pytest --verbose --showlocals --disable-warnings && \
    coverage report --format=markdown --precision=3 --sort=cover --skip-empty --show-missing > ./coverage/coverage.md && \
    coverage html --precision=3 --skip-empty -d ./coverage/html/
