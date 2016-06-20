#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################
#Sample Retweetbot
#V1.6
#MichaelJranglin@gmail.com
#Copyright 2016 Michael Ranglin
#
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
import configparser


def config_create():
        
        """
        ## EXAMPLE OF botconfig.ini FILE ##

        
        [Auth]
        consumer_key = qweqf
        consumer_secret = secret
        access_key = key
        access_secret = secret acess
        botname = TweetBot

        [Log]
        log1 = StreamLog
        log2 = TweetLog
        log3 = TweetLog

        [Filter]
        search = Twitter
        string1 = Badword, Badword2, More, etc
        string2 = Phrase one, old phrase, this too, three, Awesome

        [Tweet_Delay]
        min = 180
        max = 1000
        step = 2

        [Latest_Log]
        currentstreamlog = Jun_19_16_StreamLog.txt
        currenttweetlog = Jun_19_16_TweetLog.txt
        OverallLog = TweetLog.txt
        
        """

        """
        global CONSUMER_KEY  
        global CONSUMER_SECRET 
        global ACCESS_KEY 
        global ACCESS_SECRET
        global TweetBotName 
        global StreamL 
        global TweetL 
        global NSFW 
        global SFW 
        global searchterm 
        global tMax 
        global tMin 
        global tStep
        
        config = configparser.ConfigParser()
        with open('botconfig.ini', 'r') as configfile:
        config.read_file(configfile)
        CONSUMER_KEY =  config.get('Auth', 'CONSUMER_KEY') 
        CONSUMER_SECRET = config.get('Auth', 'CONSUMER_SECRET').encode('utf-8') 
        ACCESS_KEY = config.get('Auth', 'ACCESS_KEY').encode('utf-8')
        ACCESS_SECRET = config.get('Auth', 'ACCESS_SECRET').encode('utf-8')
        TweetBotName = config.get('Auth', 'BotName')
        StreamL = config.get('Log', 'Log1')
        TweetL = config.get('Log', 'Log2')
        NSFW = config.get('Filter', 'String1')
        SFW = config.get('Filter', 'String2')
        searchterm = config.get('Filter', 'Search')
        tMax = int(float(config.get('Tweet_Delay', 'Max')))
        tMin = int(float(config.get('Tweet_Delay', 'Min')))
        tStep = int(float(config.get('Tweet_Delay', 'Step')))
        global api 

        """
        config = configparser.ConfigParser()
        with open('botconfig.ini', 'r') as configfile:
            config.readfp(configfile)
        return config
    
class MyStreamer(TwythonStreamer):
    """The stream class derived drom twython streamer class that
        deals with data as it is recieved from the twitter stream"""

    
    def on_success(self, data):
        config = config_create()
        time.sleep(1)
        NSFW = config.get('Filter', 'string1')
        SFW = config.get('Filter', 'string2')
        
        NSFWCheck = NSFW.split(",")
        SFWCheck = SFW.split(",")
         
        #checks for a media link in the tweet object (images)
        if 'entities' in data:
            if 'media' in data['entities']:
                if data['entities']['media'][0]['media_url'] != None:
                    #simplified method to parse information
                    #lower cases all letters in text // Regular expression casued script to hang
                    stri = data['text']
                    lstri = stri.lower()
                    #filter these words // Will be moved to config file
                    #SFWfilter = ['sex', 'fuck', 'porn', 'fucking'] #words NOT to be in tweet
                    #ComicCheck = ['new comic', 'old comic' , 'comic strip' , 'web comic', 'webcomic']
                    NSFW = config.get('Filter', 'string1')
                    SFW = config.get('Filter', 'string2')
                    
                    NSFWCheck = NSFW.split(",")
                    SFWCheck = SFW.split(",")
                    
                    
                    
                    if  any(x in lstri for x in SFWCheck):
                                
                                            
                        if  any(x in lstri for x in NSFWCheck):
                                print("NSFW tweet")

                                return
                             
                                
                            
                                    
                            
                        else:
                                
                                CRT = Can_RT(data, config)
                                if  CRT != 0:
                                        print("Tweet added")
                                        x1 = config.get('Latest_Log', 'currentstreamlog')
                                        StreamLog = StreamLog = open(x1, 'a')
                                        NewTweet = CRT+','+data['user']['screen_name']
                                        StreamLog.write(NewTweet+'\n')
                                                 

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        #self.disconnect()


def RT(ID, name):
    """Function that actually retweets tweet"""
    """Takes a ID and username parameter"""
    """Once tweeted log is updated in overall and to date tweetlog"""
    
    config = config_create()
    print("RT")
    #Tid = int(float(ID))
    Tweetusername = config.get('Auth', 'botname')
    #TweetText = 'https://twitter.com/'+Tweetusername+'/status/'+ID
    #ReTweet = 'Hi I am ComicTweetBot!('+tim+') I Retweet Comics! Use #comicretweetbot '+TweetText
    x2 = config.get('Latest_Log', 'currenttweetlog')
    x3 = config.get('Latest_Log', 'overalllog')
    CONSUMER_KEY =  config.get('Auth', 'CONSUMER_KEY') 
    CONSUMER_SECRET = config.get('Auth', 'CONSUMER_SECRET')
    ACCESS_KEY = config.get('Auth', 'ACCESS_KEY')
    ACCESS_SECRET = config.get('Auth', 'ACCESS_SECRET')
    api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    tMax = int(float(config.get('Tweet_Delay', 'Max')))
    tMin = int(float(config.get('Tweet_Delay', 'Min')))
    tStep = int(float(config.get('Tweet_Delay', 'Step')))
    Log = open(x2, 'w')
    enterlog = ID+' '+name+ '\n'
    Log.write(enterlog)
    Log2 = open(x3, 'w')
    Log2.write(ID+'\n')
    #api.update_status(status= ReTweet)
    api.retweet(id = ID)
    api.create_favorite(id=ID, include_entities = True)
    #randomize the time for sleep 1.5mins to 5 mins
    rant = random.randrange(tMin, tMax, tStep)
    time.sleep(rant)
   
    
    
   
    
