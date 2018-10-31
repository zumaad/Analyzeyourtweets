from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
from DataVisualization.utilityfunctions import convertmilitary,get_top_x_values_in_dic
from numpy import median


#INTERACTIONS SECTION
def retweet_fav_count_per_hour(base):
    xaxis =['9 AM','10 AM','11 AM','12 PM','1 PM','2 PM','3 PM','4 PM',
    '5 PM','6 PM','7 PM','8 PM','9 PM','10 PM','11 PM','12 AM','1 AM','2 AM',
    '3 AM','4 AM','5 AM','6 AM','7 AM','8 AM']

    favoriteaxis = []
    retweetaxis = []

    rt_fav_hour_dic = {}

    for tweet in base:
        if convertmilitary(tweet.time.hour) not in rt_fav_hour_dic:
            if tweet.retweetofwhom == None:
                rt_fav_hour_dic[convertmilitary(tweet.time.hour)] = {"favorite":[tweet.favoritecount],"retweet":[tweet.retweetcount]}
        else:
            if tweet.retweetofwhom == None:
                rt_fav_hour_dic[convertmilitary(tweet.time.hour)]["favorite"].append(tweet.favoritecount)
                rt_fav_hour_dic[convertmilitary(tweet.time.hour)]["retweet"].append(tweet.retweetcount)
    
    for hour in xaxis:
        if hour in rt_fav_hour_dic:
            favoriteaxis.append(median(rt_fav_hour_dic[hour]["favorite"]))
            retweetaxis.append(median(rt_fav_hour_dic[hour]["retweet"]))
        else:
            favoriteaxis.append(0)
            retweetaxis.append(0)

    favorites_trace = go.Bar(
        x = xaxis,
        y = favoriteaxis,
        name = "median favorite count"
    )

    retweets_trace = go.Bar(
        x = xaxis,
        y = retweetaxis,
        name = "median retweet count"

    )

    data = [favorites_trace, retweets_trace]
    layout = go.Layout(
        barmode='group'
    )
    
    

    return go.Figure(data=data, layout=layout)

def retrieve_attribute(tweet,retrievewhat):
    if retrievewhat == "retweet":
        return tweet.retweetofwhom
    elif retrievewhat == "reply":
        return tweet.replyto
    elif retrievewhat == "quote":
        return tweet.quoteof


def get_interactions(base):
    
    whichone_dic = {}
    for tweet in base:
        if tweet.retweetofwhom:
            if tweet.retweetofwhom not in whichone_dic:
                whichone_dic[tweet.retweetofwhom] = [1,0,0,0,0]
            else:
                whichone_dic[tweet.retweetofwhom][0] = whichone_dic[tweet.retweetofwhom][0]+ 1
        
        #if someone starts tweet with an @ it counts as a reply and a mention, it should only be a mention.
        #with this extra logic, if the person you replied to is also in the mentions, it doesn't add to the reply count for that person.
        #but you can still reply to someone and @people and it will accurately add the count in the mentions if clause.
        #the problem is that before, twitter used to automatically put @thepersonyouarereply so a lot of replies from back
        #when twitter used to do that are now not counted as replies according to the logic in this code.
        if tweet.replyto:
            flag = True
            for dic in tweet.mentions:
                
                if tweet.replyto ==  dic['screen_name']:
                    
                    flag = False
                    break
            if flag:
                if tweet.replyto not in whichone_dic:
                    whichone_dic[tweet.replyto] = [0,1,0,0,0]
                else:
                    whichone_dic[tweet.replyto][1] = whichone_dic[tweet.replyto][1] + 1

        if tweet.quoteof:
            if tweet.quoteof not in whichone_dic:
                whichone_dic[tweet.quoteof] = [0,0,1,0,0]
            else:
                whichone_dic[tweet.quoteof][2] = whichone_dic[tweet.quoteof][2] + 1
        
        if tweet.mentions:
            if not tweet.retweetofwhom:
                for dic in tweet.mentions:
                    if dic['screen_name'] not in whichone_dic:
                        whichone_dic[dic['screen_name']] = [0,0,0,1,0]
                    else:
                        whichone_dic[dic['screen_name']][3] = whichone_dic[dic['screen_name']][3] + 1


    #summing up the interactions and adding to the "summed interactions" index in the value list in the dic.
    for name in whichone_dic:
        whichone_dic[name][4] = whichone_dic[name][0] + whichone_dic[name][1] + whichone_dic[name][2] + whichone_dic[name][3]
    
    return whichone_dic


