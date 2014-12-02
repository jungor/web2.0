#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''My first server

Created by Junjie Li, 2014-11-12
Lasted modified by Junjie Li, 2014-11-13
Email: 28715062@qq.com

'''
import re

class Person(object):
    """docstring for Person"""
    def __init__(self, name, gender, age, personality, system, seeking, lowerbound, upperbound):
        super(Person, self).__init__()
        self.name = name
        self.gender = gender
        self.age = age
        self.personality = personality
        self.system = system
        self.seeking = seeking
        self.lowerbound = lowerbound
        self.upperbound = upperbound
        self.photo = self.name.replace(' ', '_').lower()+'.jpg'

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if value:
            self._name = value
        else:
            raise ValueError('You did not provide valid name')

    @property
    def gender(self):
        return self._gender
    @gender.setter
    def gender(self, value):
        if value:
            self._gender = value
        else:
            raise ValueError('You did not provide valid gender')

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        try:
            self._age = int(value)
        except ValueError:
            raise ValueError('You did not provide valid age')
        else:
            if not 0 <= self._age <= 99:
                raise ValueError('You did not provide valid age')
        finally:
            pass

    @property
    def personality(self):
        return self._personality
    @personality.setter
    def personality(self, value):
        if re.match(r'^[IE][SN][FT][JP]$', value):
            self._personality = value
        else:
            raise ValueError('You did not provide valid personality, forgot uppercase?')

    @property
    def system(self):
        return self._system
    @system.setter
    def system(self, value):
        if value:
            self._system = value
        else:
            raise ValueError('You did not provide valid system.')

    @property
    def seeking(self):
        return self._seeking
    @seeking.setter
    def seeking(self, value):
        if value:
            self._seeking = ''.join(value)
        else:
            raise ValueError('You did not provide valid seeking.')

    @property
    def lowerbound(self):
        return self._lowerbound
    @lowerbound.setter
    def lowerbound(self, value):
        try:
            self._lowerbound = int(value)
        except ValueError:
            raise ValueError('You did not provide valid lowerbound')
        else:
            if not 0 <= self._lowerbound <= 99:
                raise ValueError('You did not provide valid lowerbound')
        finally:
            pass

    @property
    def upperbound(self):
        return self._upperbound
    @upperbound.setter
    def upperbound(self, value):
        try:
            self._upperbound = int(value)
        except ValueError:
            raise ValueError('You did not provide valid upperbound')
        else:
            if not (0 <= self._upperbound <= 99 and self._lowerbound <= self._upperbound):
                raise ValueError('You did not provide valid upperbound')
        finally:
            pass

    @property
    def photo(self):
        return self._photo
    @photo.setter
    def photo(self, value):
        self._photo = value

    def ismatch(self, you):
        if self.seeking.find(you.gender) >= 0 and you.seeking.find(self.gender) >= 0:
            return True
        else:
            return False

    def rating(self, you):
        result = 0
        if self._lowerbound <= you.age <= self._upperbound\
        and you._lowerbound <= self.age <= you._upperbound:
            result += 1
        if self.system == you.system:
            result += 2
        result += len(set(self.personality)&set(you.personality))
        return result
    def __str__(self):
        return ','.join([self.name, self.gender, str(self.age), self.personality, self.system, self.seeking, str(self.lowerbound), str(self.upperbound)])
