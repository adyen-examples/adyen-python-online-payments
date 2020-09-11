#!/usr/bin/env bash
FILE=config_example.ini
if test -f "$FILE"; then
    cp config_example.ini config.ini
fi
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
