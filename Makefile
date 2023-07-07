
all: lint test validate

setup: setup_npm setup_python


setup_npm:
	npm install

lint:lint_markdown lint_python lint_cff

lint_markdown:
	find *.md | grep '\.md$$' \
		| xargs npx markdownlint --config ./.markdownlint.json

POETRY_NO_ROOT:= --no-root
setup_python:
	poetry install $(POETRY_OPTION)

lint_python: pyright black flake8 isort yamllint jsonlint pydocstyle

pyright:
	npx pyright

black:
	find ./src tests | grep py$$ | xargs black --diff | diff /dev/null -

flake8:
	find ./src tests | grep py$$ | xargs flake8

isort:
	find ./src tests | grep py$$ | xargs isort --diff | diff /dev/null -

yamllint:
	find . -name '*.yml' -type f | grep -v node_modules | xargs yamllint --no-warnings

jsonlint:
	python3 -c "import sys,json;print(json.dumps(\
	    json.loads(sys.stdin.read()),\
	    indent=4,ensure_ascii=False,sort_keys=True))" \
	< ./.markdownlint.json  | diff -q - ./.markdownlint.json

pydocstyle:
	pydocstyle ./src tests --ignore=D100,D101,D102,D103,D104,D105,D107,D203,D212,D400,D415

test_python:
	coverage run -m unittest discover tests

test_format:
	find data -name '*.jsonl' | xargs -n1 python -m src.check_data -i

test: test_python test_format

validate:
	python -m src.update_readme -i README.md --ref ./data/data.jsonl --validate

lint_cff:
	cffconvert --validate

.PHONY: all setup \
	flake8 black pyright isort jsonlint yamllint jsonlint pydocstyle\
	test_python \
	test_format test validate \
	validate_example validate_correctness_labeled lint_cff

