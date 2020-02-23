FLASK_APP=app.py
FLASK_ENV=production

all: install
	gunicorn -c config.py wsgi:app

dev-server: 
	python3 -m flask run --no-debugger --no-reload

install:
	pip install -r requirements.txt

.PHONY: test
test: 
	env PYTHONPATH=. py.test --cov=./ .
