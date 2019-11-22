#!/bin/sh

./downloader.py --Ice.Config=serv_downloader.config | tee down.out &
sleep 4
./orchestrator.py --Ice.Config=serv_orch.config "$(head -1 down.out)"
