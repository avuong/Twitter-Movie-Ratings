import requests
import re

if __name__ == '__main__':

    api_key = "" #Youtube API Key (get through google console)
    video_id = "LKFuXETZUsI" #video ID of movie Ex.)"LKFuXETZUsI" for Moana

    response = requests.get("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=" + video_id
                    + "&maxResults=50&key=" + api_key)
    data = response.json()

    dislike_count = data['items'][0]['statistics']['dislikeCount']
    like_count = data['items'][0]['statistics']['likeCount']
    print "Dislike count is " + str(dislike_count)
    print "Like count is " + str(like_count)
    #uncomment for more JSON data below
    #print data
