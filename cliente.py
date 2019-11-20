#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class Cliente(Ice.Application):
    def main(self, current=None):
        
        print('// Bienvenido a la aplicacion para descargar musica de Youtube //')


    def run(self, argv):

        main()

        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)
        print(orchestrator.downloadTask(argv[2]))


        return 0

sys.exit(Cliente().main(sys.argv))
