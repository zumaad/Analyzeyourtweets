# Analyzeyourtweets
A website where you can type your twitter handle and have your tweets analyzed. This README will describe some of the functionality of the web app by taking you through the process of turning a bunch of tweets to a simple graph plotting some desired information.


## What Exactly Does the application Do?

  The general purpose of this web-app is to return interesting data/statistics about your tweets in three
broad categories: Sentiment data, general data, and Interactions data.

### Sentiment Data

  Sentiment data refer to any data that can be tied to the "sentiment" of a tweet. The sentiment of a 
tweet is roughly how positive or negative it is. For example: "I hate bananas. They are very bad!" would
have a pretty negative sentiment score. There's plenty of interesting data that can linked to the sentiment of tweets,
such as the frequency of certain words below a certain sentiment threshold(the wordcloud displayed on this site), or 
how any interactions you get with a tweet based on sentiment(do emotionally charged tweets, either negative or positive get more interactions? soon to be implemented),
or even the time you tweeted and whether that has any correlation with how negative or positive your tweet was (the graph that plots sentiment per weekday). The sentiment "score" of a tweet was retrieved by using Vader,a sentiment analysis tool that was made for analyzing social media text. If you want to know more about Vader and it's aproach to sentiment analysis, here is 
a writup by its authors http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf. 
                
### General Data

  General data is basically any data/statistics that doesn't have to do with tweet sentiment or
interactions with a tweet. Examples of what is displayed in the site include a graph that plots
tweets per hour which models your tweeting behaviour throughout the day and shows the hours you tweet the most
or least, tweets per month, tweets per hour based on month (allows you to see trends in your tweeting behavior such as tweeting later in the day in the summer months if you are still in school), and more. 
                
### Interactions Data

  Interactions Data is data that deals with quotes,retweets,mentions,favorites, and replies. Interactions go both ways,
you can interact with others, and others can interact with you. Unfortunately, twitter makes it 
hard/impossible (unless you pay) to get information about tweets you favorite and the interactions
with your tweets other than the retweet/favorite count of a tweet. As such, this website returns statistics
based on the retweet/favorite count of your tweets and the people you interact with (reply,quote,mention,and retweet). Examples of such data include but are definitely not limited to: the top 5 people you interact with and the amount of favorites/retweets you get based on time in the hour posted - this shows you what time to post your tweets if you want the best chance of getting the most interactions.



## How does it do it?
There are 5 main steps to get from the tweets you see on screen 

![picture of a tweet](tweet.png)

to a graph like this

![picture of a graph](graph.png)

The 5 steps are:
- getting the tweets
- cleaning the tweets
- modeling the tweets
- creating axes of the graph
- Output!

### getting the tweets

~~~~
def gettweets(name,num,timezone):
        tweets = tweepy.Cursor(api.user_timeline,screen_name = name,tweet_mode = 'extended').items(num)
        tweetlist =[]
        
        for tweet in tweets:
                mytweet = tweetzz(timezone,tweet,name)
                tweetlist.append(mytweet)
        
        return tweetlist
~~~~
There are parts of this code that will be explained later. This is the way I get tweets. The first line after the method declaration is a method call from the tweepy library (discussed below) that makes http requests to the twitter api and gets data back in json form. It then parses that data and puts it in a object that models a tweet. api.user_timeline() returns an iterable which has a bunch of those "tweet" objects which I then extract and use to create my own model of a tweet object which is of class tweetzz. Those new tweet objects (mine) are then added to a list for later reference. 

### cleaning a tweet
~~~~
def cleansentence(tweet):
    dirtytweet = tweet.split(' ')
    return ' '.join([word for word in dirtytweet if not word.startswith('@') and not word.startswith('RT') and not word.startswith('http')])
~~~~

This methods cleans a tweet by building a string without any of the "dirty" elements on the tweet that muddle it's meaning 
when analyzing sentiment/outputing the text. When a user retweets a tweet, the text that tweepy returns has something along the lines of RT @handle blah blah blah. When it comes to analyzing the sentiment of the tweet you want the tweet to have less/none of these symbols which have either no meaning or a unintuitive/inapplicable meaning to the sentiment analyzer which can make the score it returns incorrect. This also applies when a user links something or mentions someone, etc. 


