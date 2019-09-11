"""
Filter a real-time stream of Tweets based on traffic keywords & geo-location.
Adapted from: https://www.dataquest.io/blog/streaming-data-python/
"""

import tweepy
import dataset
from config import TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_KEY, TWITTER_SECRET, CONNECTION_STRING
from stream_listener import StreamListener
from filter_helper import traffic_keywords

# Initialize Twitter authentication objects:
auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

# Get an api object:
api = tweepy.API(auth)

# Initialize a SQLite DB:
db = dataset.connect(CONNECTION_STRING)

# Start a Tweet listener:
stream_listener = StreamListener(db)
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=traffic_keywords)
