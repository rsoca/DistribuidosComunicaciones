#!/usr/bin/env python3
# -*- coding: utf-8; -*-
'''
Implementacion Client.py
'''

import sys
import Ice # pylint: disable=E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class Client(Ice.Application):
    '''
    Clase Client
    '''
    lista = None

    def __init__(self):
        self.lista = []

    def run(self, argv):
        ''' Run '''
        print('Bienvenido a la App de Descarga de Musica')
        proxy = self.communicator().stringToProxy(argv[1])
        orchest = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchest:
            raise RuntimeError("Invalid proxy")

        if(len(argv)==2):
            self.lista = orchest.getFileList()
            print(self.lista)
            sys.exit
        elif(len(argv)>=3):
            respuesta = orchest.downloadTask(argv[2])
            print(respuesta)


sys.exit(Client().main(sys.argv))
