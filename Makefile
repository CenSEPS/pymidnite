VENV=venv
NOSE=$(VENV)/bin/nose2
LINT=$(VENV)/bin/flake8

.PHONY: test

all: $(VENV)


$(VENV):
	virtualenv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

test:
	$(LINT) tests midnite
	$(NOSE) -v
