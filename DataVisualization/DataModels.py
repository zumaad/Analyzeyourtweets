import tweepy
import time
import pytz
from datetime import date,timedelta,datetime
import numpy
from numpy import median
import calendar
from DataVisualization.safetyfirst import api
from DataVisualization.utilityfunctions import cleanatweet,sentiments,putstextonnewline,convertmilitary,get_top_x_values_in_dic,month_to_number



class tweetzz():
    """ class to represent a tweet. Used to store information about a tweet like its text,author,etc to retrieve later
    
    Attributes
    -----------
    tweetername : str
        the author of the tweet
    timezone : Datetime
        timezone of the tweet
    text : str
        the text of the tweet
    time : Datetime
        a datetime object representing the time of the tweet
    year: int
        year of the tweet
    month: int
        month of the tweet
    day: int
        day of the tweet
    weekday: str
        weekday of the tweet
    sentiment: int
        sentiment score of a tweet
    replyto : str
        the twitter handle the tweet is in reply to
    retweetofwhom : str
        the twitter handle the tweet is a retweet of
    quoteof: str
        the twitter handle the tweet is a quote of
    mentions: list 
        list of the twitter handles the tweet mentions
    retweetcount: int
        the amount of times a tweet has been retweeted
    favoritecount : int
        the amount of times a tweet has been favorited
    length : int
        the character length of a tweet
       
    Methods
    -------
    
    fixtime(time,timezone)
        fixes the time of a tweet in accordance with the timezone given.
    
    getretweetof(tweetobj)
        gets twitter handle of the user the tweet is a retweet of
    
    getquoteof(tweetobj)
        gets twitter handle of the user the tweet is a retweet of
        
    get_fav_rt_count_of_only_wanted_user_tweets(self,tweetobj)
        gets favorite and retweet count of a tweet, only if it isn't a retweet
    """
   

    #gets relevant info from a tweet and ecapsulates it so that it can be
    #accessed cleanly later on to display data.
    def __init__(self,timezone,tweetobj,name):
        """
        Parameters
        ----------
        
        timezone : str
            the timezone the tweet should be in.
        tweetobj: Tweepy Status Object
            represents the data that tweepy gets about a tweet from the twitter api
        name: str
            the name of the author of the tweet
        """
            
        self.tweetername = name
        self.timezone = timezone
        self.text = cleanatweet(tweetobj.full_text)
        self.time = tweetzz.fixtime(tweetobj.created_at,self.timezone)
        self.year = self.time.year
        self.month = self.time.month
        self.day = self.time.day
        self.weekday = calendar.day_name[self.time.weekday()]
        self.sentiment = sentiments(self.text)['compound']
        self.replyto = tweetobj.in_reply_to_screen_name
        self.retweetofwhom = tweetzz.getretweetof(tweetobj)
        self.quoteof = tweetzz.getquoteof(tweetobj)
        self.mentions = tweetobj.entities['user_mentions']
        self.retweetcount = None
        self.favoritecount = None
        self.length = len(self.text)
        self.get_fav_rt_count_of_only_wanted_user_tweets(tweetobj)
        
        
        
    
    @staticmethod
    def fixtime(time,timezone):
        gmt = pytz.timezone('GMT')
        gmt_date = gmt.localize(time) 
        correcttimezone = pytz.timezone(timezone)
        correct_date = gmt_date.astimezone(correcttimezone)
        return correct_date
    
    @staticmethod
    def getretweetof(tweetobj):
        if hasattr(tweetobj,'retweeted_status'):
            return tweetobj.retweeted_status.user.screen_name
    
    @staticmethod
    def getquoteof(tweetobj):
        if hasattr(tweetobj,"quoted_status"):
            return tweetobj.quoted_status.user.screen_name
    
    
    
    def get_fav_rt_count_of_only_wanted_user_tweets(self,tweetobj):
        
        if self.retweetofwhom == None:
            self.retweetcount = tweetobj.retweet_count
            self.favoritecount = tweetobj.favorite_count

    @staticmethod
    def gettweets(name,num,timezone):
        tweets = tweepy.Cursor(api.user_timeline,screen_name = name,tweet_mode = 'extended').items(num)
        tweetlist =[]
        
        for tweet in tweets:
            
                mytweet = tweetzz(timezone,tweet,name)
                tweetlist.append(mytweet)
        
        return tweetlist

  

class monthbatch():
    def __init__(self,month,onedaylist):
        self.month = month
        self.onedaylist = onedaylist

    def assembledaybatches(self):
        onedaylist1 = []
        daybatchlist =[]
        for tweet in self.onedaylist:
            if onedaylist1 !=[]:
                if tweet.day!=onedaylist1[-1].day:
                    daybatch1 = daybatch(datetime(onedaylist1[-1].year,onedaylist1[-1].month,onedaylist1[-1].day),onedaylist1)
                    daybatchlist.append(daybatch1)
                    onedaylist1 = []
                    
            onedaylist1.append(tweet)
        leftoverbatch = daybatch(datetime(onedaylist1[-1].year,onedaylist1[-1].month,onedaylist1[-1].day),onedaylist1)
        daybatchlist.append(leftoverbatch)
        
        self.onedaylist = daybatchlist

        #create month batches and day batches
    
    @staticmethod
    def monthanddaybatches(base):
        daylist = []
        monthbatchlist =[]
        for tweet in base:
            #change to if daylist (idiomatic)
            if daylist != []:
                if tweet.month != daylist[-1].month or tweet.year != daylist[-1].year:
                    monthb = monthbatch(datetime(daylist[-1].year,daylist[-1].month,daylist[-1].day),daylist)
                    monthb.assembledaybatches()
                    monthbatchlist.append(monthb)
                    daylist = []

            daylist.append(tweet)
        leftover = monthbatch(datetime(daylist[-1].year,daylist[-1].month,daylist[-1].day),daylist)
        leftover.assembledaybatches()
        monthbatchlist.append(leftover)
        return monthbatchlist

    @staticmethod
    def justmonthbatches(base):
        daylist = []
        monthbatchlist =[]
        for tweet in base:
            #change to if not sentimentlist (idiomatic)
            if daylist != []:
                if tweet.month != daylist[-1].month or tweet.year != daylist[-1].year:
                    monthb = monthbatch(datetime(daylist[-1].year,daylist[-1].month,daylist[-1].day),daylist)
                    monthbatchlist.append(monthb)
                    daylist = []

            daylist.append(tweet)
        leftover = monthbatch(datetime(daylist[-1].year,daylist[-1].month,daylist[-1].day),daylist)
        monthbatchlist.append(leftover)
        return monthbatchlist
        



class daybatch():
    def __init__(self,day,daylist):
        self.day = day
        self.daylist = daylist


    def getmedian(self):
        sentimentlist = [tweet.sentiment for tweet in self.daylist if tweet.sentiment != 0.0]
        #change to if not sentimentlist (idiomatic)
        if sentimentlist != []:
            med = median(sentimentlist)
            return med
        else:
            return 'no non zero sentiment scores in this day'

    def getcount(self):
        return len(self.daylist)
    
    def gettext(self):
        tweetstringoftheday = ''
        count = 1
        for tweet in self.daylist:
            tweetstring = str(count) + ' : ' + putstextonnewline(tweet.text) + ' <br> '
            count = count + 1
            tweetstringoftheday = tweetstringoftheday + tweetstring
        return tweetstringoftheday



  



       

















