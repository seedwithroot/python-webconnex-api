#!/usr/bin/python2.4
#
# Copyright 2014 TwoBlueShoes
#

'''A library that provides a Python interface to the Webconnex REST API'''

__author__ = 'python-twitter@googlegroups.com'
__version__ = '0.8.5'


import requests
import simplejson

class WebconnexError(Exception):
  '''Base class for Webconnex errors'''

  @property
  def message(self):
    '''Returns the first argument used to construct this error.'''
    return self.args[0]


class API(object):
    def __init__(self, api_key=None,base_url=None):
    
        if base_url is None:
            self.base_url = 'https://cp.webconnex.com/api'
        else:
            self.base_url = base_url
        
        self.api_key = api_key

    def GetRegistrations(self):

        url  = '%s/%s/registrations' % (self.base_url,self.api_key)
        json = self._FetchUrl(url)
        data = self._ParseAndCheck(json)
        registrants = []
        for i in data['result']:
            r = Registrant(id=i['id'],first_name=i['first_name'],last_name=i['last_name'],status=i['status'],amount=i['amount'])
            registrants.append(r)
        return registrants
            
        
    
    def _CheckForWebconnexError(self, data):
        """Raises a TwitterError if twitter returns an error message.
    
        Args:
          data:
            A python dict created from the Twitter json response
    
        Raises:
          TwitterError wrapping the twitter error message if one exists.
        """
        # Twitter errors are relatively unlikely, so it is faster
        # to check first, rather than try and catch the exception
        if 'error' in data:
          raise WebconnexError(data['error'])
        if 'errors' in data:
          raise WebconnexError(data['errors'])

    def _FetchUrl(self,url,post_data=None,parameters=None,headers=None,no_cache=None,use_gzip_compression=None):
        if post_data:
            response = requests.post(url, data=post_data, headers=headers)
        else:
            response = requests.get(url,headers=headers)
        return response.json()
        
    def _ParseAndCheck(self, json):
        """Try and parse the JSON returned from Twitter and return
        an empty dictionary if there is any error. This is a purely
        defensive check because during some Twitter network outages
        it will return an HTML failwhale page."""
        try:
          data = json #simplejson.loads(json)
          self._CheckForWebconnexError(data)
        except ValueError:
          if "<title>Webconnex / Over capacity</title>" in json:
            raise TwitterError("Capacity Error")
          if "<title>Webconnex / Error</title>" in json:
            raise TwitterError("Technical Error")
          raise TwitterError("json decoding")
    
        return data

class Registrant(object):
    
    def __init__(self,id=None,first_name=None,last_name=None,status=None,amount=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.amount = amount
    
    def GetFirstName(self):
        '''Get the time this status message was posted.
        
        Returns:
        The time this status message was posted
        '''
        return self._first_name

    def SetFirstName(self, first_name):
        '''Set the time this status message was posted.
        
        Args:
          created_at:
            The time this status message was created
        '''
        self._first_name = first_name
    
    first_name = property(GetFirstName, SetFirstName,doc='The time this status message was posted.')
    
    
        