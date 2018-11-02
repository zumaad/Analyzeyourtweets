import tweepy
from numpy import median
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime


def cleanatweet(tweet):
    if 'RT' or '@' or 'http' in tweet:
        cleanedtweet = cleansentence(tweet)
    return cleanedtweet



 
#cleans one tweet -helper for cleanatweet()
def cleansentence(tweet):
    dirtytweet = tweet.split(' ')
    return ' '.join([word for word in dirtytweet if not word.startswith('@') and not word.startswith('RT') and not word.startswith('http')])



analyser = SentimentIntensityAnalyzer()
def sentiments(tweet):
    scores = analyser.polarity_scores(tweet)
    
    return scores


#returns sentiment of specific word
def get_sentiment(word,base): 
    compoundscore = 0
    count = 0
    compoundlist = []
    for k,v in base.items():
        
        if word in v:
            print(v)
            
            
            if sentiments(v)['compound'] != 0:
                compoundscore = compoundscore + sentiments(v)['compound']
                compoundlist.append(sentiments(v)['compound'])
                count = count + 1

   
    #take median of all the compounds 
    return (median(compoundlist))

#why is tweepy returning such off hours???
def convertmilitary(militarytime):
    miltociv ={19:'7 PM',20:'8 PM',21:'9 PM',22:'10 PM',23:'11 PM',0:'12 AM',1:'1 AM',2:'2 AM',3:'3 AM',4:'4 AM',5:'5 AM',6:'6 AM',7:'7 AM',8:'8 AM',9:'9 AM',10:'10 AM',11:'11 AM',12: '12 PM',13:'1 PM',14:'2 PM',15:'3 PM',16: '4 PM',17:'5 PM',18:'6 PM'}
    return miltociv[militarytime]

#utility function for overallsentiment graph, its puts text over 50 characters onto
#a new line
def putstextonnewline(text):
    wordlist = text.split()
    charcount = 0
    wordcount = 0
    for word in wordlist:
        charcount = charcount + len(word)
        wordcount = wordcount + 1
        if charcount > 50:
            wordlist.insert(wordcount,'<br>')
            charcount = 0
    return ' '.join(wordlist)

#util function for converting numbered months to string months
def number_to_month(num):
    monthnum = {1:"January",2:"February",3:"March",4:"April",5:"May",
    6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",
    12:"December"}
    return monthnum[num]

def month_to_number(month):
    monthnum = {"January":1,"February":2,"March":3,"April":4,"May":5,
    "June":6,"July":7,"August":8,"September":9,"October":10,"November":11,
    "December":12}
    return monthnum[month]

#UTILITY FUNCTION
#given a dic,with the value entries as list of ints, sorts based on number in specified position in list
#for example, in the given dic, there will be a screenname mapped to a list of five ints. The first int
#is the amount of times that person was retweeted by you, the second int is the amount of times you replied to them. 
#so if i give this function a position of 1, it will get the top x people you replied to the most.
def get_top_x_values_in_dic(givendic,num,position):
     sorted_list_of_tuples = sorted(givendic.items(), key=lambda kv: kv[1][position])
     
     non_zero_sorted_list_of_tuples = []
     if len(sorted_list_of_tuples) < num:
         
         
        for tup in sorted_list_of_tuples:
            if tup[1][position] !=0:
                non_zero_sorted_list_of_tuples.append(tup)
        return non_zero_sorted_list_of_tuples
     else:
         list_of_tuples_might_have_zeros = sorted_list_of_tuples[-num:]
         for tup in list_of_tuples_might_have_zeros:
             if tup[1][position] !=0:
                non_zero_sorted_list_of_tuples.append(tup)
         return non_zero_sorted_list_of_tuples

