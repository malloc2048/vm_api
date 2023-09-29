#!/usr/bin/env bash

gunicorn -c api/gunicorn.conf.py api:app
