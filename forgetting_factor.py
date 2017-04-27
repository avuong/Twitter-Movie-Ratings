import tweepy
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from datetime import datetime

if __name__ == '__main__':

    #setting up authentication
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    if(api.verify_credentials):
        print 'Login Successful'

    #search for tweets with movie keyword
    movie = "Hidden Figures"
    keyword = movie + " movie"
    tweets = api.search(q=keyword, count = 100)

    #get current time
    ts = time.time()
    curr_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    fmt = '%Y-%m-%d %H:%M:%S'
    curr_time = datetime.strptime(str(curr_time), fmt)

    for tweet in tweets:
        date_posted = tweet.created_at
        tweet_text= tweet.text

        #subtract tweet time with current time
        tweet_time = datetime.strptime(str(date_posted), fmt)
        seconds_diff = (curr_time-tweet_time).total_seconds()
        minutes_diff = seconds_diff / 60

        #separate weights based on number of minutes from current time
        if (minutes_diff <= 720):
            print "Tier 1 : " + tweet_text
        elif (minutes_diff > 720 and minutes_diff <= 1440):
            print "Tier 2 : " + tweet_text
        elif (minutes_diff > 1440):
            print "Tier 3 : " + tweet_text
