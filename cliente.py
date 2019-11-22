#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet

'''
Cliente
'''

class Cliente(Ice.Application):
    '''
    Client
    '''
    def run(self, argv):
        '''
        Run
        '''
        print('// Bienvenido a la aplicacion para descargar musica de Youtube //')
        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Proxy no valido')

        orchestrator.downloadTask(argv[2])
        return 0

sys.exit(Cliente().main(sys.argv))
