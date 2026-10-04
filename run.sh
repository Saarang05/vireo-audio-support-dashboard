#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python analyze.py --data-dir data --out-dir outputs
streamlit run app.py
