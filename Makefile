all: setup

setup:
	pipenv install

run:
	cd bbh2sr; \
	pipenv run python .

clean:
	pipenv --rm

check:
	@echo tests unimplemented