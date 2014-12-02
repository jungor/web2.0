#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Files handling

Created by Junjie Li, 2014-12-2
Lasted modified by Junjie Li, 2014-12-2
Email: 28715062@qq.com

'''

import os.path

USERS_PATH = os.path.join(os.path.dirname(__file__), 'users.txt')
BLOG_PATH = os.path.join(os.path.dirname(__file__), 'blog.txt')
COMMENTS_PATH = os.path.join(os.path.dirname(__file__), 'comments.txt')

# class User(object):
#     """docstring for User"""
#     def __init__(self, name, psw):
#         super(User, self).__init__()
#         self.name = name
#         self.psw = psw

def getUsers():
    with open(USERS_PATH) as users :
        return [line.strip() for line in users.readlines()]

def getUsernames():
    with open(USERS_PATH) as users :
        return [line.strip().split(',')[0] for line in users.readlines()]

def getBlog():
    with open(BLOG_PATH) as blog:
        return {'title': blog.readline().strip().split(':')[1],
                'author': blog.readline().strip().split(':')[1],
                'body': blog.readline().strip().split(':')[1]}

def getComments():
    with open(COMMENTS_PATH) as comments:
        return [line.strip().split('|') for line in comments.readlines()]

def addComment(comment):
    with open(COMMENTS_PATH, 'a+') as comments:
        comments.writelines((comment, '\n'))
