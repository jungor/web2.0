#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Form validator

Created by Junjie Li, 2014-11-11
Lasted modified by Junjie Li, 2014-11-26
Email: 28715062@qq.com

'''

import os

import json

import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("buyagrade.html")

class SuckerHandler(tornado.web.RequestHandler):
    def post(self):
        def _luhn(cardid):
            '''Luhn algorithm
            A method to check whther the cardid is valid'''
            idnum = int(''.join(re.split(r'\D', cardid)))
            nums = []
            result = 0
            while idnum:
                nums.append(idnum%10)
                idnum /= 10
            for i in xrange(len(nums)):
                if i%2 == 0:
                    result += nums[i]
                elif nums[i]*2 > 9:
                    result += (nums[i]*2%10+nums[i]*2/10)
                else:
                    result += nums[i]*2
            return not result%10
        kwargs = {
            'name': self.get_argument('name', None),
            'section': self.get_argument('section', None),
            'cardid': self.get_argument('cardid', None),
            'cardtype': self.get_argument('cardtype', None)
        }
        match = re.match(r'^(\d{4}\D?){4}$', kwargs['cardid'])
        if not(kwargs['name'] and kwargs['section']\
            and kwargs['cardid'] and kwargs['cardtype']):
            sorrymessage = 'You did not fill out the form completely.'
            self.render('sorry.html', sorrymessage=sorrymessage)
        elif not(match and _luhn(match.group())\
            and (kwargs['cardtype'] == 'visa'\
            and kwargs['cardid'][0] == '4'\
            or kwargs['cardtype'] == 'visa'\
            and kwargs['mastercard'][0] == '5')):
            sorrymessage = 'You did not provide a valid card number'
            self.render('sorry.html', sorrymessage=sorrymessage)
        else:
            json_str = json.dumps(kwargs)
            with open(os.path.join(os.path.dirname(__file__),\
                'templates', 'suckers.txt'), 'a') as suckers:
                suckers.writelines((json_str, '\n'))
            with open(os.path.join(os.path.dirname(__file__),\
                'templates', 'suckers.txt')) as suckers:
                records = [json.loads(line) for line in suckers.readlines()]
            self.render('sucker.html', records=records, **kwargs)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/sucker', SuckerHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=True
    )
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
