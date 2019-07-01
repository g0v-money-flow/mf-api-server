FLASK_APP=app.py
FLASK_ENV=production

all: install
	python3.7 -m flask run --no-debugger --no-reload

install:
	python3.7 -m pip install -r requirements.txt

.PHONY: test
test: 
	env PYTHONPATH=. py.test --cov=./ .
