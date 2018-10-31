from numpy import median
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
from wordcloud import WordCloud
from DataVisualization.utilityfunctions import month_to_number


def happiestweekday(base):
    
    weekdaydic ={}
    for tweet in base:
        if tweet.weekday not in weekdaydic:
            if tweet.sentiment != 0:
                weekdaydic[tweet.weekday] = [tweet.sentiment]
            else: 
                weekdaydic[tweet.weekday] =[]
        else:
            if tweet.sentiment != 0:
                weekdaydic[tweet.weekday].append(tweet.sentiment)
    
                 
    #if the value is not an empty list, cause then median can't work.
    for k,v in weekdaydic.items():
        if len(v) > 0:
            weekdaydic[k] = median(v)
        else:
            weekdaydic[k] = 0
    return weekdaydic


def happiestweekdaygraph(happiestweekdaydata):
    xlist =['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    xaxis = []
    yaxis =[]

    for day in xlist:
        if day in happiestweekdaydata and happiestweekdaydata[day] != 0:
            xaxis.append(day)
            yaxis.append(happiestweekdaydata[day])
    
    linegraph = go.Scatter(
    x=xaxis,
    y=yaxis,
    mode = "lines + markers",
    name = 'sentiment by weekday'
    )
    return linegraph
    

    
#if a day had all zero sentiment tweets, it isn't included
def overallsentiment(batches):
    xaxis =[]
    yaxis =[]
    textlist = []
    for month in batches:
        for day in month.onedaylist:
            if day.getmedian() != 'no non zero sentiment scores in this day':
                xaxis.append(day.day)
                yaxis.append(day.getmedian())
                textlist.append(day.gettext())
        
       

    line = go.Scatter(
    x=xaxis,
    y=yaxis,
    mode = "markers",
    text = textlist
    )

    layout = dict(paper_bgcolor='rgba(255,255,255,1.0)',
    plot_bgcolor='rgba(255,255,255,1.0)',
    
    xaxis = dict(
        range = [str(xaxis[-1]),str(xaxis[0])],
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

    data = [line]
    fig = dict(data=data, layout=layout)
    return fig

#raising the value error so it can be handled by the outer handler in views.py
def wordcloud_overall(base):
    text = ''
    for tweet in base:
        text = text + tweet.text

    try:
        wordcloud = WordCloud(width = 300,height = 300).generate(text)
        image = wordcloud.to_image()
        return image
    except ValueError:
        raise
    
def wordcloud_negative(base):
    text = ''
    for tweet in base:
        if tweet.sentiment < -.3:
            text = text + tweet.text

    try:
        wordcloud = WordCloud(width = 300,height = 300).generate(text)
        image = wordcloud.to_image()
        return image
    except ValueError:
        raise


def wordcloud_positive(base):
    text = ''
    for tweet in base:
        if tweet.sentiment > .3:
            text = text + tweet.text

    try:
        wordcloud = WordCloud(width = 300,height = 300).generate(text)
        image = wordcloud.to_image()
        return image
    except ValueError:
       raise

def monthly_sentiment_irrespective_of_year(base):
    monthdic = {}
    for tweet in base:
        if tweet.month not in monthdic:
            if tweet.sentiment != 0:
                monthdic[tweet.month] = [tweet.sentiment]
            else: 
                monthdic[tweet.month] =[]
        else:
            if tweet.sentiment != 0:
                monthdic[tweet.month].append(tweet.sentiment)

                
    #if the value is not an empty list, cause then median can't work.
    for k,v in monthdic.items():
        if len(v) > 0:
            monthdic[k] = median(v)
        else:
            monthdic[k] = 0
    xlist =['January','February','March','April','May','June','July','August','September','October','November','December']
    xaxis = []
    yaxis =[]

    

    for month in xlist:
        if month_to_number(month) in monthdic and monthdic[month_to_number(month)] != 0:
            xaxis.append(month)
            yaxis.append(monthdic[month_to_number(month)])
    
    linegraph = go.Scatter(
    x=xaxis,
    y=yaxis,
    mode = "lines + markers",
    name = 'sentiment by month'
    )
    return linegraph
    
def combine_monthly_sentiment_and_weekday_sentiment(base):
    monthlysentiment = monthly_sentiment_irrespective_of_year(base)
    weekdaysentiment = happiestweekdaygraph(happiestweekday(base))
    data = [weekdaysentiment,monthlysentiment]

    
    buttons = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Sentiment per month',
                 method = 'update',
                 args = [{'visible': [False,True]},
                         {'title': 'Sentiment per month'}]),
            dict(label = 'Sentiment per weekday',
                 method = 'update',
                 args = [{'visible': [True,False]},
                         {'title': 'Sentiment per weekday'}])]))])        
                         
                        
                        
    layout =  dict(updatemenus = buttons, font=dict(family ='Gill Sans, Gill Sans MT, Calibri, Trebuchet MS, sans-serif', size=18))
    fig = dict(data=data, layout=layout)
    return fig
    
    