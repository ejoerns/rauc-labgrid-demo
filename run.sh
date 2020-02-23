#!/bin/sh

python3 -m venv test-venv
. test-venv/bin/activate
pip install coloredlogs

./test_hawkbit.py

deactivate
