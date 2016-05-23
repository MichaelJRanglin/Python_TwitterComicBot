#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import time
import twython
from twython import Twython
from twython import TwythonStreamer

 
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'Blank'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'Blank'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'Blank-Blank'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'Blank'#keep the quotes, replace this with your access token secret

api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)


#auth = Twython.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#api = Twython.API(auth)


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
         #if 'text' in data:
            if data['retweeted'] == False:
               print(data['retweeted'])
               #api.retweet(id = data['id_str'])
               time.sleep(60)
               
            
            
           
            

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        #self.disconnect()




stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
stream.statuses.filter(track='python')


   
