import guid
import json
import boto3
import tweepy
from config import TABLE_NAME, S3_BUCKET_NAME
from filter_helper import bounding_boxes
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError


class StreamListener(tweepy.StreamListener):
    def __init__(self, db, logger, is_geo_specific, storage_backend):
        super(StreamListener, self).__init__()
        self.db = db
        self.logger = logger
        self.is_geo_specific = is_geo_specific
        self.storage_backend = storage_backend

        # Conditionally connect to S3 and create JSON helper function:
        if self.storage_backend == 's3':
            s3 = boto3.resource("s3").Bucket(S3_BUCKET_NAME)
            json.dump_s3 = lambda obj, f: s3.Object(key=f).put(Body=json.dumps(obj))

    def on_status(self, tweet):
        self.logger.info(f"Processing tweet id {tweet.id}")

        # Check for presence of geo-data first:
        coordinates = tweet.coordinates
        geo = tweet.geo

        # Conditionally ignore tweets w/o geo-data:
        if self.is_geo_specific:
            if coordinates is None:
                return
            if geo is not None:
                geo = json.dumps(geo)

            # Stringify coordinates, but save the point:
            point = coordinates["coordinates"]
            coordinates = json.dumps(coordinates)

            # Filter tweets by specified geo-region(s):
            if not in_desired_geo_region(point, bounding_boxes):
                return

        # Perform basic sentiment analysis on Tweet text:
        text = remove_non_ascii(tweet.text)
        blob = TextBlob(text)
        sentiment = blob.sentiment

        # Build dictionary for row data from Tweet:
        row = dict(
            user_description=remove_non_ascii(tweet.user.description),
            user_location=tweet.user.location,
            coordinates=coordinates,
            text=text,
            geo=geo,
            user_name=remove_non_ascii(tweet.user.screen_name),
            user_created=tweet.user.created_at,
            user_followers=tweet.user.followers_count,
            id_str=tweet.id_str,
            created=tweet.created_at,
            retweet_count=tweet.retweet_count,
            user_bg_color=tweet.user.profile_background_color,
            polarity=sentiment.polarity,  # p in [-1.0, 1.0], where -1.0 = negative and 1.0 = positive
            subjectivity=sentiment.subjectivity,  # s in [0.0, 1.0], where 0.0 = objective and 1.0 = subjective
        )

        # Add row to storage backend:
        if self.storage_backend == 'sqlite':
            # Update SQLite DB:
            try:
                table = self.db[TABLE_NAME]
                table.insert(row)
                self.logger.info(f"Successfully added tweet id {tweet.id} to SQLite DB")
            except ProgrammingError as err:
                print(err)
        elif self.storage_backend == 's3':
            # Upload JSONified row to S3:
            try:
                key = guid(row)
                json.dump_s3(row, key)
            except Exception as err:
                print(err)

    def on_error(self, status_code):
        if status_code == 420:  # Close the connection if API rate limit is met
            return False


# Returns a string, sanitized of non-ascii chars
def remove_non_ascii(string):
    if string:
        return string.encode("ascii", errors="ignore").decode()
    return string


# Determine if a GeoJSON point, p is within a bounding box, bb,
# where p is of the form (x, y) and bb is of the form (ix, ax, iy, ay):
def in_bbox(p, bb):
    return bb[0] <= p[0] <= bb[2] and bb[1] <= p[1] <= bb[3]


# Given a point and a list of bounding boxes, determine if the
# point falls within at least one of the bounding boxes:
def in_desired_geo_region(p, bbs):
    # One-liner:
    # return any(list(map(lambda bb: in_bbox(p, bb), bounding_boxes)))

    # More efficient:
    for bb in bbs:
        if in_bbox(p, bb):
            return True
    return False
