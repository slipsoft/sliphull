#!/bin/bash

if [ ! -f env/bin/activate ]; then virtualenv env; fi
. env/bin/activate
pip install -r requirements.txt