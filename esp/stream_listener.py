import json
import tweepy
from esp import config
from esp.filter_helper import bounding_boxes
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError


class StreamListener(tweepy.StreamListener):
    def __init__(self, db):
        super(StreamListener, self).__init__()
        self.db = db

    def on_status(self, status):
        # Check for presence of geo-data first:
        coordinates = status.coordinates
        geo = status.geo
        if coordinates is None:  # Ignore tweets w/o geo-data
            return
        if geo is not None:
            geo = json.dumps(geo)

        # Stringify coordinates, but save the point:
        point = coordinates["coordinates"]
        coordinates = json.dumps(coordinates)

        # Filter by top 15 largest cities in the USA by population:
        if not in_top_15_city(point, bounding_boxes):
            return

        # Perform basic sentiment analysis on Tweet text:
        text = remove_non_ascii(status.text)
        blob = TextBlob(text)
        sentiment = blob.sentiment

        # Update SQLite DB:
        table = self.db[config.TABLE_NAME]
        try:
            table.insert(dict(
                user_description=remove_non_ascii(status.user.description),
                user_location=status.user.location,
                coordinates=coordinates,
                text=text,
                geo=geo,
                user_name=remove_non_ascii(status.user.screen_name),
                user_created=status.user.created_at,
                user_followers=status.user.followers_count,
                id_str=status.id_str,
                created=status.created_at,
                retweet_count=status.retweet_count,
                user_bg_color=status.user.profile_background_color,
                polarity=sentiment.polarity,          # p in [-1.0, 1.0], where -1.0 = negative and 1.0 = positive
                subjectivity=sentiment.subjectivity,  # s in [0.0, 1.0], where 0.0 = objective and 1.0 = subjective
            ))
        except ProgrammingError as err:
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
def in_top_15_city(p, bbs):
    # One-liner:
    # return any(list(map(lambda bb: in_bbox(p, bb), bounding_boxes)))

    # More efficient:
    for bb in bbs:
        if in_bbox(p, bb):
            return True
    return False
