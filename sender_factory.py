#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

'''
Implementacion Sender Factory
'''

import os
import sys
import Ice
import IceStorm
import binascii
import IceGrid
Ice.loadSlice('trawlnet.ice')
import TrawlNet

ROOTS = './'
DIRECTORY= sys.argv[2]
READ_DIRECTORY = os.path.join(ROOTS, DIRECTORY)

class SenderI(TrawlNet.Sender):

	def __init__(self, file_path):
		self.file = open(file_path, 'rb')

	def receive(self, size, current=None):
		return str(binascii.b2a_base64(self.file.read(size), newline=False))

	def close(self, current=None):
		print('Close the transmission')
		self.file.close()

	def destroy(self, current=None):
		print('Destroy the sender conexion')
		current.adapter.remove(current.id)

class SenderFactoryI(TrawlNet.SenderFactory):

	def create (self, fileName, current=None):
		file_path = os.path.join(READ_DIRECTORY, fileName)
		if not os.path.exists(file_path):
			raise TrawlNet.FileDoesNotExistError ('The file {} not exist'.format(fileName))

		servant = SenderI(file_path)
		proxy = current.adapter.addWithUUID(servant)
		obj_sender = TrawlNet.SenderPrx.checkedCast(proxy)
		return obj_sender

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
		broker = self.communicator()
		sender_servant = SenderFactoryI()
		adapter = broker.createObjectAdapter('SenderAdapter')
		sender_proxy = adapter.add(sender_servant, broker.stringToIdentity('sender1'))
		print('The sender proxy is:')
		print(sender_proxy, flush=True)

		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0


SENDER = Server()
sys.exit(SENDER.main(sys.argv))
