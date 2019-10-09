# Custom list of traffic keywords:
custom_traffic_keywords = [
    'accident',
    'construction',
    'crash',
    'pothole',
    'fatality',
    'traffic jam',
    'halted',
    'backed up',
    'delay',
    'stoppage',
    'gridlock',
    'transport',
    'rush hour',
    'congestion',
    'road rage',
    'road closed',
    'bottleneck',
    'heavy traffic',
    'hazard',
    'pileup',
    'collision',
    'fender-bender',
    'totalled',
    'crack-up',
    'disaster',
    'calamity',
    'casualty'
    # 'avenue',
    # 'street',
]

# UK traffic movements and traffic jams keywords taken from:
# https://www.macmillandictionary.com/us/thesaurus-category/american/traffic-movements-and-traffic-jams
traffic_keywords_uk = [
    'back up',
    'bottleneck',
    'bumper-to-bumper',
    'busy',
    'congestion',
    'congestion charge',
    'filter',
    'gridlock',
    'hold-up',
    'jam',
    'nose to tail',
    'the rush',
    'snarl',
    'snarl-up',
    'speed limit',
    'ticket',
    'tied up',
    'traffic',
    'traffic calming',
    'traffic jam'
]

# Accidents, Road Closure, Hazards & Weather, and Obstacle Vehicles keywords taken from:
# http://www.dot7.state.pa.us/BPR_PDF_FILES/Documents/Research/Complete%20Projects/Operations/Real_time_Incident_Detection_Using_Social_Media_Data.pdf
accidents = [
    'Crash',
    'Accident',
    'Collision',
    'Fatal',
    'Tow',
    'Break',
    'Damage',
    'Repair'
]

road_closure = [
    'Road work',
    'Closure',
    'Zone',
    'Maintenance',
    'Schedule',
    'Seal'
]

hazards_and_weather = [
    'Rain',
    'Snow',
    'Slip',
    'Wind',
    'Flood',
    'Rainy',
    'Snowy',
    'Hazard',
    'Tree',
    'Block',
    'Wiper',
    'Inches',
    'Wet',
    'Cold',
    'Freeze',
    'Hot',
    'Visibility',
    'Fire',
    'Weather',
    'Animal',
    'Deer',
    'Dead',
    'Hail',
    'Melt',
    'Ice',
    'Slope',
    'Chilly',
    'Slick',
    'Tire',
    'Cover',
    'Friction',
    'Frozen',
    'Grip',
    'Cloudy',
    'Freeze',
    'Ponding'
]

obstacle_vehicles = [
    'Debris',
    'Obstacle',
    'Disabled',
    'Overweight',
    'Tall',
    'Height',
    'Heavy',
    'Stuck'
]

all_traffic_keywords = list(set(custom_traffic_keywords)
                            .union(set(traffic_keywords_uk))
                            .union(set(accidents))
                            .union(set(road_closure))
                            .union(set(hazards_and_weather))
                            .union(set(obstacle_vehicles))
                            )

# Geo-region(s) to filter Tweets by, encoded using the GeoJSON format:
bounding_boxes = [
    (-11.69, 49.87, 1.85, 61.26),  # United Kingdom
]

# Top 15 largest cities in the USA by population, 2019.
# Cities are ordered from largest to smallest, descending.
# bboxes generated via: https://boundingbox.klokantech.com/
"""
(-74, 40, -73, 41),                # New York City, NY
(-118.67, 33.70, -118.16, 34.34),  # Los Angeles, CA
(-87.94, 41.64, -87.52, 42.02),    # Chicago, IL
(-95.91, 29.54, -95.01, 30.11),    # Houston, TX
(-112.67, 33.13, -111.37, 33.89),  # Phoenix, AZ
(-75.28, 39.87, -74.96, 40.14),    # Philadelphia, PA
(-98.81, 29.19, -98.22, 29.73),    # San Antonio, TX
(-117.31, 32.53, -116.91, 33.11),  # San Diego, CA
(-97, 32.61, -96.46, 33.02),       # Dallas, TX
(-122.09, 37.20, -121.73, 37.46),  # San Jose, CA
(-97.94, 30.10, -97.56, 30.52),    # Austin, TX
(-82.05, 30.10, -81.32, 30.59),    # Jacksonville, FL
(-97.59, 32.55, -97.03, 33.05),    # Fort Worth, TX
(-122.75, 36.8, -121.75, 37.8),    # San Francisco, CA
(-83.21, 39.81, -82.77, 40.12)     # Columbus, OH
"""

# Keywords for email notifications:
email_keywords = {
    # Accidents:
    'accident',
    'crash',
    'pileup',
    'collision',
    'fender-bender',
    # Delays:
    'construction',
    'congestion',
    'traffic jam',
    'road closed',
    'bottleneck',
    'heavy traffic',
    # Natural Disasters:
    'flood',
    'tsunami',
    'earthquake',
    'tornado'
}
