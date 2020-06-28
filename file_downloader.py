#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

'''
Definicion Cliente
'''
import sys
import os
import binascii
import Ice 
Ice.loadSlice('trawlnet.ice')
import TrawlNet
import IceStorm

DOWN_DIRECTORY = './downloads/'

class ReceiverI(TrawlNet.Receiver):

	def __init__(self, fileName, sender, transfer):#, peerEvent):
		self.fileName = fileName
		self.sender = sender
		self.transfer = transfer
		#self.peerEvent = peerEvent

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
		#peerInfo = TrawlNet.PeerInfo()
		#peerInfo.transfer = self.transfer
		#peerInfo.fileName = self.fileName
		#self.peerEvent.peerFinished(peerInfo)

		print('Transmision finished')

	def destroy(self, current):
		print('Destroy the receiver')
		current.adapter.remove(current.id)

class ReceiverFactoryI(TrawlNet.ReceiverFactory):

	#def __init__(self, peerEvent):
	#	self.peerEvent = peerEvent

	def create(self, fileName, sender, transfer, current=None):
		print('Create the receiver factory')

		receiver = ReceiverI(fileName, sender, transfer)#, self.peerEvent)
		proxy_receiver = current.adapter.addWithUUID(receiver)
		obj_receiver = TrawlNet.ReceiverPrx.checkedCast(proxy_receiver)

		return obj_receiver


class Client(Ice.Application):
	def get_topic_manager(self):
		key = 'IceStorm.TopicManager.Proxy'
		proxy = self.communicator().propertyToProxy(key)
		if proxy is None:
			print("Property '{}' not set".format(key))
		return None

		print("Using IceStorm in: '%s'" % key)
		return IceStorm.TopicManagerPrx.checkedCast(proxy)


	def run(self, argv):
		'''
		topic_mgr = self.get_topic_manager()

		topic_name = 'PeerEvent'
		try:
			topic = topic_mgr.retrieve(topic_name)
		except IceStorm.NoSuchTopic:
			print ('no such topic found, creating')
			topic = topic_mgr.create(topic_name)

		publisher = topic.getPublisher()
		peerEvent = TrawlNet.PeerEventPrx.uncheckedCast(publisher)
		'''
		#crear proxy del receiverFactory
		broker = self.communicator()
		client_servant = ReceiverFactoryI()#peerEvent)
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

		print('Client finished')

		return 0



sys.exit(Client().main(sys.argv))

