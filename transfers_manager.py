#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

'''
Implementacion Transfer Manager
'''

import os
import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet
import IceStorm

class PeerEventI(TrawlNet.PeerEvent):

	def peerFinished(self, peerInfo, current = None):
		print('The peer is finished!')
		peerInfo.transfer.destroyPeer(peerInfo.fileName)

class TransferI(TrawlNet.Transfer):

	def __init__(self, senderFactory, receiverFactory, current=None):
		self.senderFactory = senderFactory
		self.receiverFactory = receiverFactory
		self.proxy_transfer = None
		self.dic = {}

	def createPeers(self, files, current=None):
		print('Create the peers')
		ReceiversList = []
		i=0
		for i in range(len(files)):
			fileName = files[i]
			sender = self.senderFactory.create(fileName)
			receiver = self.receiverFactory.create(fileName, sender, self.proxy_transfer )
			ReceiversList.append(receiver)
			self.dic[fileName] = [sender,receiver]

		return ReceiversList

	def destroyPeer(self, peerId, current=None):
		print('Destroy the peer')
		value_sender=self.dic[peerId][0]
		value_sender.destroy()
		value_receiver = self.dic[peerId][1]
		value_receiver.destroy()
		diccionary.pop(peerId)

	def destroy(self, current):
		print('Destroy the transfer conexion')
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

	def get_topic_manager(self):
		key = 'IceStorm.TopicManager.Proxy'
		proxy = self.communicator().propertyToProxy(key)
		if proxy is None:
			print("Property '{}' not set".format(key))
			return None
		print("Using IceStorm in: '%s'" % key)
		return IceStorm.TopicManagerPrx.checkedCast(proxy)

	def run(self, argv):

		topic_mgr = self.get_topic_manager()
		if not topic_mgr:
			print (': invalid proxy')
			return 2

		servant_peer = PeerEventI()
		adapter_peer =self.communicator().createObjectAdapter('PeerAdapter')
		subscriber = adapter_peer.addWithUUID(servant_peer)
		topic_name = 'PeerEvent'
		qos = {}
		try:
			topic = topic_mgr.retrieve(topic_name)
		except IceStorm.NoSuchTopic:
			topic = topic_mgr.create(topic_name)

		topic.subscribeAndGetPublisher(qos, subscriber)

		adapter_peer.activate()

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

		topic.unsubscribe(subscriber)

		return 0


server = Server()
sys.exit(server.main(sys.argv))
