#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Definicion Cliente
'''
import sys
import os
import binascii
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

DOWN_DIRECTORY = './downloads/'

class ReceiverI(TrawlNet.Receiver):

	def __init__(self, fileName, sender, transfer):
		self.fileName = fileName
		self.sender = sender
		self.transfer = transfer

	def start(self,current=None):
		print('Start the transmision of the file ', self.fileName)

		BLOCK_SIZE = 1024
		
		with open(os.path.join(DOWN_DIRECTORY, self.fileName), 'wb') as file:
			remote_EOF = False
			while not remote_EOF:
				data = self.sender.receive(BLOCK_SIZE)
				if len(data) > 1:
					data = data[1:]
				data = binascii.a2b_base64(data)
				remote_EOF = len(data) < BLOCK_SIZE
				if data:
					file.write(data)
			self.sender.close()

		print('Transmision finished!')

	def destroy(self, current):
		print('Destroy the receiver')
		current.adapter.remove(current.id)

class ReceiverFactoryI(TrawlNet.ReceiverFactory):

	def create(self, fileName, sender, transfer, current=None):
		print('Create the receiver factory')

		receiver = ReceiverI(fileName, sender, transfer)
		proxy_receiver = current.adapter.addWithUUID(receiver)
		obj_receiver = TrawlNet.ReceiverPrx.checkedCast(proxy_receiver)

		return obj_receiver


class Client(Ice.Application):

	def run(self, argv):
		#crear proxy del receiverFactory
		broker = self.communicator()
		client_servant = ReceiverFactoryI()
		rec_adapter = broker.createObjectAdapter('ReceiverAdapter')
		rec_proxy = rec_adapter.add(client_servant, broker.stringToIdentity('receiver1'))

		print('Proxy receiver: ', rec_proxy)
		rec_adapter.activate()

		proxy_transfer = self.communicator().propertyToProxy('Transfer.proxy')
		transfer = TrawlNet.TransferFactoryPrx.checkedCast(proxy_transfer)		

		proxy_receiver=broker.propertyToProxy('Receiver.proxy') 
		receiver=TrawlNet.ReceiverFactoryPrx.checkedCast(proxy_receiver)

		if not transfer:
			raise RuntimeError('Transfer proxy not correct')

		print ('Obtain the file list')
		file_list = []
		for i in range(1, len(sys.argv)):
			file_list.append(sys.argv[i])

		print('Create the transfer')
		nw_transfer = transfer.newTransfer(receiver)

		print('Create the peers')
		receivers_list = nw_transfer.createPeers(file_list)

		print('Start the transmissions')
		i = 0
		for i in range(len(receivers_list)):
			receivers_list[i].start()

		print('Transfers finished')

		return 0



sys.exit(Client().main(sys.argv))

