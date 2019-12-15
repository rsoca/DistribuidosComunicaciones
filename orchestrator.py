 #!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import re
import sys
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413


    
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
            return self.orchestrator.call_downloadTask(url)

    def getFileList(self, current=None):
        ''' getFileList '''
        if self.orchestrator:
            return self.orchestrator.obtener_lista_canciones()
    
        return []

    def announce(self, orchestrator, current=None):
        ''' Announce '''
        if self.orchestrator:
            self.orchestrator.nuevo_orchestrator(orchestrator)


class ManageOrchestrators():

    ''' Manage Orchestrators class '''

    qos = {}
    orchestrators_dict = {}
    files_update = {}
    file_list = []

    def __init__(self, broker, downloader_proxy, topic_update, topic_orchestrator):
        ''' Constructor '''
        self.adapter = broker.createObjectAdapter("OrchestratorAdapter")
        self.crear_orchestrator(broker, downloader_proxy, topic_update, topic_orchestrator)
        self.downloader = TrawlNet.DownloaderPrx.checkedCast(broker.stringToProxy(downloader_proxy))
        self.topic_orchestrator = topic_orchestrator
        self.file_topic = topic_update
        self.crear_orchestrator_event()
        self.crear_file_update_event()

    
    def crear_orchestrator(self, broker, downloader_proxy, topic_update, topic_orchestrator):
        ''' Crear orchestrator'''
        self.orchestrator = OrchestratorI()
        self.orchestrator.orchestrator = self
        self.proxy_orchestrator = self.adapter.addWithUUID(self.orchestrator)

    def crear_orchestrator_event(self):
        ''' Crear Orchestrator Event '''
        self.subscriptor = OrchestratorEventI()
        self.subscriptor.orchestrator = self
        self.proxy_subscriptor = self.adapter.addWithUUID(self.subscriptor)
        self.topic_orchestrator.subscribeAndGetPublisher(self.qos, self.proxy_subscriptor)
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.topic_orchestrator.getPublisher())

    def crear_file_update_event(self):
        ''' Crear FileUpdatesEventI '''
        self.file_updates = FileUpdatesEventI()
        self.file_updates.orchestrator = self
        self.file_updates_proxy = self.adapter.addWithUUID(self.file_updates)
        self.file_topic.subscribeAndGetPublisher(self.qos, self.file_updates_proxy)

    def call_downloadTask(self, url):
        ''' envio downloadTask '''
        return self.downloader.addDownloadTask(url)

    def decir_hola(self, orchestrator):
        ''' Decir hola a un orchestrator'''
        if orchestrator.ice_toString() in self.orchestrators_dict:
            return
        print("Hola! soy el orchestrator %s" % orchestrator.ice_toString())
        self.orchestrators_dict[orchestrator.ice_toString()] = orchestrator
        orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))

    def nuevo_orchestrator(self, orchestrator):
        if orchestrator.ice_toString() in self.orchestrators_dict:
            return
        print("Hola! yo soy %s" % orchestrator.ice_toString())
        self.orchestrators_dict[orchestrator.ice_toString()] = orchestrator

    def lanzar(self):
        ''' Activar adaptador y lanzar hello orchestrator '''
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.proxy_orchestrator))

    def obtener_lista_canciones(self):
        ''' Obtener lista '''
        for fhash in self.files_update:
            file_info_object = TrawlNet.FileInfo()
            file_info_object.hash = fhash
            file_info_object.name = self.files_update[fhash]
            self.file_list.append(file_info_object)
        return self.file_list

    def __str__(self):
        ''' to str '''
        return str(self.proxy_subscriptor)


class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Servidor
    '''
    def run(self, argv):
        '''
        Init
        '''
        key = 'IceStorm.TopicManager.Proxy'
        topic_name_file = "UpdateEvents"
        topic_name_orchestrator = "OrchestratorSync"
        broker = self.communicator()
        proxy = broker.propertyToProxy(key)
        if proxy is None:
            return None
        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101
        if not topic_mgr:
            return 2
     
        try:
            topic_update_event = topic_mgr.retrieve(topic_name_file)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic_update_event = topic_mgr.create(topic_name_file)

        try:
            topic_orchestrator_event = topic_mgr.retrieve(topic_name_orchestrator)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic_orchestrator_event = topic_mgr.create(topic_name_orchestrator)

        orchestrator = ManageOrchestrators(broker, argv[1], topic_update_event, topic_orchestrator_event)
        orchestrator.lanzar()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0


ORCHEST = Server()
sys.exit(ORCHEST.main(sys.argv))
