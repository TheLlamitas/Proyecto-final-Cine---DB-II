from .models import User, Movie, Transaction

def register_user(name, email, preferences):
    if User.get_user(email):
        return "Error: Usuario ya registrado."
    User.create_user(name, email, preferences)
    return "Usuario registrado con exito."

def buy_tickets(user_email, movie_name, schedule, seats):
    user = User.get_user(user_email)
    movie = Movie.collection.find_one({"name": movie_name})

    if not user or not movie:
        return "Error: Usuario o película no encontrada"
    
    movie_schedule = None
    for schedule_item in movie['schedules']:
        if schedule_item['time'] == schedule:
            movie_schedule = schedule_item
            break

    if not movie_schedule:
        return "Error: Horario no disponible para la película."

    if movie_schedule['available_seats'] < seats:
        return f"Error: Solo hay {movie_schedule['available_seats']} asientos disponibles."

    new_available_seats = movie_schedule['available_seats'] - seats
    Movie.update_movie(
        movie["_id"],
        {"$set": {"schedules.$[elem].available_seats": new_available_seats}},
        array_filters=[{"elem.time": schedule}]
    )


    transaction_details = Transaction.create_transaction(user_email, movie_name, schedule, seats)

    return "Compra realizada con éxito.", transaction_details


def create_movie(name, genre, duration, schedules, total_seats):
    existing_movie = Movie.collection.find_one({"name": name})
    if existing_movie:
        return "Error: La película ya existe."

    # Crea la nueva película en la base de datos
    Movie.add_movie(name, genre, duration, schedules, total_seats)
    return "Película creada con éxito."