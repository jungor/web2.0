#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''My first server

Created by Junjie Li, 2014-11-6
Lasted modified by Junjie Li, 2014-11-9
Email: 28715062@qq.com

'''

import os

import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

SONGSDIR = os.path.join(os.path.dirname(__file__), "static", "songs")
FILES = os.listdir(SONGSDIR)
SONGS = [filename for filename in FILES if filename.find(".mp3") >= 0]
PLAYLISTS = [filename for filename in FILES if filename.find(".m3u") >= 0]

class MusicHandler(tornado.web.RequestHandler):
    ''' A requesthandler
    to / and /music.html'''
    def get(self):
        __is_playlist = False
        __playlist = self.get_argument('playlist', 'none')
        __shuffle = self.get_argument('shuffle', 'off')
        __by_size = self.get_argument('bysize', 'off')
        __songs = SONGS
        __playlists = PLAYLISTS
        __lines = []
        if __playlist != 'none':
            __is_playlist = True
            __playlists = []
            with open(os.path.join(SONGSDIR, __playlist)) as playfile:
                __lines = playfile.readlines()
                __lines = [str.strip(line) for line in __lines]
            __songs = [line for line in __lines if line.find('#') < 0]
        if '' in __songs:
            __songs.remove('')
        if __shuffle == 'on':
            random.shuffle(__songs)
        else:
            __songs.sort()
        if __by_size == 'on':
            def mycmp(left, right):
                '''My cmp
                use to sort'''
                return cmp(os.path.getsize(os.path.join(SONGSDIR, left)),
                           os.path.getsize(os.path.join(SONGSDIR, right)))
            __songs.sort(mycmp)
        __sizes = [os.path.getsize(os.path.join(SONGSDIR, i)) for i in __songs]
        __paths = [os.path.join(SONGSDIR, i) for i in __songs]
        self.render('music.html',
                    is_playlist=__is_playlist,
                    shuffle=__shuffle,
                    bysize=__by_size,
                    songs=__songs,
                    sizes=__sizes,
                    paths=__paths,
                    playlist=__playlist,
                    playlists=__playlists)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/', MusicHandler), (r'/music.html', MusicHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static")
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
