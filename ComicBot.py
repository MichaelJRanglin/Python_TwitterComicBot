#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################
#Sample Retweetbot
#V1.3
#MichaelJranglin@gmail.com
#############################
import re
import multiprocessing
import sys
import time
import twython
from twython import Twython
from twython import TwythonStreamer

 
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'blank'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'blank'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'blank-pbN3IiTH2ONFeZd4fU0XjnrGh3IN6uH'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'blank'#keep the quotes, replace this with your access token secretapi = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)


def RT(ID):
    print("RT")
    Tid = int(float(ID))
    tim = time.strftime("%M")
    Tweetusername = 'ComicTweetBot'
    TweetText = 'https://twitter.com/'+Tweetusername+'/status/'+ID
    ReTweet = 'Hi I am ComicTweetBot!('+tim+') I Retweet Comics! Use #comicretweetbot '+TweetText 
    Log = open('TweetLog.txt', 'a')
    Log.write(ID +'\n')
    api.update_status(status= ReTweet)
    #api.create_favorite(id=Tid, include_entities = True)
 
    time.sleep(90)
    
    #api.retweet(id = tib)
    #tlist.append(tib)
    
    #timeout on sucessfull retweet
    
def Do_RT():
    DoRT = True
    with open('StreamLog.txt') as f:
        for line in f:
            one = line

            with open('TweetLog.txt') as a:
                for line in a:
                    two = line
                   
                    if one is two:
                        DoRT = False
                        
            if DoRT == True:
                    RT(one)
    return

    
        
def Can_RT(twib):
    RT = 0
    if 'retweeted_status' in twib or 'RT: @' in twib['text']:
            if twib['retweeted_status']['id_str'] in open('TweetLog.txt', "r").read():
                RT= 0
            else:
                RT = twib['retweeted_status']

                
    else:
        
            if twib['id_str'] in open('TweetLog.txt', "r").read():
                RT= 0
            else:
                RT = twib
                
    return RT
    
class MyStreamer(TwythonStreamer):
    #edit the on_sucess method to handle how data stream is parsed
    def on_success(self, data):
       if 'entities' in data:
            if 'media' in data['entities']:
                if data['entities']['media'][0]['media_url'] != None:
                    ComicCheck = ['new comic', 'old comic' , 'comic strip' , 'web comic', 'webcomic']
                    stri = data['text']
                    lstri = stri.lower()
                    if  any(x in lstri for x in ComicCheck) :
                        if Can_RT(data) != 0:
                                print(data['id_str'])
                            
                                StreamLog = open('StreamLog.txt', 'a')
                                NewTweet = data['id_str']
                                StreamLog.write(NewTweet+'\n')
                            
                    
            
                
               
                    

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        #self.disconnect()

    def Dconnection(self):
        self.disconnect()



#Change parameters to filter incoming tweet stream.
stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
def Stream():
            name = multiprocessing.current_process().name
            stream.statuses.filter(track='comic')
            #print("Stream")
def Tweet_stream():
    while True:
        name = multiprocessing.current_process().name
        Do_RT()
        #print("Tweet Attempt")
        
                    
if __name__ == '__main__':
        ServiceStream = multiprocessing.Process(name='Stream', target=Stream)
        ServiceTweet=   multiprocessing.Process(name='Tweet_stream', target=Tweet_stream)
        ServiceStream.start()
        ServiceTweet.start()
        
        
        
