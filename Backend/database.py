from pymongo import MongoClient

def get_database():
    client = MongoClient("Su link de conexion a atlas")
    return client["cine"]

db = get_database()
