# -*- coding: utf-8 -*-
#!/usr/bin/env python

'''APIs of files IO

Created by Junjie Li, 2014-12-2
Lasted modified by Junjie Li, 2014-12-2
Email: 28715062@qq.com

'''

import os.path

USERS_PATH = os.path.join(os.path.dirname(__file__), 'static', 'data', 'userData.txt')
QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), 'static', 'data', 'questionData.txt')
REPLIES_PATH = os.path.join(os.path.dirname(__file__), 'static', 'data', 'replyData.txt')

def getUsers():
    with open(USERS_PATH) as users:
        return [line.strip() for line in users.readlines()]

def getUsernames():
    with open(USERS_PATH) as users:
        return [line.strip().split(',')[0] for line in users.readlines()]

def addUser(name, psw):
    with open(USERS_PATH, 'a+') as users:
        users.writelines((','.join([name, psw]), '\n'))

def getQuestions():
    with open(QUESTIONS_PATH) as questions:
        return [line.strip().split(';') for line in questions.readlines()]

def addQuestion(title, time, author, content):
    with open(QUESTIONS_PATH, 'a+') as questions:
        questions.writelines((';'.join([title.encode('utf8'), time.encode('utf8'), author.encode('utf8'), content.encode('utf8')]), '\n'))

def getReplies():
    with open(REPLIES_PATH) as replies:
        return [line.strip().split(';') for line in replies.readlines()]

def addReply(subject, time, author, content):
    with open(REPLIES_PATH, 'a+') as replies:
        replies.writelines((';'.join([subject.encode('utf8').encode('utf8'), time.encode('utf8').encode('utf8'), author.encode('utf8').encode('utf8'), content.encode('utf8')]), '\n'))
