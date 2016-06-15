#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################
#Sample Retweetbot
#V1.4
#MichaelJranglin@gmail.com
#############################
import re
import os
import random
import multiprocessing
import sys
import time
import twython
from twython import Twython
from twython import TwythonStreamer

 
 
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'jqBCOWg9cdXZYBDMJM1rh12xQ'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'AktqLb3TXub4pj8ZlyL3dtjyoNUW8moZXaoVLUDVkhBrvkq20b'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '733405687351365637-pbN3IiTH2ONFeZd4fU0XjnrGh3IN6uH'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'uODza38kstufIfPqQbmp9Tbw0z7RvavwQlrGMk37Nulfv'#keep the quotes, replace this with your access token secretapi = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
#necessary files
StreamFileName = time.strftime("%b_%d_%y")+"_StreamLog.txt"
TweetFileName = time.strftime("%b_%d_%y")+"_TweetLog.txt" 

def RT(ID, name):
    """Performs retweet"""
    print("RT")
    #Tid = int(float(ID))
    tim = time.strftime("%M")
    Tweetusername = 'ComicTweetBot'
    TweetText = 'https://twitter.com/'+Tweetusername+'/status/'+ID
    ReTweet = 'Hi I am ComicTweetBot!('+tim+') I Retweet Comics! Use #comicretweetbot '+TweetText 
    Log = open(TweetFileName, 'a')
    enterlog = ID+' '+name+ '\n'
    Log.write(enterlog)
    Log2 = open('TweetLog.txt', 'a')
    Log2.write(ID+'\n')
    #api.update_status(status= ReTweet)
    api.retweet(id = ID)
    api.create_favorite(id=ID, include_entities = True)
    #randomize the time for sleep 1.5mins to 5 mins
    rant = random.randrange(180, 1000, 2)
    time.sleep(rant)
    
    
   
    
def Do_RT():
    """Similar to Can_RT however is for redundancy"""
    DoRT = True
    twi = open(TweetFileName).read()
    twilog = open('TweetLog.txt').read()
    with open(StreamFileName) as f:
        for line in f:
            
            one = line.split()
            
            if any(x in twi for x in one) or one[0] in twilog:
                
                DoRT = False
                        
            else:
                DoRT = True
                    
            if DoRT == True:
                RT(one[0], one[1])
    return
       



def Can_RT(twib):
    """function to check to see if tweet is duplicate or has been tweeted by bot"""
    RT = 0
    txtfile2 = open('TweetLog.txt', "r").read()
    txtfile = open(TweetFileName, "r").read()
    if 'retweeted_status' in twib or 'RT: @' in twib['text'] or twib['retweeted'] == True:
            
            if twib['retweeted_status']['user']['screen_name'] in txtfile or twib['retweeted_status']['id_str'] in txtfile or 'ComicTweetBot' in twib['retweeted_status']['user']['screen_name'] or twib['retweeted_status']['id_str'] in txtfile2 :
                RT= 0
            else:
                RT = twib['retweeted_status']['id_str']

                
    else:
        
            if twib['user']['screen_name'] in txtfile or twib['id_str'] in txtfile or 'ComicTweetBot' in twib['user']['screen_name'] or twib['id_str'] in txtfile2:
                RT= 0
            else:
                RT = twib['id_str']
                
    return RT
    
class MyStreamer(TwythonStreamer):
    """The stream class derived drom twython streamer class that
        deals with data as it is recieved from the twitter stream"""

    
    def on_success(self, data):
        #checks for a media link in the tweet object (images)
       if 'entities' in data:
            if 'media' in data['entities']:
                if data['entities']['media'][0]['media_url'] != None:
                    #simplified method to parse information
                    #lower cases all letters in text // Regular expression casued script to hang
                    stri = data['text']
                    lstri = stri.lower()
                    #filter these words // Will be moved to config file
                    SFWfilter = ['sex', 'fuck', 'porn', 'fucking'] #words NOT to be in tweet
                    ComicCheck = ['new comic', 'old comic' , 'comic strip' , 'web comic', 'webcomic']
                    if  any(x in lstri for x in SFWfilter):
                        pass
                    else:
                        
                        if  any(x in lstri for x in ComicCheck) :
                             print(data['id_str'])
                             CRT = Can_RT(data)
                             if  CRT != 0:
                                    
                                
                                    StreamLog = open(StreamFileName, 'a')
                                    NewTweet = CRT+' '+data['user']['screen_name']
                                    StreamLog.write(NewTweet+'\n')
                            
                    
            
                
               
                    

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()

   



#Change parameters to filter incoming tweet stream.
stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
def Stream():
    """Function that will manage doing the twitter stream"""
    
    while True:
            name = multiprocessing.current_process().name
            try:
                stream.statuses.filter(track='comic')
                #print("Stream")
            except:
                continue
def Tweet_stream():
    """Function that will manage doing the retweet"""
    name = multiprocessing.current_process().name
    while True:
            try:
                Do_RT()
                #print("Tweet Attempt")
            except:
                continue
def Create_log():
    """Function that will create log file"""
    name = multiprocessing.current_process().name
    while True:
            if os.path.isfile(StreamFileName) is False:
                open(StreamFileName, 'a')
            if os.path.isfile(StreamFileName) is False:
                open('TweetLog.txt', 'a')
            
            if os.path.isfile(TweetFileName) is False:
                twfile = open(TweetFileName, 'a')
                twfile.write('0 ComicTweetBot')
            
if __name__ == '__main__':
    
        ServiceStream = multiprocessing.Process(name='Stream', target=Stream)
        ServiceTweet=   multiprocessing.Process(name='Tweet_stream', target=Tweet_stream)
        Servicelog = multiprocessing.Process(name='Create_log', target= Create_log)
        ServiceStream.start()
        Servicelog.start()
        ServiceTweet.start()
        
        
        
