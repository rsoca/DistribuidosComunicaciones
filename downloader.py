#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

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


class Downloader(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    DownloaderImplementacion
    '''
    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        addDownloadTask
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


class Server(Ice.Application):
    '''
    Server Downloader
    '''
    def run(self, argv):
        '''
        Iniciar server downloader Ice
        '''
        dw = Downloader()
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        downloader = adapter.add(dw, broker.stringToIdentity("downloader"))
        print(downloader, flush=True)
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
        Debug
        '''
        pass

    def warning(self, msg):
        '''
        Warning
        '''
        pass

    def error(self, msg):
        '''
        Error
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

SERVER = Server()
sys.exit(SERVER.main(sys.argv))
