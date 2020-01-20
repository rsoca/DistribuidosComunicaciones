#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

''' Topics Icestorm class '''

import IceStorm

class Topics:
    '''
    Crear topics
    '''
    def __init__(self, broker):
        ''' Constructor '''
        self.topic_mgr = self.create_topic_manager(broker)
        self.topic_archivos = self.create_topic(self.topic_mgr, "UpdateEvents")
        self.topic_orchestrator = self.create_topic(self.topic_mgr, "OrchestratorSync")
    
    def create_topic_manager(self, broker):
        ''' Get topic manager mgr '''
        key = 'YoutubeDownloaderApp.IceStorm/TopicManager'
        proxy = broker.stringToProxy(key)
        if proxy is None:
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

    def create_topic(self, topic_mgr, name):
        ''' Get topic or create '''
        try:
            return topic_mgr.retrieve(name)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            return topic_mgr.create(name)

    def get_orch_topic(self):
        ''' Get orch '''
        return self.topic_orchestrator

    def get_file_topic(self):
        ''' Get File topic '''
        return self.topic_archivos

