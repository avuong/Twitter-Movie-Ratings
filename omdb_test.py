import omdb
import tweepy
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

if __name__ == '__main__':

    movie = raw_input("Enter movie title: ")

    # Current issue with movie not being the right one
    # Possible to seearch for title and get IMDb id returned to determine which one you want
    options = omdb.search(movie)
    imdb_id = 0
    year = 0
    for option in options:
        if int(option["year"]) > year:
            year = int(option["year"])
            imdb_id = option["imdb_id"]

    res = omdb.request(i=imdb_id)
    data = res.json()
    if data["Response"] == "False":
        exit()

    # print data['Actors'].split(',')
    actors = [a.strip() for a in data["Actors"].split(',')]
    directors = [d.strip() for d in data["Director"].split(',')]

    auth = tweepy.OAuthHandler("Bvo4QBYXneS8Z4NgXRpPltrHw", "qYU60CVlJyoaJojB9QHoVZP2I37lnvwIZWP9cYnv5KsPGFIn7z")
    auth.set_access_token("271137941-zrWtZjcVbDsuaGwvwg3rz4wRJP6er5scmqTAOxct", "vGN7VQWHc86YtYX8Q8QVRnnhD5edgUgezRDyGzNkUYrMW")

    api = tweepy.API(auth)

    # user = api.get_user(screen_name = actors[1])

    # tweets = []
    actor_sentiment = []
    average_users = 200
    analyzer = SentimentIntensityAnalyzer()

    for i in xrange(len(actors)):
        # tweets.append(api.search(q=actors[i], count = 100))
        tweets = api.search(q=actors[i], count = 100)
        tot_pos = 0
        tot_neg = 0
        for tweet in tweets:
            tweet_string = tweet.text.encode('ascii', 'ignore')
            vs = analyzer.polarity_scores(tweet_string)
            follower_count = tweet.user.followers_count
            tot_pos += vs['pos']*(follower_count/float(average_users))
            tot_neg += vs['neg']*(follower_count/float(average_users))

        score = 0
        try:
            score = tot_pos / float(tot_neg+tot_pos)
        except ZeroDivisionError:
            score = 0
        print "Adjusted Predicted Actor Rating for " + actors[i] + " : " + str(score)

    for i in xrange(len(directors)):
        tweets = api.search(q=directors[i], count=100)
        tot_pos = 0
        tot_neg = 0
        for tweet in tweets:
            tweet_string = tweet.text.encode('ascii', 'ignore')
            vs = analyzer.polarity_scores(tweet_string)
            follower_count = tweet.user.followers_count
            tot_pos += vs['pos']*(follower_count/float(average_users))
            tot_neg += vs['neg']*(follower_count/float(average_users))

        score = 0
        try:
            score = tot_pos / float(tot_neg+tot_pos)
        except ZeroDivisionError:
            score = 0
        print "Adjusted Predicted Actor Rating for " + directors[i] + " : " + str(score)


    #   results = api.search_users(actors[i])
    #   for r in results:
    #  if r['verified'] == True:
    # print actors[i] + ": " + r['screen_name']
    # print api.get_user(r['id'])
