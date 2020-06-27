#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Implementacion Transfer Manager
'''

import os
import sys
import Ice
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet

class TransferI(TrawlNet.Transfer):

	def __init__(self, senderFactory, receiverFactory, current=None):
		self.senderFactory = senderFactory
		self.receiverFactory = receiverFactory
		self.proxy_transfer = None

	def createPeers(self, files, current=None):
		print('Create the peers')
		ReceiversList = []
		i=0
		for i in range(len(files)):
			fileName = files[i]
			sender = self.senderFactory.create(fileName)
			receiver = self.receiverFactory.create(fileName, sender, self.proxy_transfer )
			ReceiversList.append(receiver)

		return ReceiversList

	def destroyPeer(self, peerId, current=None):
		print('Destroy the peer')

	def destroy(self, current):
		print('Destroy the conexion')
		current.adapter.remove(current.id)
		

class TransferFactoryI(TrawlNet.TransferFactory):

	def __init__(self, sender, current = None):
		self.sender = sender

	def newTransfer(self, receiverFactory, current=None):
		transfer = TransferI(self.sender, receiverFactory)
		proxy_transfer = current.adapter.addWithUUID(transfer)
		obj_transfer = TrawlNet.TransferPrx.checkedCast(proxy_transfer) 
		transfer.proxy_transfer = obj_transfer

		return obj_transfer

class Server(Ice.Application):

	def run(self, argv):

		broker = self.communicator()
		proxy_sender=broker.propertyToProxy('Sender.proxy')
		sender=TrawlNet.SenderFactoryPrx.checkedCast(proxy_sender)
		
		if not sender:
			raise RuntimeError('Sender proxy not run')

		servant = TransferFactoryI (sender)
		adapter = broker.createObjectAdapter('TransferAdapter')
		proxy = adapter.add(servant, broker.stringToIdentity('transfer1'))
		
		print('The transfer proxy is:')
		print(proxy, flush=True)

		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0


server = Server()
sys.exit(server.main(sys.argv))
