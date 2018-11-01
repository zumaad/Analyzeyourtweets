# Analyzeyourtweets
A website where you can type your twitter handle and have your tweets analyzed.


## What Exactly Does the application Do?

  The general purpose of this web-app is to return interesting data/statistics about your tweets in three
broad categories: Sentiment data, general data, and Interactions data.

### Sentiment Data

  Sentiment data refer to any data that can be tied to the "sentiment" of a tweet. The sentiment of a 
tweet is roughly how positive or negative it is. For example: "I hate bananas. They are very bad!" would
have a pretty negative sentiment score. There's plenty of interesting data that can linked to the sentiment of tweets,
such as the frequency of certain words below a certain sentiment threshold(the wordcloud displayed on this site), or 
how any interactions you get with a tweet based on sentiment(do emotionally charged tweets, either negative or positive get more interactions?),
or even the time you tweeted and whether that has any correlation with how negative or positive your tweet was (the graph that plots sentiment per weekday).
                
### General Data

  General data is basically any data/statistics that doesn't have to do with tweet sentiment or
interactions with a tweet. Examples of what is displayed in the site include a graph that plots
tweets per hour which models your tweeting behaviour throughout the day and shows the hours you tweet the most
or least, tweets per month, tweets per hour based on month, and more. 
                
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
