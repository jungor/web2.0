#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''NerdLuv server

Created by Junjie Li, 2014-11-12
Lasted modified by Junjie Li, 2014-12-1
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
    def get(self):
        oldusername = self.get_argument('name', None)
        olduser = None
        if oldusername:
            with open(os.path.join(self.get_template_path(), 'singles.txt')) as data:
                singles = [Person.Person(*(line.strip().split(','))) for line in data.readlines()]
                for person in singles:
                    if person.name == oldusername:
                        olduser = person
                matches = [single for single in singles if single.ismatch(olduser) and single.rating(olduser) >= 3  and single.name != oldusername]
                images = os.listdir(os.path.join(os.path.dirname(__file__), "static", "images"))
                self.render('results.html', newuser=None, olduser=olduser, matches=matches, images=images)
        else:
            self.render('sorry.html', message='You did not provide valid name.')

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
        try:
            newuser = Person.Person(**kwargs)
        except ValueError, e:
            self.render('sorry.html', message=str(e))
        else:
            with open(os.path.join(self.get_template_path(), 'singles.txt'), 'a+') as data:
                singles = [Person.Person(*(line.strip().split(','))) for line in data.readlines()]
                names = [person.name for person in singles]
                if newuser.name in names:
                    self.render('sorry.html', message='The name has already been used.')
                else:
                    matches = [single for single in singles if single.ismatch(newuser) and single.rating(newuser) >= 3 and single.name != newuser.name]
                    data.writelines((str(newuser), '\n'))
                    images_path = os.path.join(os.path.dirname(__file__), "static", "images")
                    images = os.listdir(images_path)
                    photo = self.request.files['photo']
                    for meta in photo:
                        filename = newuser.photo
                        filepath = os.path.join(images_path, filename)
                        with open(filepath,'wb') as up:
                            up.write(meta['body'])
                    self.render('results.html', newuser=newuser, olduser=None, matches=matches, images=images)
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
