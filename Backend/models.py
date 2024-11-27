from database import db
from datetime import datetime
from bson import ObjectId

class User:
    collection = db["usuarios"]

    def create_user(name, email, preferences):
        new_user = {
            "name": name,
            "email": email,
            "preferences": preferences,
            "purchase_history": []
        }
        return User.collection.insert_one(new_user)
    
    def get_user(email):
        return User.collection.find_one({"email": email})
    
    def update_user(email, data):
        return User.collection.update_one({"email": email}, {"$set": data})
    
    def delete_user(email):
        return User.collection.delete_one({"email": email})
    
class Movie:
    collection = db["peliculas"]

    def add_movie(name, genre, duration, schedule, total_seats):
        new_movie = {
            "name": name,
            "genre": genre,
            "duration": duration,
            "schedule": schedule,
            "available_seats": total_seats
        }
        return Movie.collection.insert_one(new_movie)
    
    def get_movies():
        return list(Movie.collection.find())
    
    def update_movie(movie_id, data):
        return Movie.collection.update_one({"_id": movie_id}, {"$set": data})
    
    def delete_movie(movie_id):
        return Movie.collection.delete_one({"_id": movie_id})

class Transaction:
    collection = db["transacciones"]

    def create_transaction(user_email, movie_name, seats):
        new_transaction = {
            "user_email": user_email,
            "movie_name": movie_name,
            "seats": seats,
            "timestamp": datetime.now()
        }
        result = Transaction.collection.insert_one(new_transaction)
        
        transaction_id = result.inserted_id
        transaction_summary = {
            "_id": transaction_id,  
            "movie_name": movie_name,
            "seats": seats,
            "timestamp": datetime.now()
        }
        
        User.collection.update_one(
            {"email": user_email},
            {"$push": {"purchase_history": transaction_summary}}
        )
        
        return result
