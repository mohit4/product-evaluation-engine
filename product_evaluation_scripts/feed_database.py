"""
feed_database.py : script that uses the generated classifier in earlier stages to classify the
    dataset and generate reports.
"""

# used to access the mongodb database
from pymongo import MongoClient

# client to access the database, defaults to localhost:27017
client = MongoClient()

# accessing the database using its name
db = client['mydb']

# accessing the collection
coll = db['mycoll']
