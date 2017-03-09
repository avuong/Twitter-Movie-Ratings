# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import json

def get_tweets(file):
	data = []
	f = open(file)
	for line in f:
		tweet = json.loads(line)
		tweet = tweet['text']
		tweet = re.sub('^(RT @.+?: )+', '', tweet)
		tweet = re.sub('#\w+', '', tweet)
		tweet = re.sub('[^\w ]', '', tweet)
		data.append(tweet)

	return data

if __name__ == '__main__':
	tweets = get_tweets('moana.txt')
	analyzer = SentimentIntensityAnalyzer()
	for tweet in tweets:
		vs = analyzer.polarity_scores(tweet)
		print("{:-<100} {}".format(tweet, str(vs)))
