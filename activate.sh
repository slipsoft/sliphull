#!/bin/bash

if [ ! -f env/bin/activate ]
then
	pip install --user --ignore-installed virtualenv
	virtualenv env --python=python3
fi
. env/bin/activate
pip install -r requirements.txt