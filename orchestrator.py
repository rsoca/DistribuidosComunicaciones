#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import sys
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

import utils as utilidades

class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Servidor
    '''
    def run(self, argv):
        ''' Init '''
        broker = self.communicator()
        topics = utilidades.Topics(broker)
        orchestrator = InitOrchestrators(broker, topics.get_file_topic(), topics.get_orch_topic())
        orchestrator.comenzar()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    '''
    OrchestratorEventI
    '''
    orchestrator = None

    def hello(self, orchestrator, current=None):
        ''' Saludo '''
        if self.orchestrator:
            self.orchestrator.decir_hola(orchestrator)

class FileUpdatesEventI(TrawlNet.UpdateEvent):
    '''
    FileUpdatesEventI
    '''
    orchestrator = None

    def newFile(self, file_info, current=None):
        '''newFile'''
        if self.orchestrator:
            file_hash = file_info.hash
            if file_hash not in self.orchestrator.files_update:
                print(file_info.name)
                print(file_info.hash)
                self.orchestrator.files_update[file_hash] = file_info.name


class OrchestratorI(TrawlNet.Orchestrator):
    '''
    OrchestratorI
    '''
    orchestrator = None

    def downloadTask(self, url, current=None):
        ''' downloadTask '''
        if self.orchestrator:
            return self.orchestrator.enviar_downloadTask(url)

    def getFile(self, name, current=None):
        ''' Get File Transfer'''
        if self.orchestrator:
            return self.orchestrator.get(name)

    def getFileList(self, current=None):
        ''' getFileList '''
        if self.orchestrator:
            return self.orchestrator.obtener_lista_canciones()
        return []

    def announce(self, orchestrator, current=None):
        ''' Announce '''
        if self.orchestrator:
            self.orchestrator.nuevo_orchestrator(orchestrator)


class InitOrchestrators():
    ''' Manage Orchestrators class '''

    orchestrators_dict = {}
    files_update = {}

    def __init__(self, broker,  topic_update, topic_orchestrator):
        ''' Constructor '''
        self.adapter = broker.createObjectAdapter("OrchestratorAdapter")
        downloader_factory = TrawlNet.DownloaderFactoryPrx.checkedCast(broker.propertyToProxy("DownloaderFactoryIdentity"))
        self.downloader = downloader_factory.create()
        self.transfer_factory = TrawlNet.TransferFactoryPrx.checkedCast(broker.propertyToProxy("TransferFactoryIdentity"))
        self.crear_orchestrator(broker, topic_update, topic_orchestrator)
        self.topic_orchestrator = topic_orchestrator
        self.file_topic = topic_update
        self.crear_orchestrator_event()
        self.crear_file_update_event()

    def crear_orchestrator(self, broker, topic_update, topic_orchestrator):
        ''' Crear orchestrator'''
        self.orchestrator = OrchestratorI()
        self.orchestrator.orchestrator = self
        identidad = broker.getProperties().getProperty("Identity")
        self.proxy = self.adapter.add(self.orchestrator, broker.stringToIdentity(identidad))
        self.proxy_orchestrator = self.adapter.createDirectProxy(self.proxy.ice_getIdentity())

    def crear_orchestrator_event(self):
        ''' Crear Orchestrator Event '''
        self.subscriptor = OrchestratorEventI()
        self.subscriptor.orchestrator = self
        self.proxy_event = self.adapter.addWithUUID(self.subscriptor)
        identidad = self.proxy_event.ice_getIdentity()
        self.proxy_subscriptor = self.adapter.createDirectProxy(identidad)
        self.topic_orchestrator.subscribeAndGetPublisher({}, self.proxy_subscriptor)
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.topic_orchestrator.getPublisher())

    def crear_file_update_event(self):
        ''' Crear FileUpdatesEventI '''
        self.file_updates = FileUpdatesEventI()
        self.file_updates.orchestrator = self
        self.file_proxy = self.adapter.addWithUUID(self.file_updates)
        identidad = self.file_proxy.ice_getIdentity()
        self.updates_proxy = self.adapter.createDirectProxy(identidad)
        self.file_topic.subscribeAndGetPublisher({}, self.updates_proxy)

    def enviar_downloadTask(self, url):
        ''' envio downloadTask '''
        return self.downloader.addDownloadTask(url)

    def decir_hola(self, orchestrator):
        ''' Decir hola a un orchestrator'''
        if orchestrator.ice_toString() in self.orchestrators_dict:
            return
        print("Hola! soy %s" % orchestrator.ice_toString())
        self.orchestrators_dict[orchestrator.ice_toString()] = orchestrator
        orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))

    def nuevo_orchestrator(self, orchestrator):
        ''' Nuevo orchestrator '''
        if orchestrator.ice_toString() in self.orchestrators_dict:
            return
        print("Hola!! yo soy %s" % orchestrator.ice_toString())
        self.orchestrators_dict[orchestrator.ice_toString()] = orchestrator

    def get(self, name):
        ''' get file'''
        return self.transfer_factory.create(name)

    def obtener_lista_canciones(self):
        ''' Obtener lista '''
        file_list = []
        for fhash in self.files_update:
            file_info_object = TrawlNet.FileInfo()
            file_info_object.hash = fhash
            file_info_object.name = self.files_update[fhash]
            file_list.append(file_info_object)
        return file_list

    def comenzar(self):
        ''' Activar adaptador y lanzar hello orchestrator '''
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))



ORCHEST = Server()
sys.exit(ORCHEST.main(sys.argv))
