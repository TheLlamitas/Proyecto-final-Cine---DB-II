import tkinter as tk
from tkinter import messagebox
import sys
import os
from datetime import datetime

# Asegurarse de que los módulos del Backend estén en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.services import buy_tickets
from Backend.models import User, Movie, Transaction

def buy_tickets_gui():
    def on_buy():
        user_email = selected_user.get()
        movie_name = selected_movie.get()
        schedule = selected_schedule.get()
        seats = entry_seats.get()

        if not seats.isdigit() or int(seats) <= 0:
            messagebox.showerror("Error", "El número de asientos debe ser un número mayor a 0.")
            return

        seats = int(seats)

        try:
            result, transaction_details = buy_tickets(user_email, movie_name, schedule, seats)

            message = f"{result}\n\nDetalles de la transacción:\n"
            message += f"Usuario: {transaction_details['user_email']}\n"
            message += f"Película: {transaction_details['movie_name']}\n"
            message += f"Horario: {transaction_details['schedule']}\n"
            message += f"Asientos: {transaction_details['seats']}\n"
            message += f"Fecha y hora: {transaction_details['timestamp']}"
            
            messagebox.showinfo("Transacción Exitosa", message)
            buy_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar la compra: {str(e)}")

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
    selected_user.set(user_list[0])  # Seleccionar el primer usuario por defecto
    tk.OptionMenu(buy_window, selected_user, *user_list).pack(pady=5)

    tk.Label(buy_window, text="Selecciona una Película:").pack(pady=5)
    movies = Movie.collection.find()
    movie_list = [movie['name'] for movie in movies]

    if not movie_list:
        messagebox.showerror("Error", "No hay películas disponibles.")
        buy_window.destroy()
        return

    selected_movie = tk.StringVar(buy_window)
    selected_movie.set(movie_list[0])  # Seleccionar la primera película por defecto
    tk.OptionMenu(buy_window, selected_movie, *movie_list).pack(pady=5)

    def update_schedule_options(*args):
        selected_movie_name = selected_movie.get()
        movie = Movie.collection.find_one({"name": selected_movie_name})
        schedule_list = [schedule['time'] for schedule in movie['schedules']] if movie else []
        selected_schedule.set(schedule_list[0] if schedule_list else "")
        schedule_menu['menu'].delete(0, 'end')
        for time in schedule_list:
            schedule_menu['menu'].add_command(label=time, command=tk._setit(selected_schedule, time))

    selected_movie.trace_add("write", update_schedule_options)

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
