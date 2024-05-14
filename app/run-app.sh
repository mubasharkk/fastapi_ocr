#!/bin/bash

cd /var/www/app/

python3 -m pip install -r ./requirements.txt

uvicorn main:app --host 0.0.0.0 --port 80 --reload --reload-dir ./
