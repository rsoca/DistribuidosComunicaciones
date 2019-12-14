#!/bin/sh
#

PYTHON=python3

CLIENT_CONFIG=serv.config

$PYTHON client.py --Ice.Config=$CLIENT_CONFIG "$1" "$2"
