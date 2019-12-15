#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader Implementation
'''

import sys
import os.path
import youtube_dl #pylint: disable=E0401
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    DownloaderI
    '''
    publicador = None
    
    def __init__(self, publicador):
        '''
        Constructor
        '''
        self.publicador = publicador

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        addDownloadTask
        '''
        try:
            archivo = download_mp3(url)
        except:
            raise TrawlNet.DownloadError("Error en la descarga del video")

        file_objet = TrawlNet.FileInfo()
        file_objet.name = os.path.basename(archivo)
        file_objet.hash = url_hash(url)

        if self.publicador is not None:
            self.publicador.newFile(file_objet)
            
        return file_objet

def url_hash(url):
    '''
    Create hash from url youtube
    '''
    with youtube_dl.YoutubeDL(_YOUTUBEDL_OPTS_) as ytb:
        info_dict = ytb.extract_info(url, download=False)
    return info_dict['id']


class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server
    '''

    def run(self, argv): # pylint: disable=W0613,W0221
        '''
        run server
        '''
        self.key = 'IceStorm.TopicManager.Proxy'
        self.topic_name = "UpdateEvents"
        broker = self.communicator()
        self.proxy_icestorm = broker.propertyToProxy(self.key)

        if self.proxy_icestorm is None:
            print("Proxy no valido")
            return None

        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(self.proxy_icestorm) # pylint: disable=E1101

        if not topic_mgr:
            print("Topic mgr no valido")
            return 2
        try:
            file_event = topic_mgr.retrieve(self.topic_name)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            file_event = topic_mgr.create(self.topic_name)
        
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        publicador = file_event.getPublisher()
        downloader = DownloaderI(TrawlNet.UpdateEventPrx.uncheckedCast(publicador)) 
        proxy_downloader = adapter.add(downloader, broker.stringToIdentity("downloader"))
        print(proxy_downloader, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0


class NullLogger:
    '''
    NullLogger
    '''
    def debug(self, msg):
        '''
        debug method
        '''
        pass

    def warning(self, msg):
        '''
        warning method
        '''
        pass

    def error(self, msg):
        '''
        error method
        '''
        pass

_YOUTUBEDL_OPTS_ = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}


def download_mp3(url, destination='./'):
    '''
    Synchronous download from YouTube
    '''
    options = {}
    task_status = {}

    def progress_hook(status):
        '''
        progress hook
        '''
        task_status.update(status)
    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')

    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([url])
    filename = task_status['filename']
    filename = filename[:filename.rindex('.') + 1]
    return filename + options['postprocessors'][0]['preferredcodec']


    
DOWNLOADER = Server()
sys.exit(DOWNLOADER.main(sys.argv))
