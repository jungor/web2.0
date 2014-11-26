#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''NerdLuv server

Created by Junjie Li, 2014-11-12
Lasted modified by Junjie Li, 2014-11-12
Email: 28715062@qq.com

'''

import os

import Person

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    ''' A requesthandler
    to / '''
    def get(self):
        self.render("index.html")

class SignupHandler(tornado.web.RequestHandler):
    ''' A requesthandler
    to /signup '''
    def post(self):
        kwargs = {
            'name': self.get_argument('name', None),
            'gender': self.get_argument('gender', None),
            'age': self.get_argument('age', None),
            'personality': self.get_argument('personality', None),
            'system': self.get_argument('system', None),
            'seeking': self.get_arguments('seeking[]'),
            'lowerbound': self.get_argument('lowerbound', None),
            'upperbound': self.get_argument('upperbound', None)
        }
        with open(os.path.join(self.get_template_path(), 'singles.txt')) as data:
            singles = [Person.Person(*(line.strip().split(','))) for line in data.readlines()]
        try:
            signuper = Person.Person(**kwargs)
        except ValueError, e:
            self.render('sorry.html', message=str(e))
        else:
            # print signuper
            # for single in singles:
            #     print single.__dict__
            matches = [single for single in singles if single.ismatch(signuper) and single.rating(signuper) >= 3]
            self.render('results.html', signuper=signuper, matches=matches)
        finally:
            pass

if __name__ == '__main__':
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/signup', SignupHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
