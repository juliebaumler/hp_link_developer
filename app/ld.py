#!/usr/bin/env python

from __future__ import print_function
import json
import os
import requests
import uritemplate
import pprint

link_username = os.environ.get('LINK_API_USER')
link_key = "Basic " + os.environ.get('LINK_API_KEY')

class LinkApiClient(object):
    def __init__(self):
	self.username = link_username
	self.key = link_key

class LinkAuthClient(LinkApiClient):
    def __init__(self):
	super(LinkAuthClient,self ).__init__()
	self.root_url = 'https://www.livepaperapi.com/auth/v1'
	self.base_headers = { 'Authorization': link_key, 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json' }
	self.content = {'grant_type': 'client_credentials', 'scope': 'default'}

    def get(self):
	response = requests.post (self.root_url + '/token',
	    data='grant_type=client_credentials&scope=default',
	    headers=self.base_headers)
	if response.status_code != 200:
	    print("error %s" % response.status_code)
	else:
            self.token = response.json()['accessToken']
	    return response.json()
    
    def upload_file(self, img):
        self.base_headers['Authorization'] = "Bearer "+ self.token
        self.base_headers['Content-Type'] = 'image/jpeg'
        print(self.base_headers)
	response = requests.post('https://storage.livepaperapi.com/objects/v1/files', data=img, headers=self.base_headers)
	if response.status_code != 201:
	    print("error %s" % response.status_code)
	else:
	    self.original_file = response.headers['Location']
	    return response


if __name__=='__main__':
    lauth = LinkAuthClient()
    print(lauth.username, lauth.key)
    pprint.pprint(lauth.get())
    print(lauth.token)
    img = open('../asset/test.jpg').read()
    print(len(img))
    r = lauth.upload_file(img)
    print(lauth.original_file)

