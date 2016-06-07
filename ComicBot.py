#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################
#Sample Retweetbot
#V1.2
#MichaelJranglin@gmail.com
#############################
import re
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
tlist = []

#trying manually retweeting and adding own words
#STOP BOT FROM RETWEETING SAME FUCKING TWEETS IN A ROW FROM OTHER FUCKING BOTS

##use try catch
def Do_RT(tib):
    Tweetid = tib['id_str']
    TweetImgurl = tib['entities']['media'][0]['id']
    Tweetusername = tib['user']['screen_name']
    TweetText = 'https://twitter.com/'+Tweetusername+'/status/'+Tweetid

    ReTweet = 'Hi I am ComicTweetBot! I Retweet Comics! Use #comicretweetbot '+TweetText 
    
            


    Log = open('log.txt', 'a')
    Log.write(Tweetid +' '+Tweetusername+'\n')
    api.update_status(status= ReTweet)
    api.create_favorite(id=Tweetid, include_entities = True)

    
    #api.retweet(id = tib)
    #tlist.append(tib)
    
    #timeout on sucessfull retweet
    
        
def Can_RT(twib):
    RT = 0
    if 'retweeted_status' in twib or 'RT: @' in twib['text']:
            if twib['retweeted_status']['id_str'] in open('log.txt', "r").read():
                RT= 0
            else:
                RT = twib['retweeted_status']

                
    else:
        
            if twib['id_str'] in open('log.txt', "r").read():
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
                    #for x in ComicCheck:
                        
                        
                       # rmat = re.search(x, stri, re.IGNORECASE)
                        #if rmat :
                    #if 'new comic' or 'New comic' or 'New Comic' or 'Old comic' or 'old comic' or 'Old Comic' in data['text'] :
                                print(data['id_str'])
                                
                                     
                                
                                #Returned collection with tweets on authenticated user timeline
                                #tline = api.get_user_timeline(user_id = self, exclude_replies = 'true', count = 200, include_rts = 'true')
                                #Each new tweet id in string
                                NewTweet = data['id_str']
                                if Can_RT(data) != 0:
                                    Do_RT(Can_RT(data))
                                    time.sleep(90)
                    
            
                
               
                    

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        #self.disconnect()

    def Dconnection(self):
        self.disconnect()



#Change parameters to filter incoming tweet stream.
stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
def run_bot():
    while True:
        #try:
            stream.statuses.filter(track='comic')
           # break
        #except:
         #   stream.statuses.filter(track='new, old, comic')
            
        #else:
         #   return
run_bot()
    
