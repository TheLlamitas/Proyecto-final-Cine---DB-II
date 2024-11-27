from services import register_user, buy_tickets
from models import Movie

if __name__ == "__main__":
    print(register_user("Juan Perez", "juan@mail.com", ["Accion", "Comedia"]))

    Movie.add_movie("Avengers", "Accion", 120, ["15:00", "18:00"], 100)

    print(buy_tickets("juan@mail.com", "Avengers", 2))