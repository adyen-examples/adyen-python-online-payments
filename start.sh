#!/usr/bin/env bash
FILE=config_example.ini
if test -f "$FILE"; then
    mv config_example.ini config.ini
fi
python3 -m venv venv
. venv/bin/activate
export FLASK_APP=app
export FLASK_ENV=development
python setup.py install
