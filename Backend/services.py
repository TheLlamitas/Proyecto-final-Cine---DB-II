from models import User, Movie, Transaction

def register_user(name, email, preferences):
    if User.get_user(email):
        return "Error: Usuario ya registrado."
    User.create_user(name, email, preferences)
    return "Usuario registrado con exito."

def buy_tickets(user_email, movie_name, seats):
    user = User.get_user(user_email)
    movie = Movie.collection.find_one({"name": movie_name})

    if not user or not movie:
        return " Error: Usuario o pelicula no encontrada"
    
    if movie['available_seats'] < seats:
        return f"Error: Solo hay {movie['available_seats']} asientos disponibles."
    
    Transaction.create_transaction(user_email, movie_name, seats)
    Movie.update_movie(movie["_id"], {"available_seats": movie["available_seats"] - seats})
    return "Compra realizada con exito."