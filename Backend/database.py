from pymongo import MongoClient

def get_database():
    client = MongoClient("Su Database MongoDB")
    return client["cine"]

db = get_database()
