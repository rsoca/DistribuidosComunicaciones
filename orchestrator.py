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

class Server(Ice.Application):   #pylint: disable=R0903

    '''
    Servidor
    '''
    files = {}
    def run(self, argv):

        '''
        Iniciar server orchestrator
        '''
        key = "IceStorm.TopicManager.Proxy"
        topic_name = "UpdateEvents"
        topic_orchestrator = "OrchestratorSync"
        qos_orch = {}
        qos = {}
        proxy = self.communicator().propertyToProxy(key)
        print("Using IceStorm in '%s'" % key)

        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(proxy)
        if not downloader:
            raise RuntimeError('No esta instanciado el downlader')

        servidor = Orchestrator(downloader)
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        
        proxy_orchestrator = adapter.add(orchestrator, broker.stringToIdentity("orchestrator"))
        orchestrator.setTopicandDownloader(downloader_instance, topicorch, proxy_orchestrator)
        print(proxy_orchestrator)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

ORCHESTRADOR = Server()
sys.exit(ORCHESTRADOR.main(sys.argv))
