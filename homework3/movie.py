#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''My first server

Created by Junjie Li, 2014-11-13
Lasted modified by Junjie Li, 2014-11-13
Email: 28715062@qq.com

'''

import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

SP = os.path.join(os.path.dirname(__file__), "static")

class MovieHandler(tornado.web.RequestHandler):
    ''' A requesthandler
    to / and /movie.html'''
    def get(self):
        film = self.get_argument("film")
        reviews = []
        with open(os.path.join(SP, film, 'info.txt')) as info:
            kwargs = {
                "film": film,
                "name": info.readline().strip(),
                "year": info.readline().strip(),
                "score": info.readline().strip(),
                "review_num": info.readline().strip()
            }
        with open(os.path.join(SP, film, 'generaloverview.txt')) as general:
            lines = [line.strip().split(':') for line in general.readlines()]
            kwargs.update({"general": lines})
        for review in os.listdir(os.path.join(SP, film)):
            if review.startswith("review"):
                with open(os.path.join(SP, film, review)) as reviewfile:
                    reviews.append([line.strip() for line in reviewfile.readlines()])
        kwargs.update({"reviews": reviews})
        self.render('movie.html', **kwargs)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        autoescape=None,
        handlers=[(r'/movie.html', MovieHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
