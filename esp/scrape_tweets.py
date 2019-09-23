"""
Filter a real-time stream of Tweets based on traffic keywords & geo-location.
Adapted from: https://www.dataquest.io/blog/streaming-data-python/
"""

import sys
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

# Initialize storage backend:
storage_backend = sys.argv[1]
if storage_backend == 'sqlite':
    # Initialize a SQLite DB:
    db = dataset.connect(CONNECTION_STRING)
elif storage_backend == 's3':
    pass  # Use an Amazon S3 bucket
else:
    logger.error("Invalid storage backend", exc_info=True)
    raise ValueError("Invalid storage backend")
logger.info("Storage backend initialized")

# Initiate Tweet listeners:
stream_listener = StreamListener(db, logger, True, storage_backend)

# Initiate streams:
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Begin filtering Tweets:
try:
    stream.filter(track=all_traffic_keywords)
except Exception as err:
    logger.error(err)
    raise err
