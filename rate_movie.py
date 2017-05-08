from flask import Flask, request, render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os, tweepy, json, time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import omdb
import requests, re
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)
key = os.urandom(24)
app.config['SECRET_KEY'] = key

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
youtube_api_key = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class ReusableForm(Form):
	name = TextField('Name:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])

def search_movie():
	form = ReusableForm(request.form)

	print form.errors
	if request.method == 'POST':
		movie_name = request.form['name']

		if form.validate():
			compute_rating(movie_name)
		else:
			flash('All form fields are required.')

	return render_template('movie_form.html', form=form)

def compute_rating(movie):

    flash('Movie Searched: ' + movie)

    if(api.verify_credentials):
        print 'Login Successful'
    else:
        exit()

    #search for tweets with movie keyword
    keyword = movie + " movie"
    print "Getting movie Tweets..."
    movie_score = get_score(keyword, 100)
    print "Getting actors ratings..."
    actors_scores, directors_scores, outside_ratings = get_actor_rating(movie)
    print "Getting YouTube trailer ratings..."
    youtube_score = get_trailer_rating(movie)

    print "Movie Score: " + str(movie_score)
    flash("Movie Score: " + str(movie_score))

    average_actor_score = 0
    # flash("Actors")
    for score in actors_scores:
        # flash(score[0] + ": " + str(score[1]))
        print score[0] + ": " + str(score[1])
        average_actor_score += score[1]
    average_actor_score /= len(actors_scores)
    flash("Average actor score: " + str(average_actor_score))

    average_director_score = 0
    # flash("Directors")
    for score in directors_scores:
        # flash(score[0] + ": " + str(score[1]))
        print score[0] + ": " + str(score[1])
        average_director_score += score[1]
    average_director_score /= len(directors_scores)
    flash("Average director score: " + str(average_director_score))

    print "YouTube score: " + str(youtube_score)
    flash("YouTube score: " + str(youtube_score))

    #Final Score
    #50% movie tweets
    #10% director
    #20% actors
    #20% youtube

    final_score = movie_score*.5 + \
        average_actor_score*.2 + \
        youtube_score*.2 + \
        average_director_score*.1

    print "Our Final Score: " + str(final_score)
    flash("Our Final Score: " + str(final_score))

    tot_score = 0
    for rating in outside_ratings:
        flash(rating["Source"] + ": " + rating["Value"])
        print rating["Source"] + ": " + rating["Value"]
        if rating["Source"] == "Internet Movie Database":
            num, denom = rating["Value"].split('/')
            tot_score += float(num)/float(denom)
        elif rating["Source"] == "Rotten Tomatoes":
            score = int(rating["Value"].strip('%'))
            tot_score += float(score)/100
        elif rating["Source"] == "Metacritic":
            num, denom = rating["Value"].split('/')
            tot_score += float(num)/float(denom)

    if len(outside_ratings) != 0:
        print "Average Outside Source Rating: " + str(tot_score/len(outside_ratings))
        flash("Average Outside Source Rating: " + str(tot_score/len(outside_ratings)))

def get_score(keyword, count=100):
    print "Getting score for " + keyword + "..."

    TIER_ONE_FACTOR = 720
    TIER_TWO_FACTOR = 1440

    tweets = api.search(q=keyword, count = count)

    tot_pos = 0
    tot_neg = 0

    analyzer = SentimentIntensityAnalyzer()

    #get current time
    ts = time.time()
    curr_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    fmt = '%Y-%m-%d %H:%M:%S'
    curr_time = datetime.strptime(str(curr_time), fmt)

    tweet_weight = 1
    for tweet in tweets:
        date_posted = tweet.created_at
        tweet_string = tweet.text.encode('ascii','ignore')
        tweet_author_id = tweet.user.id

        # if ignore_check(tweet_author_id):
            # print "Ignored"
            # continue

        tweet_time = datetime.strptime(str(date_posted), fmt)
        seconds_diff = (curr_time-tweet_time).total_seconds()
        minutes_diff = seconds_diff / 60

        #separate weights based on number of minutes from current time
        if (minutes_diff <= TIER_ONE_FACTOR):
            tweet_weight = 1
        elif (minutes_diff > TIER_ONE_FACTOR and minutes_diff <= TIER_TWO_FACTOR):
            tweet_weight = 0.5
        elif (minutes_diff > TIER_TWO_FACTOR):
            tweet_weight = 0.25

        vs = analyzer.polarity_scores(tweet_string)

        if vs['compound'] > 0.8 or vs['compound'] < -0.8:
            if ignore_check(tweet_author_id):
                print "Ignored"
                continue

        tot_pos += vs['pos']*tweet_weight
        tot_neg += vs['neg']*tweet_weight

    score = 0
    try:
        score = tot_pos / float(tot_neg + tot_pos)
    except ZeroDivisionError:
        score = 0

    return score

def get_actor_rating(movie):
    #Get imdb movie id
    options = omdb.search(movie)
    imdb_id = 0
    year = 0
    #simply find most recent movie with the title
    for option in options:
        if int(option["year"]) > year:
            year = int(option["year"])
            imdb_id = option["imdb_id"]

    res = omdb.request(i=imdb_id)
    data = res.json()
    if data["Response"] == "False":
        print "Movie not found"
        exit()

    actors = [a.strip() for a in data["Actors"].split(',')]
    directors = [d.strip() for d in data["Director"].split(',')]

    actor_scores = []
    director_scores = []

    for i in xrange(len(actors)):
        actor_scores.append((actors[i], get_score(actors[i], 100)))

    for i in xrange(len(directors)):
        director_scores.append((directors[i], get_score(directors[i], 100)))

    return actor_scores, director_scores, data["Ratings"]

def ignore_check(tweet_author_id):
    print "Running ignore check..."

    analyzer = SentimentIntensityAnalyzer()

    IGNORE_BOUNDARY_POS = 0.8
    IGNORE_BOUNDARY_NEG = -0.8
    users_tweet_count = 20 #check last # tweets

    #get users recent tweets and calculate the sentiment average
    tweets2 = api.user_timeline(id=tweet_author_id, count=users_tweet_count)
    compound_count = 0 #reset compound_count for next user
    for tweet2 in tweets2:
        tweet_text2 = tweet2.text.encode('ascii','ignore')
        vs = analyzer.polarity_scores(tweet_text2)
        compound_count += vs['compound']

    compound_average = float(compound_count)/users_tweet_count

    #ignore if tweeter is too positive or negative
    if compound_average > IGNORE_BOUNDARY_POS or compound_average < IGNORE_BOUNDARY_NEG:
        return True; #return true if we need to ignore user

    return False #return false if we don't need to ignore user

def get_trailer_rating(movie):
    response = requests.get("https://www.googleapis.com/youtube/v3/" \
                        "search?part=snippet&q="+ movie + "Trailer" + "&key=" + youtube_api_key)

    search_data = response.json()
    total_dislikes = 0
    total_likes = 0
    #default get 3 results back
    for i in range(0,3):
        video_id = search_data['items'][i]['id']['videoId'] #video ID of movie Ex.)"LKFuXETZUsI" for Moana
        # print video_id

        response = requests.get("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=" \
                                    + video_id + "&maxResults=50&key=" + youtube_api_key)

        trailer_data = response.json()

        dislike_count = trailer_data['items'][0]['statistics']['dislikeCount']
        like_count = trailer_data['items'][0]['statistics']['likeCount']
        print "Dislike count is " + str(dislike_count)
        print "Like count is " + str(like_count)

        total_dislikes += int(dislike_count)
        total_likes += int(like_count)

    trailer_rating = 0
    try:
        trailer_rating = float(total_likes)/(total_dislikes + total_likes)
    except ZeroDivisionError:
        trailer_rating = 0

    return trailer_rating

if __name__ == '__main__':
	app.run()
