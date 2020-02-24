#!/bin/sh

python3 -m venv test-venv
. test-venv/bin/activate
pip install coloredlogs attrs requests

./wait-for-hawkbit-online

./test_hawkbit.py

deactivate
