import tweepy
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

    tot_pos = 0
    tot_neg = 0
    average_users = 200 #average number of followers a twitter user has

    analyzer = SentimentIntensityAnalyzer()

    for tweet in tweets:
        tweet_string = tweet.text.encode('ascii','ignore')
        vs = analyzer.polarity_scores(tweet_string)
        follower_count = tweet.user.followers_count
        tot_pos += vs['pos']*(follower_count / float(average_users))
        tot_neg += vs['neg']*(follower_count / float(average_users))
        #print("{:-<65} {}".format(tweet_string, str(vs)))
        #print tweet.text
        #print tweet.user.screen_name
        #print tweet.user.followers_count


print "Adjusted Predicted Movie Rating for " + movie + " : " + str(tot_pos / float(tot_neg + tot_pos))
