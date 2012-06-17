#!/bin/bash

DJANGO_SETTINGS_MODULE=django_hello_world.settings; export DJANGO_SETTINGS_MODULE
PYTHONPATH=`pwd`; export PYTHONPATH
OUTFILE=`date +%Y-%m-%d`.dat
COMMAND=modelcount
ADMIN=django-admin.py

$ADMIN $COMMAND 2>$OUTFILE
