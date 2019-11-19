#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import sys
import Ice
import TrawlNet
Ice.loadSlice('trawlnet.ice')


class Server(Ice.Application):
    def run(self, argv):
	if len(argv) < 2: 
		print('ERROR: Proporcionar un Downloader()')
		return 1
     broker = self.communicator()

        proxy_downloader = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(proxy_downloader)
        if not downloader:
            raise RuntimeError('Proxy no encontrado')

        servidor = Orchestrator(downloader)

        adapter = broker.createObjectAdapter('OrchestratorAdapter')
        proxy = adapter.add(servidor, broker.stringToIdentity('orchestrator'))
        print('Conectando a orquestador ',proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))
