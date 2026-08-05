# Makefile for LangChain & LangGraph Course
# Editor-agnostic: runs in the PyCharm / WebStorm terminal, VS Code, or CI.
# Requires Python 3.13+ and Node 22+.

PYTHON  ?= python3
VENV    ?= .venv
PIP     := $(VENV)/bin/pip
PY      := $(VENV)/bin/python

.PHONY: help setup install-py install-docs docs docs-dev docs-preview lint run clean

help:
	@echo "Targets:"
	@echo "  setup         Create venv, install Python + Node deps, copy .env"
	@echo "  install-py    python -m venv + pip install -r requirements.txt"
	@echo "  install-docs  npm install (VitePress)"
	@echo "  docs          Build static docs site -> docs/.vitepress/dist"
	@echo "  docs-dev      Live preview at http://localhost:5173"
	@echo "  docs-preview  Preview the built site"
	@echo "  lint          py_compile all examples"
	@echo "  run p=N       Run Phase N hello example (e.g. make run p=1)"
	@echo "  clean         Remove venv, node_modules and build cache"

setup: install-py install-docs
	cp -n .env.example .env || true
	@echo "Done. Edit .env to choose LLM_PROVIDER (openai / deepseek / ollama)."

install-py:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

install-docs:
	npm install

docs:
	npm run docs:build

docs-dev:
	npm run docs:dev

docs-preview:
	npm run docs:preview

lint:
	$(PYTHON) -m py_compile $$(find examples -name '*.py')

run:
	$(PY) -m examples.p$(p).hello_chain

clean:
	rm -rf $(VENV) node_modules docs/.vitepress/dist docs/.vitepress/cache
