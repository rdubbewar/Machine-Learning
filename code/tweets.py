import re
import tweepy
import csv
from textblob import TextBlob

#Twitter API credentials
consumer_key = "qcSo7xJjPbIuOeoz6FpHgKY09"
consumer_secret = "OX9fpsHoY7pbDKAwQqA6USpARq1YI9CimQD6lWgm48knTBk59S"
access_key = "904614061861691392-tPyHAxyCQUsuR3EEzJ8LivAOyCzN1xz"
access_secret = "9hqb5Aei1g3W8Hx05Dp6lGZUUBuU2UagNx8pLjF2TGI2O"

def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
       return 1
    elif analysis.sentiment.polarity == 0:
       return 0
    else:
       return -1

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []  
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))
    outtweets = [[tweet.id_str, get_tweet_sentiment(tweet.text), tweet.text.encode("utf-8")] for tweet in alltweets]

    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(outtweets)
    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("Cubs")