#!make

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
