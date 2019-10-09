import os

# Load Twitter API Credentials from environment:
TWITTER_APP_KEY = os.getenv("TWITTER_APP_KEY")
TWITTER_APP_SECRET = os.getenv("TWITTER_APP_SECRET")
TWITTER_KEY = os.getenv("TWITTER_KEY")
TWITTER_SECRET = os.getenv("TWITTER_SECRET")

# DB Constants:
CONNECTION_STRING = "sqlite:///tweets.db"
CSV_NAME = "geo-tweets.csv"
TABLE_NAME = "traffic_tweets"

# SMTP Constants:
NOTIFICATION_TWITTER_ACCOUNT_ID = "1181772721455353857"
VOLPE_GMAIL_PASSWORD = os.getenv("VOLPE_GMAIL_PASSWORD")
