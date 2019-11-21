#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import TrawlNet

class Downloader(TrawlNet.Downloader):


    def addDownloadTask(self, url, current=None):
        print('Downloader -> url: \n',url)
        print('\n')
        print("Descargandooo")
        mensaje = "Descarga completa"
        return mensaje

    def __init__(self):
        print('Iniciando Downloader')


class Server(Ice.Application):


    def run(self, argv):

        dw = Downloader()

        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        downloader = adapter.add(dw, broker.stringToIdentity("downloader"))
        print(downloader, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
