import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.services import buy_tickets
from Backend.models import User, Movie, Transaction

def buy_tickets_gui():
    def on_buy():
        user_email = selected_user.get()
        movie_name = selected_movie.get()
        schedule = selected_schedule.get()  
        seats = int(entry_seats.get())

        if seats <= 0:
            messagebox.showerror("Error", "El número de asientos debe ser mayor a 0.")
            return

        # Llamada al servicio para comprar boletos
        result, transaction_details = buy_tickets(user_email, movie_name, schedule, seats)

        # Crear una transacción y guardarla
        transaction = Transaction(user_email=user_email, movie_name=movie_name, schedule=schedule, seats=seats)
        transaction.save()

        # Mostrar la transacción
        message = f"{result}\n\nDetalles de la transacción:\n"
        message += f"Usuario: {user_email}\nPelícula: {movie_name}\nHorario: {schedule}\nAsientos: {seats}"

        response = messagebox.showinfo("Transacción Exitosa", message)
        
        # Cerrar la ventana después de aceptar
        buy_window.destroy()

    buy_window = tk.Tk()
    buy_window.title("Compra de Boletos")

    tk.Label(buy_window, text="Selecciona un Usuario:").pack(pady=5)
    
    users = User.collection.find()
    user_list = [user['email'] for user in users]

    if not user_list:
        messagebox.showerror("Error", "No hay usuarios en la base de datos.")
        buy_window.destroy()  
        return

    selected_user = tk.StringVar(buy_window)
    selected_user.set(user_list[0])  

    user_menu = tk.OptionMenu(buy_window, selected_user, *user_list)
    user_menu.pack(pady=5)

    tk.Label(buy_window, text="Selecciona una Película:").pack(pady=5)

    movies = Movie.collection.find()
    movie_list = [movie['name'] for movie in movies]

    selected_movie = tk.StringVar(buy_window)
    selected_movie.set(movie_list[0])  

    movie_menu = tk.OptionMenu(buy_window, selected_movie, *movie_list)
    movie_menu.pack(pady=5)

    def update_schedule_options(*args):
        selected_movie_name = selected_movie.get()
        movie = Movie.collection.find_one({"name": selected_movie_name})
        if movie:
            schedule_list = [schedule['time'] for schedule in movie['schedules']]
            selected_schedule.set(schedule_list[0] if schedule_list else "")  # Predeterminar al primer horario disponible
            schedule_menu['menu'].delete(0, 'end')  # Limpiar los horarios existentes
            for time in schedule_list:
                schedule_menu['menu'].add_command(label=time, command=tk._setit(selected_schedule, time))

    selected_movie.trace("w", update_schedule_options) 
    tk.Label(buy_window, text="Selecciona un Horario:").pack(pady=5)

    selected_schedule = tk.StringVar(buy_window)
    schedule_menu = tk.OptionMenu(buy_window, selected_schedule, "")
    schedule_menu.pack(pady=5)

    tk.Label(buy_window, text="Número de Asientos:").pack(pady=5)
    entry_seats = tk.Entry(buy_window)
    entry_seats.pack(pady=5)

    tk.Button(buy_window, text="Comprar Boletos", command=on_buy).pack(pady=10)

    buy_window.mainloop()


if __name__ == "__main__":
    buy_tickets_gui()
