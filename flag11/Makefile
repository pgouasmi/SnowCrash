SOURCE_FILE = script.py

all: deps script

deps:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

script:
	./venv/bin/python3 $(SOURCE_FILE)

clean:
	rm -rf venv

re: clean all

.PHONY: all deps script clean re