from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
from DataVisualization.utilityfunctions import convertmilitary
import calendar

def tweetcountpermonth(batches):
    data = []
    for month in batches:
        date = month.month
        tweetcount = 0
        for day in month.onedaylist:
            numberoftweets = len(day.daylist)
            tweetcount = tweetcount+ numberoftweets
            
      
        onemonth = go.Bar(
            x=[str(date.year) + ' - ' + str(date.month)],
            y=[tweetcount],
            name = str(date.year) + ' - ' + str(date.month)
    )
        data.append(onemonth)
    return data

def tweetcountperweekday(base):
    
    yaxis =[]
    weekdaydic = {}
    xaxis =['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for tweet in base:
        if tweet.weekday not in weekdaydic:
            weekdaydic[tweet.weekday] = 1
        else:
            weekdaydic[tweet.weekday] = weekdaydic[tweet.weekday] + 1
    for day in xaxis:
        if day in weekdaydic:
            yaxis.append(weekdaydic[day])
        else:
            yaxis.append(0)
    

    line = go.Scatter(
    x=xaxis,
    y=yaxis,
    mode = "lines + markers",
    name = 'tweet count per weekday'
    )
    return line
    

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

def tweet_per_month_irrespective_of_year(base):
    monthdic ={}
    xaxis = ['January','February','March','April','May','June','July',
    'August','September','October','November','December']
    yaxis = []

    for tweet in base:
        if calendar.month_name[tweet.month] not in monthdic:
            monthdic[calendar.month_name[tweet.month]] = 1
        else:
            monthdic[calendar.month_name[tweet.month]] = monthdic[calendar.month_name[tweet.month]] + 1
    
    for month in xaxis:
        if month in monthdic:
            yaxis.append(monthdic[month])
        else:
            yaxis.append(0)

    line = go.Scatter(
    x=xaxis,
    y=yaxis,
    mode = "lines + markers",
    name = 'tweet count per month'
    )

    return line
    


def tweet_per_hour_weekday_month_graph(base):
    weekdaytrace = tweetcountperweekday(base)
    hourtrace = tweetperhour(base)
    monthtrace = tweet_per_month_irrespective_of_year(base)
    data = [hourtrace,weekdaytrace,monthtrace]

    buttons = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Tweets per hour',
                 method = 'update',
                 args = [{'visible': [True,False,False]},
                         {'title': 'Tweets per Hour'}]),
            dict(label = 'Tweets per weekday',
                 method = 'update',
                 args = [{'visible': [False, True,False]},
                         {'title': 'Tweets per Weekday'}]),
            dict(label = 'Tweets per Month',
                 method = 'update',
                 args = [{'visible': [False, False,True]},
                         {'title': 'Tweets per Month'}])]))])           
                         
                        
                        
    layout =  dict(updatemenus = buttons, font=dict(family ='Gill Sans, Gill Sans MT, Calibri, Trebuchet MS, sans-serif', size=18))
    fig = dict(data=data, layout=layout)
    return fig



    

def tweetperhourovertime(monthbatches):
    xaxis =['9 AM','10 AM','11 AM','12 PM','1 PM','2 PM','3 PM','4 PM',
    '5 PM','6 PM','7 PM','8 PM','9 PM','10 PM','11 PM','12 AM','1 AM','2 AM',
    '3 AM','4 AM','5 AM','6 AM','7 AM','8 AM']
    data = []

    
    

    for month in monthbatches:
        date = month.month
        yaxis = []
        hourdic = {}
        for tweet in month.onedaylist:
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
        name = str(date.year) + '-' + str(date.month)
        )
        data.append(line)
    return data
