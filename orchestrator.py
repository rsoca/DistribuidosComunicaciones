#!/usr/bin/env python3
# -*- coding: utf-8; -*-

'''
Orchestrator
'''

import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet

class Orchestrator(TrawlNet.Orchestrator):
    '''
    OrchestratorI
    '''

    def downloadTask(self, url, current=None):
        '''
            Downloader
        '''
        return self.downloader.addDownloadTask(url)

    def __init__(self, downloader):
        '''
            Constructor o builder
        '''
        self.downloader = downloader

class Server(Ice.Application):

    '''
    Server orchestrator
    '''
    def run(self, argv):

        '''
        Iniciar server orchestrator
        '''
        broker = self.communicator()
        proxy_downloader = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(proxy_downloader)
        if not downloader:
            raise RuntimeError('No esta instanciado el downlader')
        servidor = Orchestrator(downloader)
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        proxy = adapter.add(servidor, broker.stringToIdentity("orchestrator"))
        print("Conexion a orquestador :",proxy)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

ORCHESTRADOR = Server()
sys.exit(ORCHESTRADOR.main(sys.argv))
