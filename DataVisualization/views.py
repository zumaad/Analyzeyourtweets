from django.shortcuts import render,redirect
from django.http import HttpResponse
from DataVisualization import DataModels,sentimentgraphs,interactionsgraphs,generalstatisticsgraphs,utilityfunctions
from plotly.offline import plot
from django.conf import settings
import os
from PIL import Image
import tweepy
from tweepy import TweepError
from DataVisualization import hiddenurl
import io
from io import BytesIO
import boto3

overallcloudcount = 0
negativecloudcount = 0
positivecloudcount = 0
boto_client = boto3.client(
    's3',
    aws_access_key_id=hiddenurl.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=hiddenurl.AWS_SECRET_ACCESS_KEY
)


# Create your views here.

def home_page(request):
    if request.method == 'POST':
        return redirect('/analysis')
    return render(request,'home.html')
   
        
def analysis_page(request):
    global overallcloudcount
    global negativecloudcount
    global positivecloudcount
    global boto_client
     
    if request.method == 'GET':
        return render(request, 'home.html')
    
    
    username = request.POST['twitter_handle']
    tweetcount = request.POST['number']
    timezone = request.POST['timezones']
    
    #getting the tweetbase, if the handle entered isn't an account or is protected, redirect to the homepage.
    try:
        base = DataModels.tweetzz.gettweets(username,int(tweetcount),timezone)
    except TweepError:
        errormessage = "the twitter handle you just entered was either protected or doesn't exist!"
        return render(request,'home.html',{'errormessage':errormessage})

    except ValueError:
        errormessage = "The tweetcount field can only be a Integer!"
        return render(request,'home.html',{'errormessage':errormessage})
         
    
    numberoftweetsretrieved = len(base)
    

    #creating the batches of tweets by month and day
    allbatches = DataModels.monthbatch.monthanddaybatches(base)
    #creating just month batches
    monthbatchez = DataModels.monthbatch.justmonthbatches(base)



    

    

    #creating the overall sentiment graph
    fig = sentimentgraphs.overallsentiment(allbatches)
    overallsentiment = plot(fig, output_type = 'div')

    #creating the happiest weekday graph
    
    weekday_and_monthly_sentiment = plot(sentimentgraphs.combine_monthly_sentiment_and_weekday_sentiment(base),output_type = 'div')

    

     
    
    #creating the tweet count per month graph
    data = generalstatisticsgraphs.tweetcountpermonth(allbatches)
    tweet_count_per_month = plot(data,output_type = 'div')

    #creating the tweetcount per hour/month/weekday graph.
    per_hour_weekday_month_graph = plot(generalstatisticsgraphs.tweet_per_hour_weekday_month_graph(base),output_type = 'div')

    #creating the tweetcount per hour over time graph
    perhourovertimedata = generalstatisticsgraphs.tweetperhourovertime(monthbatchez)
    perhourovertimegraph = plot(perhourovertimedata,output_type = 'div')

    #saving the wordclouds
    #problem is that sometimes there aren't enough words to generate a wordcloud,
    #so a image is not generated and you can't call save.


    
    
    

    try:
        overallwordcloud = sentimentgraphs.wordcloud_overall(base)
        final_image = BytesIO()
        overallwordcloud.save(final_image,'png')
        final_image.seek(0)
        name = 'overallwordcloud' + str(overallcloudcount) + '.png'
        # s3.Bucket(hiddenurl.bucketname).put_object(Key=name, Body=final_image)
        boto_client.upload_fileobj(final_image, hiddenurl.bucketname, name)
        path_to_overall_cloud = hiddenurl.url+ name
        
        overallcloudcount+=1
        
    except ValueError:
        path_to_overall_cloud = hiddenurl.url + 'errorpic.png'
    
    try:
        negativewordcloud = sentimentgraphs.wordcloud_negative(base)
        negative_final_image = BytesIO()
        negativewordcloud.save(negative_final_image,'png')
        negative_final_image.seek(0)
        negative_name = 'negativewordcloud' + str(negativecloudcount) + '.png'
        # s3.Bucket(hiddenurl.bucketname).put_object(Key=negative_name, Body=negative_final_image)
        boto_client.upload_fileobj(negative_final_image, hiddenurl.bucketname, negative_name)
        path_to_negative_cloud = hiddenurl.url + negative_name
        
        negativecloudcount+=1
        
    except:
        path_to_negative_cloud = hiddenurl.url + 'errorpic.png'
        
    try:
        positivewordcloud = sentimentgraphs.wordcloud_positive(base)
        positive_final_image = BytesIO()
        positivewordcloud.save(positive_final_image,'png')
        positive_final_image.seek(0)
        positive_name = 'positivewordcloud' + str(positivecloudcount) + '.png'
        # s3.Bucket(hiddenurl.bucketname).put_object(Key=positive_name, Body=positive_final_image)
        boto_client.upload_fileobj(positive_final_image, hiddenurl.bucketname, positive_name)
        path_to_positive_cloud = hiddenurl.url + positive_name
       
        positivecloudcount+=1
        
    except:
        path_to_positive_cloud = hiddenurl.url + 'errorpic.png'
    
    

    #creating retweets/favorite count per hour 
    #basically shows what time your tweets do the best,worst, etc.(how time posted
    # affects interaction with tweets).
    retweet_favorite_per_hour = plot(interactionsgraphs.retweet_fav_count_per_hour(base),output_type = 'div')


    
    #creating the "all interactions" graph
    get_all_interactions_graph = plot(interactionsgraphs.graph_all_interactions(base),output_type = 'div')

    #stacked bar graph of top summed interactions
    get_summed_interactions_graph = plot(interactionsgraphs.graph_top_summed_interactions(base),output_type = 'div')
    


    #TEXT VARIABLES---------

    #HEADERS FOR SECTIONS
    sentimentstatisticsheader = 'Sentiment Statistics (excluding retweets)'
    generaltweetstatisticsheader = 'General Tweet Statistics'
    interactionsheader = "Interactions"

    #HEADERS FOR GRAPHS 
    
    tweetcountperhour_month_weekdayheader = 'Tweet count per hour in the day,weekday,and month'
    tweetcountperhourpermonthheader = 'Tweet count per hour based on month'
    sentimentgraphheader = "sentiment of your tweets over time"
    tweetcountpermonthheader = "tweet count per month(excludes months without tweets)"
    weekdayandmonthlysentimentheader = "Sentiment of your tweets on the weekdays and months"
    wordcloudheader = "Wordcloud of your tweets based on sentiment"
    medianfavandrtheader = "median retweet and favorite count based on hour of the tweet."
    topfivespeceficinteractionsheader = 'top 5 users you interact with based on specific interactions'
    topfiveoverallheader = 'top 5 people you interact based on all interactions.'

    #EXPLANATIONS FOR GRAPHS
    rangeslidertext = "The bar above is a range slider. You can use it to effectively zoom in on a certain time, as far as picking out specific days or even hours. You do this by sliding either end of the slider. If you slide both ends until there is little space left in the middle, and then drag the middle around, you can get data about very specific dates."
    
    tweetcountperhour_month_weekdayexp = 'Displays the number of tweets you have tweeted in every hour of the day/every month/every weekday.'
    
    tweetcountperhourpermonthtext = 'Displays the number of tweets you have tweeted in any given hour for the given month. This graph probably looks like a jumbled mess but you can isolate lines by clicking on them twice and you can reveal/hide a line by clicking on it. This enables you to see interesting trends such as tweeting later in the day in the summer months compared to school months.'
    
    #OTHER
    
 

    
    

    return render(request, 'analysis.html',
    {'overallsentiment':overallsentiment,
    'sentimentgraphheader':sentimentgraphheader,
    'tweet_count_per_month':tweet_count_per_month,
    'tweetcountpermonthheader':tweetcountpermonthheader,
    'rangeslidertext':rangeslidertext,
    'sentimentstatisticsheader':sentimentstatisticsheader,
    'generaltweetstatisticsheader':generaltweetstatisticsheader,
    'weekday_and_monthly_sentiment':weekday_and_monthly_sentiment,
    'per_hour_weekday_month_graph':per_hour_weekday_month_graph,
    'perhourovertimegraph':perhourovertimegraph,
    'tweetcountperhour_month_weekdayheader':tweetcountperhour_month_weekdayheader,
    'tweetcountperhour_month_weekdayexp':tweetcountperhour_month_weekdayexp,
    'tweetcountperhourpermonthheader':tweetcountperhourpermonthheader,
    'tweetcountperhourpermonthtext':tweetcountperhourpermonthtext,
    'interactionsheader':interactionsheader,
    'retweet_favorite_per_hour':retweet_favorite_per_hour,
    'get_all_interactions_graph':get_all_interactions_graph,
    'get_summed_interactions_graph':get_summed_interactions_graph,
    'weekdayandmonthlysentimentheader':weekdayandmonthlysentimentheader,
    'wordcloudheader':wordcloudheader,
    'medianfavandrtheader':medianfavandrtheader,
    'topfivespeceficinteractionsheader':topfivespeceficinteractionsheader,
    'topfiveoverallheader':topfiveoverallheader,
    'numberoftweetsretrieved':numberoftweetsretrieved,
    'overallcloudpath':path_to_overall_cloud,
    'negativecloudpath':path_to_negative_cloud,
    'positivecloudpath':path_to_positive_cloud})

