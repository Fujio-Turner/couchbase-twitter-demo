#!/usr/bin/python
from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import urllib2
import json
from time import sleep

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="..."
consumer_secret="..."

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="..."
access_token_secret="..."

class StdOutListener(StreamListener):
    """ 
    A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    httpSleep = 0.09
    debug     = False

    def on_data(self, data):
        a = json.loads(data) 
        #print(json.dumps(data))
        #print(a['id_str'])
        a['docType'] = 'twitter'
        if 'id_str' in a:   #have to use id_str instead of id as INT due to length restriction
            url = 'http://localhost:4984/sync_gateway/' + str(a['id_str'])
            b = self.put_request(url,json.dumps(a))
            if 'error' in b:  # sometimes tweets get resent in feed, instead of throwing them away I'll update the doc.
                if b['error'] == 409:
                    have = self.get_request(url)
                    url = url + '?rev='+ have['_rev']
                    c = self.put_request(url,json.dumps(a))
        else:
            print(data)
        return True

    def put_request(self,url, data,retry=0):
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(url, data=data)
            request.add_header('Content-Type', 'application/json')
            request.get_method = lambda: 'PUT'
            opener.open(request)
            return {}
        except Exception, e:
            if e:
                if hasattr(e, 'code'):
                    print("Error: HTTP PUT: " + str(e.code))
                    if e.code == 409:
                        print("Conflict - Already in Sync Gateway : " + url)
                        #print(data)
                        b = {}
                        b['error'] = 409
                        return b
            if retry == 3:
                if self.debug == True:
                    print("DEBUG: Tried 3 times could not execute: PUT")             
                if e:
                    if hasattr(e, 'code'):
                        if self.debug == True:
                            print("DEBUG: HTTP CODE ON: PUT - "+ str(e.code))    
                        return e.code
                    else:
                        return False
            sleep(self.httpSleep)
            return self.put_request(url,data,retry+1)

    def get_request(self,url='',retry=0):

        try:
            r = self.jsonChecker(urllib2.urlopen(url).read())
            return r
        except Exception, e:
            if e:
                if hasattr(e, 'code'):
                    print("Error: HTTP GET: " + str(e.code))
            if retry == 3:
                if self.debug == True:
                    print("DEBUG: Tried 3 times could not execute: GET")             
                if e:
                    if hasattr(e, 'code'):
                        if self.debug == True:
                            print("DEBUG: HTTP CODE ON: GET - "+ str(e.code))    
                        return e.code
                    else:
                        return False
            sleep(self.httpSleep)
            return self.get_request(url,retry+1)

    def jsonChecker(self, data=''):
        #checks if its good json and if so return back Python Dictionary
        try:
            checkedData = json.loads(data)
            return checkedData
        except Exception, e:
            return False

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['basketball'],async=True)


#The twitter stream is not always stable i.e. there might be timeouts and retry needed.
# Here is the link talking about it. https://github.com/tweepy/tweepy/blob/master/docs/api.rst