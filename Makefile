.PHONY:install hooks clean

bold := $(shell tput bold)
red := $(shell tput setaf 1)
green := $(shell tput setaf 2)
blue := $(shell tput setaf 4)
reset := $(shell tput sgr0)

setup: install hooks
	@printf '${green}${bold}Sucessfully set up${reset} python-lomography!\n'

install:
	@printf '${green}${bold}Installing dependencies${reset}...\n'
	poetry install

hooks:
	@printf '${green}${bold}Setting up hooks${reset}...\n'
	poetry run pre-commit autoupdate
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg

clean:
	@printf '${red}${bold}Cleaning${reset}...\n'
	@printf '${red}Removing hooks${reset}...\n'
	rm .git/hooks/pre-commit
	rm .git/hooks/commit-msg