#!/usr/bin/make -f
# -*- mode:makefile -*-

run-server:
	$(MAKE) run-registry &
	sleep 1
	$(MAKE) run-icestorm &
	sleep 1
	$(MAKE) run-sender-factory &
	sleep 1
	$(MAKE) run-transfer-manager

run-registry:
	mkdir -p db/Registry 
	icegridregistry --Ice.Config=registry.config

run-icestorm:
	mkdir -p IceStorm/
	icebox --Ice.Config=icebox.config

run-sender-factory:
	./sender_factory.py --Ice.Config=senders.config files/

run-transfer-manager:
	./transfers_manager.py --Ice.Config=transfers.config

run-client: create-client-workspace
	./file_downloader.py --Ice.Config=client.config file1 file2

create-client-workspace:
	mkdir -p downloads/

clean:
	$(RM) -r downloads __pycache__ IceStorm Registry db