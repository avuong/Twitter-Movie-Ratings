import tweepy
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from datetime import datetime

#check user tweets to see if they always tweet positively
#or negatively to ignore
def ignore_check(tweet_author_id):

            IGNORE_BOUNDARY_POS = 1.8
            IGNORE_BOUNDARY_NEG = -1.8

            #get user screen name
            user = api.get_user(tweet_author_id)
            print user.screen_name

            #get users recent tweets and calculate the sentiment of
            #the users recent tweets
            #make sure not too much near the extremes
            #this is to ignore users that are tweeting to positively or negatively
            tweets2 = api.user_timeline(id=tweet_author_id, count=users_tweet_count)
            compound_count = 0 #reset compound_count for next user
            for tweet2 in tweets2:
                tweet_text2 = tweet2.text.encode('ascii','ignore')
                #print tweet.text.encode('ascii','ignore')
                vs = analyzer.polarity_scores(tweet_text2)
                #print("{:-<65} {}".format(tweet_text2, str(vs)))
                compound_count += vs['compound']

            compound_average = float(compound_count)/users_tweet_count

            #ignore if tweeter is too positive or negative
            #based on last twenty tweets sentiment average
            if compound_average > 1.8 or compound_average < -1.8:
                #print "Ignore user"
                #print "User average tweet sentiment: " + str(compound_average)
                return true; #return true if we need to ignore user

            return false #return false if we don't need to ignore user


if __name__ == '__main__':

    #setting up authentication
    consumer_key = "hPUwcXRKUvnsgaW2rXgBD3XmQ"
    consumer_secret = "Y43JkP1swTeScCiviBbCKwkIEwwKN1rYbUEdWc5yuw8QtzUdv5"
    access_token = "824001893089296386-Mv8UqQW6ICGOZuv4U5nJDeV4mppnlMt"
    access_token_secret = "3kXgdluBregjHu4SyTfK47ecJEkjlW5tpLDuLhkaUqBf7"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    TIER_ONE_FACTOR = 720;
    TIER_TWO_FACTOR = 1440;
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

    analyzer = SentimentIntensityAnalyzer()
    compound_count = 0
    users_tweet_count = 20
    for tweet in tweets:
        date_posted = tweet.created_at
        tweet_text = tweet.text.encode('ascii','ignore')
        tweet_author_id = tweet.user.id

        ignore_check(tweet_author_id)
        #subtract tweet time with current time
        tweet_time = datetime.strptime(str(date_posted), fmt)
        seconds_diff = (curr_time-tweet_time).total_seconds()
        minutes_diff = seconds_diff / 60

        '''
        #separate weights based on number of minutes from current time
        if (minutes_diff <= TIER_ONE_FACTOR):
            print "Tier 1 : " + tweet_text
        elif (minutes_diff > TIER_ONE_FACTOR and minutes_diff <= TIER_TWO_FACTOR):
            print "Tier 2 : " + tweet_text
        elif (minutes_diff > TIER_TWO_FACTOR):
            print "Tier 3 : " + tweet_text
        '''
