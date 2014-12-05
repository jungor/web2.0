# -*- coding: utf-8 -*-
#!/usr/bin/env python

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
import re
import time
import json

from tornado.options import define, options
define('port', default=8001, help='run on the given port', type=int)

class BaseHandler(tornado.web.RequestHandler):
    '''docstring for BaseHandler'''
    def get_current_user(self):
        return self.get_secure_cookie('name')

class LoginHandler(BaseHandler):
    '''docstring for LoginHandler'''
    def get(self):
        self.render('login_signup.html', is_login=True)
    def post(self):
        name = self.get_argument('name', None)
        psw = self.get_argument('password', None)
        userList = files.getUsers()
        user = ','.join([name, psw])
        if user in userList:
            self.set_secure_cookie('name', name)
            self.redirect('/')
        else:
            self.redirect('/login')

class SignupHandler(BaseHandler):
    '''docstring for SignupHandler'''
    def get(self):
        self.render('login_signup.html', is_login=False)
    def post(self):
        name = self.get_argument('name', None)
        psw = self.get_argument('password', None)
        usernameList = files.getUsernames()
        if re.match(r'[a-zA-Z0-9]{6,12}', name)\
        and re.match(r'[a-zA-Z0-9]{6,12}', psw)\
        and not (name in usernameList):
            self.set_secure_cookie('name', name)
            files.addUser(name, psw)
            self.redirect('/')
        else:
            self.redirect('/signup')

class IndexHandler(BaseHandler):
    '''docstring for IndexHandler'''
    @tornado.web.authenticated
    def get(self):
        questions = files.getQuestions()
        replies = files.getReplies()
        self.render('index.html', questions=questions, replies=replies)

class QuestionHandler(BaseHandler):
    """docstring for QuestionHandler"""
    @tornado.web.authenticated
    def get(self):
        self.render('question.html')
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument('title', None)
        time = self.get_argument('time', None)
        content = self.get_argument('content', None)
        if title and time and content:
            files.addQuestion(title, str(time), self.get_current_user(), content)
            self.redirect('/')
        else:
            self.redirect('/question')

class ReplyHandler(BaseHandler):
    """docstring for replyHandler"""
    # @tornado.web.authenticated
    # def get(self):
    #     respose = {
    #         'time': time.strftime('%Y-%m-%d',time.localtime(time.time())),
    #         'author': self.get_current_user()
    #     }
    #     self.write(json.dumps(respose))
    @tornado.web.authenticated
    def post(self):
        subject = self.get_argument('subject', None)
        content = self.get_argument('content', None)
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        author = self.get_current_user()
        if subject and content:
            files.addReply(subject, date, author, content)
            self.write('<div class="jumbotron reply col-sm-10 col-sm-offset-2">'
          '<div class="replyTxt">'+content+'</div>'
          '<div class="replyTime">'+date+'</div>'
          '<div class="replyAuthor">'+author+'</div>'
        '</div>')

class LogoutHandler(BaseHandler):
    '''docstring for LogoutHandler'''
    def get(self):
        self.clear_cookie('name')
        self.redirect('/login')

class ErrorHandler(BaseHandler):
    '''docstring for ErrorHandler'''
    def get(self):
        self.render('error.html')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/', IndexHandler),
                (r'/login', LoginHandler),
                (r'/logout', LogoutHandler),
                (r'/signup', SignupHandler),
                (r'/question', QuestionHandler),
                (r'/reply', ReplyHandler),
                (r'/\S+', ErrorHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'template'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        cookie_secret='61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
        xsrf_cookies=True,
        login_url='/login',
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
