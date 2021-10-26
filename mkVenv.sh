#!/bin/bash

[ -d venv ] || python3 -mvirtualenv -p python3 venv

venv/bin/pip install -U pip
venv/bin/pip install -U -r requirements.txt

