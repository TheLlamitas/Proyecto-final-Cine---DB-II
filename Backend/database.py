from pymongo import MongoClient

def get_database():
    client = MongoClient("Su base de datos MongoDB")
    return client["cine"]

db = get_database()
