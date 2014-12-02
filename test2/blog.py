#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Blog server

Created by Junjie Li, 2014-12-2
Lasted modified by Junjie Li, 2014-12-2
Email: 28715062@qq.com

'''

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os
import files
import time

from tornado.options import define, options
define('port', default=8888, help='run on the given port', type=int)

class BaseHandler(tornado.web.RequestHandler):
    '''docstring for BaseHandler'''
    def get_current_user(self):
        return self.get_secure_cookie('username')

class LoginHandler(BaseHandler):
    '''docstring for LoginHandler'''
    def get(self):
        self.render('login.html')
    def post(self):
        name = self.get_argument('username', None)
        psw = self.get_argument('password', None)
        userList = files.getUsers()
        user = ','.join([name, psw])
        if user in userList:
            self.set_secure_cookie('username', name)
            print 'set!\nredirect...'
            self.redirect('/')


class IndexHandler(BaseHandler):
    '''docstring for IndexHandler'''
    @tornado.web.authenticated
    def get(self):
        blog = files.getBlog()
        self.render('index.html', blog=files.getBlog(), comments=files.getComments())

    @tornado.web.authenticated
    def post(self):
        comment = '|'.join([self.get_current_user(), time.strftime('%Y-%m-%d',time.localtime(time.time())), self.get_argument('comment'), ''])
        files.addComment(comment)
        blog = files.getBlog()
        self.render('index.html', blog=files.getBlog(), comments=files.getComments())

class LogoutHandler(BaseHandler):
    '''docstring for LogoutHandler'''
    def get(self):
        self.clear_cookie('username')
        self.render('logout.html')

class BlogsHandler(BaseHandler):
    '''docstring for BlogsHandler'''
    def get(self, username, author, id):
        usernameList = files.getUsernames()
        if username in usernameList:
            self.render('index.html', blog=files.getBlog(), comments=files.getComments())
        else:
            self.render('error.html')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/login', LoginHandler), (r'/logout', LogoutHandler), ('/(\w+)/(\w+)/(\d+)', BlogsHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        cookie_secret='bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
        xsrf_cookies=True,
        login_url='/login',
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
