"""
Filter a real-time stream of Tweets based on traffic keywords & geo-location.
Adapted from: https://www.dataquest.io/blog/streaming-data-python/
"""

import tweepy
import logging
import dataset
from config import TWITTER_APP_KEY, TWITTER_APP_SECRET, TWITTER_KEY, TWITTER_SECRET, CONNECTION_STRING
from stream_listener import StreamListener
from filter_helper import all_traffic_keywords

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize Twitter authentication objects:
auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

# Get an api object:
api = tweepy.API(auth)

# Verify successful API authentication:
try:
    api.verify_credentials()
except Exception as err:
    logger.error("Error creating API", exc_info=True)
    raise err
logger.info("API created")

# Initialize a SQLite DB:
db = dataset.connect(CONNECTION_STRING)

# Initiate Tweet listeners:
stream_listener = StreamListener(db, logger, True)

# Initiate streams:
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Begin filtering Tweets:
try:
    stream.filter(track=all_traffic_keywords)
except Exception as err:
    logger.error(err)
    raise err