#this method is retarded, need to abstract.
#creates bar graph for interactions.
def graph_all_interactions(base):

    dic_of_names_and_interaction_counts = get_interactions(base)

    top_five_people_retweeted = get_top_x_values_in_dic(dic_of_names_and_interaction_counts,5,0)
    top_five_people_replied_to = get_top_x_values_in_dic(dic_of_names_and_interaction_counts,5,1)
    top_five_people_quoted = get_top_x_values_in_dic(dic_of_names_and_interaction_counts,5,2)
    top_five_people_mentioned = get_top_x_values_in_dic(dic_of_names_and_interaction_counts,5,3)
    
   
   

    retweet_x_axis = [inner_list[0] for inner_list in top_five_people_retweeted]
    retweet_y_axis = [inner_list[1][0] for inner_list in top_five_people_retweeted]

    quote_x_axis = [inner_list[0] for inner_list in top_five_people_quoted]
    quote_y_axis = [inner_list[1][2] for inner_list in top_five_people_quoted]

    reply_x_axis = [inner_list[0] for inner_list in top_five_people_replied_to]
    reply_y_axis = [inner_list[1][1] for inner_list in top_five_people_replied_to]

    mention_x_axis = [inner_list[0] for inner_list in top_five_people_mentioned]
    mention_y_axis = [inner_list[1][3] for inner_list in top_five_people_mentioned]
    
    

    retweet_trace = go.Bar(
        x = retweet_x_axis,
        y = retweet_y_axis,
        name = "top 5 people you retweeted",
        marker=dict(
        color='rgb(0,204,102)'
    )
    )

    reply_trace = go.Bar(
        x = reply_x_axis,
        y = reply_y_axis,
        name = "top 5 people you replied to",
        marker=dict(
        color='rgb(51,51,255)'
    )
    )

    quote_trace =  go.Bar(
        x = quote_x_axis,
        y = quote_y_axis,
        name = "top 5 people you quoted",
        marker=dict(
        color='rgb(152,51,255)'
    )
        
    )

    mention_trace = go.Bar(
        x = mention_x_axis,
        y = mention_y_axis,
        name = "top 5 people you mentioned",
        marker=dict(
        color='rgb(204,0,0)'
    )
    )

    

    data = [retweet_trace,reply_trace,quote_trace,mention_trace]
    buttons = list([
    dict(type="buttons",
         active=-1,
         buttons=list([
            dict(label = 'Top 5 People You Retweet',
                 method = 'update',
                 args = [{'visible': [True,False,False,False]},
                         {'title': 'Top 5 People You Retweet'}]),
            dict(label = 'Top 5 People You Reply To',
                 method = 'update',
                 args = [{'visible': [False,True,False,False]},
                         {'title': 'Top 5 People You Reply To'}]),

            dict(label = 'Top 5 People You Quote',
                 method = 'update',
                 args = [{'visible': [False,False,True,False]},
                         {'title': 'Top 5 People You Quote'}]),

            dict(label = 'Top 5 People You mention',
                 method = 'update',
                 args = [{'visible': [False,False,False,True]},
                         {'title': 'Top 5 People You mention'}])]))])        
                         
                        
                        
    layout =  dict(updatemenus = buttons, font=dict(family ='Gill Sans, Gill Sans MT, Calibri, Trebuchet MS, sans-serif', size=18))
    fig = dict(data=data, layout=layout)
    
    return fig

def graph_top_summed_interactions(base):
    dic_of_names_and_interaction_counts = get_interactions(base)
    top_five_people_interacted_with_overall = get_top_x_values_in_dic(dic_of_names_and_interaction_counts,5,4)
    
    overall_interactors_x_axis = [inner_list[0] for inner_list in top_five_people_interacted_with_overall]

    #creating the stacked bar graph.First i have to create individual traces for each component of the stacked graph
    #and then reference that trace which references the individual traces in the buttons variable.
    retweet_part_of_overall_trace = go.Bar(
        x = overall_interactors_x_axis,
        y = [inner_list[1][0] for inner_list in top_five_people_interacted_with_overall],
        name = "# times you retweeted them"

    )

    reply_part_of_overall_trace = go.Bar(
        x = overall_interactors_x_axis,
        y = [inner_list[1][1] for inner_list in top_five_people_interacted_with_overall],
        name = "# times you replied to them"

    )

    quote_part_of_overall_trace = go.Bar(
        x = overall_interactors_x_axis,
        y = [inner_list[1][2] for inner_list in top_five_people_interacted_with_overall],
        name = "# times you quoted them"

    )

    mention_part_of_overall_trace = go.Bar(
        x = overall_interactors_x_axis,
        y = [inner_list[1][3] for inner_list in top_five_people_interacted_with_overall],
        name = "# times you mentioned them"

    )

    data = [retweet_part_of_overall_trace,reply_part_of_overall_trace,quote_part_of_overall_trace,mention_part_of_overall_trace]
    layout = go.Layout(
    barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    return fig
