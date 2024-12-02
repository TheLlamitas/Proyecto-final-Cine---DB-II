from pymongo import MongoClient

def get_database():
    client = MongoClient("mongodb+srv://Nicolas:12345@practica1.cdhav.mongodb.net/")
    return client["cine"]

db = get_database()
