#!/usr/bin/env bash
# simple run script
set -e
source .venv/bin/activate || true
export FLASK_APP=app.py
python app.py --demo
