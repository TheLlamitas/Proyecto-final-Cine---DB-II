import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.services import create_movie  
from Backend.models import Movie

def create_movie_gui():
    def on_create_movie():
        name = entry_name.get()
        genre = entry_genre.get()
        duration = entry_duration.get()
        schedule_input = entry_schedule.get()  
        total_seats = entry_total_seats.get()

        if not name or not genre or not duration or not schedule_input or not total_seats:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            total_seats = int(total_seats)
        except ValueError:
            messagebox.showerror("Error", "El número de asientos debe ser un número entero.")
            return

        schedules = []
        for schedule in schedule_input.split(','):
            time = schedule.strip()
            schedules.append({'time': time, 'available_seats': total_seats}) 
        
        result = create_movie(name, genre, duration, schedules, total_seats)
        messagebox.showinfo("Resultado", result)
        
        entry_name.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        entry_duration.delete(0, tk.END)
        entry_schedule.delete(0, tk.END)
        entry_total_seats.delete(0, tk.END)
    
    def update_movie_list():
        listbox_movies.delete(0, tk.END)
        
        movies = Movie.get_movies()  
        
        for movie in movies:
            for schedule in movie['schedules']:
                schedule_str = f"{schedule['time']} - Asientos disponibles: {schedule['available_seats']}"
                listbox_movies.insert(tk.END, f"{movie['name']} | {movie['genre']} | {movie['duration']} | {schedule_str}")

    create_movie_window = tk.Tk()
    create_movie_window.title("Crear Película")

    tk.Label(create_movie_window, text="Nombre:").pack(pady=5)
    entry_name = tk.Entry(create_movie_window)
    entry_name.pack(pady=5)

    tk.Label(create_movie_window, text="Género:").pack(pady=5)
    entry_genre = tk.Entry(create_movie_window)
    entry_genre.pack(pady=5)

    tk.Label(create_movie_window, text="Duración (en minutos):").pack(pady=5)
    entry_duration = tk.Entry(create_movie_window)
    entry_duration.pack(pady=5)

    tk.Label(create_movie_window, text="Horarios (separados por coma):").pack(pady=5)
    entry_schedule = tk.Entry(create_movie_window)
    entry_schedule.pack(pady=5)

    tk.Label(create_movie_window, text="Asientos Totales por horario:").pack(pady=5)
    entry_total_seats = tk.Entry(create_movie_window)
    entry_total_seats.pack(pady=5)

    tk.Button(create_movie_window, text="Crear Película", command=on_create_movie).pack(pady=10)

    tk.Label(create_movie_window, text="Películas Registradas:").pack(pady=5)
    listbox_movies = tk.Listbox(create_movie_window, width=80, height=10)
    listbox_movies.pack(pady=5)

    update_movie_list() 

    create_movie_window.mainloop()

if __name__ == "__main__":
    create_movie_gui()
