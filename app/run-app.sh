#!/bin/bash

cd /var/www/app/ && uvicorn main:app --host 0.0.0.0 --port 80 --reload
