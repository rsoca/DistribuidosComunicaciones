#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader Implementacion
'''

import sys
import hashlib
import os.path
import youtube_dl 
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

import utils as utilidades


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


def download_mp3(url, destination='./downloads/'):
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

def calculate_hash(filename):
    '''
    Crear hash
    '''
    file_hash = hashlib.md5()
    route = "./downloads/"+filename
    with open(route, "rb") as new_file:
        for chunk in iter(lambda: new_file.read(4096), b''):
            file_hash.update(chunk)
    return file_hash.hexdigest()


class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server
    '''
    def run(self, argv): # pylint: disable=W0613,W0221
        '''
        run ice class
        '''
        broker = self.communicator()
        properties = broker.getProperties()
        topic = utilidades.Topics(broker)
        factory = properties.getProperty("DownloaderFactoryIdentity")
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        publisher = TrawlNet.UpdateEventPrx.uncheckedCast(topic.get_file_topic().getPublisher())
        downloader = DownloaderFactoryI(publisher)
        
        proxy = adapter.add(downloader, broker.stringToIdentity(factory))
        print(proxy, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0


class DownloaderFactoryI(TrawlNet.DownloaderFactory):
    '''
    Downloader Factory I
    '''
    publisher = None

    def __init__(self, publisher):
        ''' Constructor de clase '''
        self.publisher = publisher

    def create(self, current):
        ''' metodo create '''
        downloader = DownloaderI(self.publisher)
        proxy_downlader = current.adapter.addWithUUID(downloader)
        return TrawlNet.DownloaderPrx.checkedCast(proxy_downlader)

class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    Downloader
    '''
    publisher = None

    def __init__(self, publisher):
        ''' Constructor de clase '''
        self.publisher = publisher

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Downloader
        '''
        try:
            file_to_download = download_mp3(url)
        except:
            raise TrawlNet.DownloadError()

        fileInfo = TrawlNet.FileInfo()
        fileInfo.name = os.path.basename(file_to_download)
        fileInfo.hash = calculate_hash(fileInfo.name)

        if self.publisher is not None:
            self.publisher.newFile(fileInfo)

        return fileInfo

SERVER_DOWN = Server()
sys.exit(SERVER_DOWN.main(sys.argv))
