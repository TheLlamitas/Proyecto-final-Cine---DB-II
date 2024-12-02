import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.services import register_user
from Backend.models import User

def register_user_gui():
    def on_register():
        name = entry_name.get()
        email = entry_email.get()
        preferences = entry_preferences.get()

        if not name or not email or not preferences:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        result = register_user(name, email, preferences)
        messagebox.showinfo("Resultado", result)
        
        update_user_list()

    def update_user_list():
        listbox_users.delete(0, tk.END)

        users = User.collection.find()
        for user in users:
            listbox_users.insert(tk.END, f"Nombre: {user['name']} | Correo: {user['email']}")

    register_window = tk.Tk()
    register_window.title("Registrar Usuario")

    tk.Label(register_window, text="Nombre:").pack(pady=5)
    entry_name = tk.Entry(register_window)
    entry_name.pack(pady=5)

    tk.Label(register_window, text="Correo:").pack(pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.pack(pady=5)

    tk.Label(register_window, text="Preferencias:").pack(pady=5)
    entry_preferences = tk.Entry(register_window)
    entry_preferences.pack(pady=5)

    tk.Button(register_window, text="Registrar", command=on_register).pack(pady=10)

    tk.Label(register_window, text="Usuarios Registrados:").pack(pady=10)
    listbox_users = tk.Listbox(register_window, width=50, height=10)
    listbox_users.pack(pady=5)

    update_user_list()

    register_window.mainloop()

if __name__ == "__main__":
    register_user_gui()
