from .database import db
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

    def add_movie(name, genre, duration, schedules, total_seats):
        movie_data = {
            "name": name,
            "genre": genre,
            "duration": duration,
            "schedules": schedules,  
            "total_seats": total_seats
        }
        Movie.collection.insert_one(movie_data)

    def get_movies():
        return list(Movie.collection.find())

    def update_movie(movie_id, update_operation, array_filters=None):
        update_query = {"_id": movie_id}

        if array_filters:
            result = Movie.collection.update_one(update_query, update_operation, array_filters=array_filters)
        else:
            result = Movie.collection.update_one(update_query, update_operation)
    
        return result
    
    def delete_movie(movie_id):
        return Movie.collection.delete_one({"_id": movie_id})

class Transaction:
    collection = db["transacciones"]

    def create_transaction(user_email, movie_name, schedule, seats):
        new_transaction = {
            "user_email": user_email,
            "movie_name": movie_name,
            "schedule": schedule,  # Agregar el horario
            "seats": seats,
            "timestamp": datetime.now()
        }
        result = Transaction.collection.insert_one(new_transaction)
        
        transaction_id = result.inserted_id
        transaction_summary = {
            "_id": transaction_id,  
            "user_email": user_email,
            "movie_name": movie_name,
            "schedule": schedule,  
            "seats": seats,
            "timestamp": datetime.now()
        }
        
        User.collection.update_one(
            {"email": user_email},
            {"$push": {"purchase_history": transaction_summary}}
        )
        
        return transaction_summary  

    def get_transaction():
        return list(Transaction.collection.find())

