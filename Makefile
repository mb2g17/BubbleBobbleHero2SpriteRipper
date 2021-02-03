all: setup

setup:
	pipenv install

run:
	cd bbh2sr; \
	pipenv run python .

clean:
	pipenv --rm

check:
	pipenv run python -m unittest discover -v