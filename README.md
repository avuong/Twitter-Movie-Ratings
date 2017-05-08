# Twitter-Movie-Ratings
Social Sensing Final Project

## How to Use
In order to run the program you will need omdb, NLTK, VADER Sentiment Analysis from NLTK, and tweepy. To run the web application you will also need flask and wtforms. These packages can all be installed using pip install:
  ```
  pip install omdb
  pip install nltk
  pip install tweepy
  pip install flask
  pip install wtforms
  ```
  
To install VADER Sentiment Analysis from NLTK, you can use the NLTK downloader in the terminal python interpreter:
```
python
>import nltk
>nltk.download()
>d vader_lexicon
```

Finally, we use both the Twitter and YouTube APIs. You will therefore need to obtain your own API keys and secrets for these APIs and fill in the apporpriate variables with your keys.

To run the terminal version of the program use the following command:
```
python twitter_movie_ratings.py
```
You will then be prompted to enter the title of the movie and the results will be printed to the screen.

To run the terminal version use the following commands:
```
export FLASK_APP=rate_movie.py
flask run --host=0.0.0.0
```
