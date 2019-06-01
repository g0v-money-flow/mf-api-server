

.PHONY: test
test: 
	env PYTHONPATH=. py.test --cov=./ .
