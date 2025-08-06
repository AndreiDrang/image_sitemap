#!make
install:
	pip3 install -e .

remove:
	pip3 uninstall image_sitemap -y

lint:
	black src/ --check
	isort src/ --check-only
	autoflake --in-place --recursive src/ --check-diff

refactor:
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
