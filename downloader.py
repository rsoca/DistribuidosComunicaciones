#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader: Servidor
'''

import sys
import hashlib
import os.path
import youtube_dl #pylint: disable=E0401
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    DownloaderImplementation
    '''
    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Add Download Task
        '''
        file = download_mp3(url)
        fileInfo = TrawlNet.FileInfo()
        fileInfo.name = os.path.basename(file)
        fileInfo.hash = file_hash(fileInfo.name)
        orchestrators = self.event_file.getPublisher()
        # Put exception
        event = TrawlNet.UpdateEventPrx.uncheckedCast(orchestrators)
        event.newFile(fileInfo)
        return fileInfo

    def __init__(self, event):
        self.event_file = event


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

def file_hash(filename):
    '''
    Hash files
    '''
    fileHash = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b''):
            fileHash.update(chunk)
    return fileHash.hexdigest()



class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server
    '''
    def run(self, argv): # pylint: disable=W0613
        '''
        Run Server
        '''
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            return None
        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy)
        if not topic_mgr:
            return 2

        topic_name = "UpdateEvents"
        try:
            topic_update = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic_update = topic_mgr.create(topic_name)

        downloader = DownloaderI(topic_update)
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy = adapter.add(downloader, broker.stringToIdentity("dwn"))
        print(proxy, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

DOWN = Server()
sys.exit(DOWN.main(sys.argv))
