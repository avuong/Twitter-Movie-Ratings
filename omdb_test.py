import omdb
import tweepy

if __name__ == '__main__':
   res = omdb.request(t="hidden figures")
   data = res.json()
   # print data['Actors'].split(',')
   actors = data["Actors"].split(',')

   auth = tweepy.OAuthHandler("Bvo4QBYXneS8Z4NgXRpPltrHw", "qYU60CVlJyoaJojB9QHoVZP2I37lnvwIZWP9cYnv5KsPGFIn7z")
   auth.set_access_token("271137941-zrWtZjcVbDsuaGwvwg3rz4wRJP6er5scmqTAOxct", "vGN7VQWHc86YtYX8Q8QVRnnhD5edgUgezRDyGzNkUYrMW")

   api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

   # user = api.get_user(screen_name = actors[1])

   for i in xrange(len(actors)):
      results = api.search_users(actors[i])
      for r in results:
         if r['verified'] == True:
            print actors[i] + ": " + r['screen_name']
            # print api.get_user(r['id'])