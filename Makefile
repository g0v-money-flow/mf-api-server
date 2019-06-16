all: install
	python3 app.py

install:
	pip install -r requirements.txt

.PHONY: test
test: 
	env PYTHONPATH=. py.test --cov=./ .
