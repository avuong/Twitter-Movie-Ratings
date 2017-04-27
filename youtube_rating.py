import requests
import re

if __name__ == '__main__':

    api_key = "" #Youtube API Key (get through google console)
    movie = 'Moana'

    print "Finding ratings for 3 trailers for " + movie
    #Get the Video ID - automated need to parse

    #print "https://www.googleapis.com/youtube/v3/search?part=snippet&q="+ movie + "Trailer" + "&key=" + api_key
    response = requests.get("https://www.googleapis.com/youtube/v3/" \
                            "search?part=snippet&q="+ movie + "Trailer" + "&key=" + api_key)

    search_data = response.json()

    total_dislikes = 0
    total_likes = 0
    #default get 3 results back
    for i in range(0,3):
        video_id = search_data['items'][i]['id']['videoId'] #video ID of movie Ex.)"LKFuXETZUsI" for Moana
        print video_id

        response = requests.get("https://www.googleapis.com/youtube/v3/videos?part=statistics&id=" \
                                    + video_id + "&maxResults=50&key=" + api_key)

        trailer_data = response.json()

        dislike_count = trailer_data['items'][0]['statistics']['dislikeCount']
        like_count = trailer_data['items'][0]['statistics']['likeCount']
        print "Dislike count is " + str(dislike_count)
        print "Like count is " + str(like_count)

        total_dislikes += int(dislike_count)
        total_likes += int(like_count)

    print total_likes
    print total_dislikes
    trailer_rating = float(total_likes)/(total_dislikes + total_likes)
    print trailer_rating
