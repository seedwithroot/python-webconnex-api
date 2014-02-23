#!/usr/bin/python2.4
#
# Copyright 2014 TwoBlueShoes
#

'''A library that provides a Python interface to the Webconnex REST API'''

__author__ = 'python-twitter@googlegroups.com'
__version__ = '0.8.5'


import requests

class WebconnexError(Exception):
  '''Base class for Webconnex errors'''

  @property
  def message(self):
    '''Returns the first argument used to construct this error.'''
    return self.args[0]


class API(object):
    def __init__(self,
               api_key=None,
               base_url=None):
    
    if base_url is None:
        self.base_url = 'https://cp.webconnex.com/api'
    else:
        self.base_url = base_url
