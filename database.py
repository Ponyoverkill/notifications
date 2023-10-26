from pymongo import MongoClient

from config import DB_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(DB_URI)
db = getattr(client, DB_NAME)
collection = getattr(db, COLLECTION_NAME)


