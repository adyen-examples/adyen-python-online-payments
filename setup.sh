#!/usr/bin/env bash
FILE=config.ini
if [[ ! -f $FILE ]] 
then
    cp config_example.ini config.ini
fi
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt