PIP = pip3
TEST_DIR = tests
PRJ = brythoncli
PYTEST_FLAGS = -v


.PHONY: test
test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)

.PHONY: cover
cover:
	pytest $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)

.PHONY: lint
lint:
	pylama

.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

.PHONY: dist
dist:
	python setup.py sdist

