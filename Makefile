all: setup

setup: ## Installs Pipenv environment
	pipenv install

run: ## Runs project with installed Pipenv environment
	cd bbh2sr; \
	pipenv run python .

package: ## Packages into an executable
	cd bbh2sr; \
	pipenv run pyinstaller --onefile --windowed --icon=assets/fire.ico --name=BBH2SR __main__.py
	cp -r ./bbh2sr/assets ./bbh2sr/dist/assets
	mv ./bbh2sr/dist ./dist
	rm -r ./bbh2sr/build
	rm ./bbh2sr/BBH2SR.spec
	@printf "Successfully packaged in 'dist' folder.\n"

clean: ## Uninstalls Pipenv environment
	pipenv --rm

check: ## Runs test cases in Pipenv environment
	pipenv run python -m unittest discover -v

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)