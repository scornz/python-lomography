.PHONY:install hooks clean

setup: install hooks

install:
	@echo "Installing dependencies..."
	poetry install

hooks:
	@echo "Setting up hooks.."
	poetry run pre-commit autoupdate
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg

clean:
	rm .git/hooks/pre-commit
	rm .git/hooks/commit-msg