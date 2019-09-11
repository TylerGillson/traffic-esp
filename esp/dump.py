import logging
import dataset
import datafreeze
from config import CONNECTION_STRING, TABLE_NAME, CSV_NAME

logger = logging.getLogger()

# Export the contents of a SQLite table to CSV:
try:
    db = dataset.connect(CONNECTION_STRING)
    result = db[TABLE_NAME].all()
    datafreeze.freeze(result, format='csv', filename=CSV_NAME)
    logger.info("All data successfully exported to CSV")
except Exception as err:
    logger.error(err)
