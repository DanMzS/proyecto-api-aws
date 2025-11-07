#!/usr/bin/env bash
set -euo pipefail
export FLASK_ENV=development
python3 -m pip install -r requirements.txt
python3 app.py