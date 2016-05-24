#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################
#Sample Retweetbot
#V1.1
#MichaelJranglin@gmail.com
#############################
import sys
import time
import twython
from twython import Twython
from twython import TwythonStreamer

 
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'blank'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'blank'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'blank'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'blank'#keep the quotes, replace this with your access token secret

api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)


#auth = Twython.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#api = Twython.API(auth)


class MyStreamer(TwythonStreamer):
    #edit the on_sucess method to handle how data stream is parsed
    def on_success(self, data):

        #ID string for authenticated user (BOT)
        self = api.verify_credentials()['id_str']
        #Returned collection with tweets on authenticated user timeline
        tline = api.get_user_timeline(user_id = self, exclude_replies = 'true', count = 200, include_rts = 'true')
        #Each new tweet id in string
        NewTweet = data['id_str']
        #Boolean to check whether authenticated user has retweeted
        DoRT = True
        #iterates through tweets in timeline // Checks to see if new tweet has been retweeted
        for tweet in tline:
            if tweet['id_str'] == NewTweet:
                DoRT = False
        if DoRT == True:
            api.retweet(id = data['id_str'])
            #print(data['id_str'], " ",tline)
            #timeout on sucessfull retweet
            time.sleep(60)    

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        #self.disconnect()

    def Dconnection(self):
        self.disconnect()


stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
#Change parameters to filter incoming tweet stream.
stream.statuses.filter(track='Mortgage')



   
