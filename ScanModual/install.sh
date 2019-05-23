#!/bin/bash
if test -e /usr/bin/pip -o -e /usr/local/bin/pip
then
	pip install -r requirements.txt
else
	apt-get install python-pip
fi

