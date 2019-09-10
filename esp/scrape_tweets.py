"""
Filter a real-time stream of Tweets based on traffic keywords & geo-location.
Adapted from: https://www.dataquest.io/blog/streaming-data-python/
"""

import tweepy
import dataset
from esp import config
from esp.stream_listener import StreamListener
from esp.filter_helper import traffic_keywords

# Initialize Twitter authentication objects:
auth = tweepy.OAuthHandler(config.TWITTER_APP_KEY, config.TWITTER_APP_SECRET)
auth.set_access_token(config.TWITTER_KEY, config.TWITTER_SECRET)

# Get an api object:
api = tweepy.API(auth)

# Initialize a SQLite DB:
db = dataset.connect(config.CONNECTION_STRING)

# Start a Tweet listener:
stream_listener = StreamListener(db)
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=traffic_keywords)
