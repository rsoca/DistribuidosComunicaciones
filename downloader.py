#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

'''
Downloader
'''

import youtube_dl
import os.path
import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet

class Downloader(TrawlNet.Downloader):
    '''
    DownloaderI
    '''
    def addDownloadTask(self, url, current=None):
        '''
        addDownloadTask
        '''
        print('Downloader -> url: \n',url)
        print("Descargando.....")
        return download_mp3(url)

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


def download_mp3(url, destination='./music/'):
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
