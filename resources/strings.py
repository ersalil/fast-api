# from app.api.logging.logging import logger

# logger.debug('This is a debug message')

from sqlite3 import DatabaseError
from xmlrpc.client import INTERNAL_ERROR


DESCRIPTION = """Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """

DATA_NOT_FOUND = """Data not found"""
INTERNAL_ERROR = """Internal error"""
DATABASE_ERROR = """Database error"""

LIMIT_IS = """Voyages for each ship is"""
COLUMN_LOADED = """Column loaded"""
OVERVIEW = """Overview of the data"""
VOYAGE_DATA = """All Voyage data"""
AVG_VOYAGE_DATA = """Average Voyage data"""



