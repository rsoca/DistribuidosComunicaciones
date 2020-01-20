#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Transfer Factory
'''

import os
import sys
import binascii
import Ice
import IceGrid # pylint : disable=W0611
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413


APP_DIRECTORY = './'
DOWNLOADS_DIRECTORY = os.path.join(APP_DIRECTORY, 'downloads')


class TransferI(TrawlNet.Transfer):
    ''' TransferI '''
    def __init__(self, file_path):
        ''' Constructor '''
        self.file_ = open(file_path, 'rb')

    def recv(self, size, current):
        ''' Recv '''
        return str(binascii.b2a_base64(self.file_.read(size), newline=False))

    def close(self, current):
        ''' Close '''
        self.file_.close()

    def destroy(self, current):
        ''' Destroy '''
        try:
            current.adapter.remove(current.id)
            print('TRASFER DESTROYED', flush=True)
        except Exception as e:
            print(e, flush=True)


class TransferFactoryI(TrawlNet.TransferFactory):
    ''' TransferFactory I '''
    def create(self, file_name, current):
        ''' Create '''
        file_path = os.path.join(DOWNLOADS_DIRECTORY, file_name)
        servant = TransferI(file_path)
        proxy = current.adapter.addWithUUID(servant)
        print('# New transfer for {} #'.format(file_path), flush=True)

        return TrawlNet.TransferPrx.checkedCast(proxy)


class Server(Ice.Application):
    '''
    Server
    '''
    def run(self, args):
        '''
        run 
        '''
        broker = self.communicator()
        properties = broker.getProperties()

        servant = TransferFactoryI()
        adapter = broker.createObjectAdapter('TransferAdapter')
        factory_id = properties.getProperty('TransferFactoryIdentity')
        proxy = adapter.add(servant, broker.stringToIdentity(factory_id))

        print('{}'.format(proxy), flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    SERVER = Server()
    exit_status = SERVER.main(sys.argv)
    sys.exit(exit_status)

