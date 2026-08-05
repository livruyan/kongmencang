# Makefile for LangChain & LangGraph Course
# Editor-agnostic: runs in the PyCharm / WebStorm terminal, VS Code, or CI.
# Requires Python 3.13+ and Node 22+.

PYTHON  ?= python3
VENV    ?= .venv
PIP     := $(VENV)/bin/pip
PY      := $(VENV)/bin/python

.PHONY: help setup install-py install-docs docs docs-dev docs-preview lint run clean deploy-docs

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
	@echo "  deploy-docs   Build docs then push main -> GitHub Actions deploys to Pages"
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

# 构建文档并推送 main；GitHub Actions 会自动部署到 GitHub Pages。
# 首次使用前需在仓库 Settings → Pages → Source 选择 "GitHub Actions"。
deploy-docs:
	npm run docs:build
	git push origin main
