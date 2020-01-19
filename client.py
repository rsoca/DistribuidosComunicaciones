#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Cliente
'''
import sys
import os
import binascii
import Ice # pylint: disable=E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

DOWNLOADS_DIRECTORY = './'

def transfer_request(file_name, orchestrator):
    remote_EOF = False
    BLOCK_SIZE = 1024
    transfer = None
    try:
        transfer = orchestrator.getFile(file_name)
    except TrawlNet.TransferError as e:
        print(e.reason)
        return 1

    with open(os.path.join(DOWNLOADS_DIRECTORY, file_name), 'wb') as file_:
        remote_EOF = False
        while not remote_EOF:
            data = transfer.recv(BLOCK_SIZE)
            if len(data) > 1:
                data = data[1:]
            data = binascii.a2b_base64(data)
            remote_EOF = len(data) < BLOCK_SIZE
            if data:
                file_.write(data)
        transfer.close()

    transfer.destroy()
    print('Transfer finished!')

class Client(Ice.Application): # pylint: disable=R0903
    '''
    Clase cliente
    '''
    def __init__(self):
        print('Cliente iniciado\n\n')

    def run(self, argv):
        '''
        Iniciar cliente
        '''
        if(len(argv)==2):
            proxy = self.communicator().stringToProxy(argv[1])
        else:
            print(len(argv))
            proxy = self.communicator().stringToProxy(argv[3])

        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Invalid orchestrator proxy')

        if(len(argv)==2):
            print('Lista de canciones preparadas')
            print(orchestrator.getFileList())
            sys.exit
        elif(len(argv)==4):
            '''
            --download -> descargar
            --transfer -> obtener
            '''
            if argv[1] == '--download':
                orchestrator.downloadTask(argv[2])
            elif argv[1] == '--transfer':
                transfer_request(argv[2], orchestrator)
        else:
            ("Introduzca los argumentos correctamente")

        return 0

sys.exit(Client().main(sys.argv))
