.PHONY: docs

default: clean

clean:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	rm -rf dist/ build/ .pytest_cache/

format:
	isort src/wagtail_live tests setup.py
	black src/wagtail_live tests setup.py
	flake8 src/wagtail_live tests setup.py

lint:
	isort --check-only --diff src/wagtail_live tests setup.py
	black --check --diff src/wagtail_live tests setup.py
	flake8 src/wagtail_live tests setup.py

test:
	pytest --cov wagtail_live

docs:
	mkdocs serve -a 127.0.0.1:8080

release:
	./make_release.sh
