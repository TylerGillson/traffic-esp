import dataset
import datafreeze
from esp import config

# Export the contents of a SQLite table to CSV:
db = dataset.connect(config.CONNECTION_STRING)
result = db[config.TABLE_NAME].all()
datafreeze.freeze(result, format='csv', filename=config.CSV_NAME)