def Do_RT():
    """Function to begin retweeting"""
    """Prases through each line of to-date stream log"""
    """Rudundancy check to make sure tweet ID has not already been tweeted"""
    
    config = config_create()
    x1 = config.get('Latest_Log', 'currentstreamlog')
    x2 = config.get('Latest_Log', 'currenttweetlog')
    x3 = config.get('Latest_Log', 'overalllog')
    
    DoRT = True
    twi = open(x2).read() #To date's Tweet log
    twilog = open(x3).read() #To date Overal Tweeted Log
    with open(x1) as f:
        for line in f:
            
            one = line.split(",")
            
            #if any(x in twi for x in one) or one[0] in twilog or ' ' in one[0]:
            if one[0] in twi or one[0] in twilog or ' ' in one[0]:
                
                DoRT = False
                        
            else:
                DoRT = True
                    
            if DoRT == True:
                RT(one[0], one[1])
                
    return 

def Can_RT(twib,config):
    """This function checks to see if the tweet object has not already been retweeted by checking against logs"""
    """
    config = configparser.ConfigParser()
    with open('botconfig.ini', 'r') as configfile:
            config.read_file(configfile)
    """

    x2 = config.get('Latest_Log', 'currenttweetlog')
    x3 = config.get('Latest_Log', 'overalllog')
    RT = 0
    
    txtfile2 = open(x3, "r").read()
    txtfile = open(x2, "r").read()
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
    

   



#Change parameters to filter incoming tweet stream.
def Stream():
    """Function to maintain stream logic and handle errors"""
 
    config = config_create()
    CONSUMER_KEY =  config.get('Auth', 'CONSUMER_KEY') 
    CONSUMER_SECRET = config.get('Auth', 'CONSUMER_SECRET')
    ACCESS_KEY = config.get('Auth', 'ACCESS_KEY')
    ACCESS_SECRET = config.get('Auth', 'ACCESS_SECRET')
    searchterm = config.get('Filter','search')
    name = multiprocessing.current_process().name
    """Function that will manage doing the twitter stream"""
    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    stream.statuses.filter(track= searchterm)
    
def Tweet_stream():
    """Function that will manage doing the retweet"""
    
    while True:
                        name = multiprocessing.current_process().name
            
                    
            #try:
                            
                        print('Begin Tweet Attempt')
                        
                        Do_RT()
                        time.sleep(1)
                        
                                  
            #except:
                        #add rate limit
                        #print('Tweet Stream Error')
                        #continue
                        #Tweet_stream()
def Create_log():
    """Function that will create log file"""
    """And Maintain log file to the current date in MMM_DD_YY format"""
    
    name = multiprocessing.current_process().name
    config = config_create()
    Stream = config.get('Log', 'Log1')
    Tweet = config.get('Log', 'Log2')
    OverallLog = config.get('Log', 'Log3')
    
    uscore = '_'
    txtn = '.txt'
    StreamL = uscore +Stream+ txtn
    TweetL = uscore +Tweet+ txtn
    OverallLogL = OverallLog+txtn
    
    
    
    name = multiprocessing.current_process().name
    StreamFileName = time.strftime("%b_%d_%y")+StreamL
    TweetFileName = time.strftime("%b_%d_%y")+TweetL
    config.set('Latest_Log', 'currentstreamlog',StreamFileName)
    config.set('Latest_Log', 'currenttweetlog',TweetFileName)
    config.set('Latest_Log', 'overalllog',OverallLogL)
    
    with open('botconfig.ini', 'w') as x:
        config.write(x)
    if os.path.isfile(StreamFileName) is False:
        open(StreamFileName, 'w')
       
    if os.path.isfile(OverallLogL) is False:
        open(OverallLogL, 'w')
    
    if os.path.isfile(TweetFileName) is False:
        twfile = open(TweetFileName, 'w')
        ## Edit this or comment to change first line entered upon
        ## File creation
        twfile.write('0 ComicTweetBot')
    #time.sleep(1)
    #Create_log()
    
            
if __name__ == '__main__':
        ServiceTweet = multiprocessing.Process(name='Tweet Stream', target= Tweet_stream)
        ServiceLog = multiprocessing.Process(name='Tweet Log', target= Create_log)
        ServiceStream = multiprocessing.Process(name='Stream', target= Stream)
        ServiceStream.start()
        ServiceTweet.start()
        ServiceLog.start()
        
        
        
        
        