### modeling the tweets

The tweet object that tweepy returns has a TON of data,and some redundant data,in it as thats what the twitter api returns when you query it. But,I don't need all that it returns so I needed to extract the relevant bits and use that to model my own tweet object which would allow me a convenient way to get information that I need.

This is the model of a typical tweet object that I ended up with:
~~~~
class tweetzz():
    def __init__(self,timezone,tweetobj,name):
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
~~~~
The fields are pretty self-explanatory. They record the time the tweet was posted,the name of the person who tweeted it, and whether the tweet belongs to an interaction such as a retweet,quote,reply,mention. With this model, it was easy to get the information I needed without having to repeat the logic to get every attribute from the tweepy tweet model everytime I need it.

### creating axes of graphs
 Most of the output is in the form of graphs. I used a Data Visualization library for python called plotly which allows you to generate many different kinds of graphs with plenty of customization. For the graphs I generated, the core process was the same: generate the x and y axis, and then plot. Now, ofcourse, depending on the data I wanted, generating axes was different graph to graph. I will illustrate the process using a simple example. For more complicated graphs/the rest of the data visualization, feel free to check out the .py files in the DataVisualization folder.
 
 Here is a simple example from the tweets per hour graph you saw at the beginning of this README:
 
 ~~~
 def tweetperhour(base):
    hourdic ={}
    xaxis =['9 AM','10 AM','11 AM','12 PM','1 PM','2 PM','3 PM','4 PM',
    '5 PM','6 PM','7 PM','8 PM','9 PM','10 PM','11 PM','12 AM','1 AM','2 AM',
    '3 AM','4 AM','5 AM','6 AM','7 AM','8 AM']
    yaxis =[]
    for tweet in base:
        if convertmilitary(tweet.time.hour) not in hourdic:
            hourdic[convertmilitary(tweet.time.hour)] = 1
        else:
            hourdic[convertmilitary(tweet.time.hour)] = hourdic[convertmilitary(tweet.time.hour)] + 1
    for hour in xaxis:
        if hour in hourdic:
            yaxis.append(hourdic[hour])
        else:
            yaxis.append(0)
     
    line = go.Scatter(
    x=xaxis,
    y=yaxis,
    mode = "lines + markers",
    name = 'tweet count per hour'
    )

    return line
~~~~

As you can the x axis is created in the x axis variable as a simple list of all the hours in the day. In this case, the x axis is static and you know it before hand so its very easy to create it. In some of the other graphs (top 5 people you interact with the most) the x axis is not known before hand and its not static. On the other hand, the y axis is never known beforehand and it has to be computed. To create the y axis for this graph, I iterate through the tweets I have collected (passed in as argument "base") and build a dictionary that maps the hours in a day to the current # of tweets seen in that hour. Once this map is created, I take the hours present in the x - axis and get the corresponding values (as the hours in the day present in the x-axis are also the keys of the map I just created). Technically, I could also just iterate through the dictionary and use whatever key,value pair comes up and stick those in the x axis and y axis as I go along, but the order would be all wacky and I want the hours to be displayed in chronological order.

This process of generating the x-axis and y-axis by iterating through the tweet base is in every single graph, of which the difficulty depends on what information I am trying to get.

### Output!

This part is taken care of by a Data Visualization library available in python called Plotly. Its an excellent tool for generating graphs and offers a ton of amazing customizations to create incredibly rich and informative graphs. In the previous example,the output was generated by creating a scatter plot with the x and y axis arguments as I defined them earlier. Here is the code:

~~~~
line = go.Scatter(
    x=xaxis,
    y=yaxis,
    mode = "lines + markers",
    name = 'tweet count per hour'
    )
~~~~

As for how you actually see this graph this graph in the web interface, plotly conveniently has an option to output the graph as html.


### Software used
