#!/bin/sh
#

mkdir -p downloads/
./file_downloader.py --Ice.Config=client.config "$@"