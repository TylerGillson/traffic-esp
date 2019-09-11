import dataset
import datafreeze
from config import CONNECTION_STRING, TABLE_NAME, CSV_NAME

# Export the contents of a SQLite table to CSV:
db = dataset.connect(CONNECTION_STRING)
result = db[TABLE_NAME].all()
datafreeze.freeze(result, format='csv', filename=CSV_NAME)
