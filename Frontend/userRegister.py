import tkinter as tk
from tkinter import messagebox, ttk
import json

# Archivo JSON donde se almacenan los usuarios
archivo_json = "usuarios.json"

# Lista para almacenar usuarios registrados
usuarios = []

# Cargar datos desde el archivo JSON al inicio
def cargar_datos():
    global usuarios
    try:
        with open(archivo_json, "r", encoding="utf-8") as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        usuarios = []

# Guardar datos en el archivo JSON
def guardar_en_json():
    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, ensure_ascii=False, indent=4)

# Función para registrar o actualizar un usuario
def registrar_usuario():
    nombre = entrada_nombre.get()
    correo = entrada_correo.get()
    preferencias = entrada_preferencias.get("1.0", tk.END).strip()
    
    if not nombre or not correo:
        messagebox.showerror("Error", "Nombre y correo son obligatorios.")
        return

    # Verificar si el usuario ya existe (por correo)
    usuario_existente = next((u for u in usuarios if u["correo"] == correo), None)
    
    if usuario_existente:
        usuario_existente["nombre"] = nombre
        usuario_existente["preferencias_peliculas"] = preferencias.split("\n")
        messagebox.showinfo("Éxito", f"Datos del usuario {nombre} actualizados correctamente.")
    else:
        usuario = {
            "nombre": nombre,
            "correo": correo,
            "historial_compras": [],  # El historial se inicializa vacío para nuevos usuarios
            "preferencias_peliculas": preferencias.split("\n")
        }
        usuarios.append(usuario)
        messagebox.showinfo("Éxito", f"Usuario {nombre} registrado correctamente.")

    guardar_en_json()
    actualizar_tabla()
    limpiar_campos()

# Limpiar los campos del formulario
def limpiar_campos():
    entrada_nombre.delete(0, tk.END)
    entrada_correo.delete(0, tk.END)
    entrada_preferencias.delete("1.0", tk.END)
    entrada_historial.delete("1.0", tk.END)

# Actualizar la tabla con los datos de los usuarios
def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    for usuario in usuarios:
        historial = ", ".join(usuario["historial_compras"])
        preferencias = ", ".join(usuario["preferencias_peliculas"])
        tabla.insert("", tk.END, values=(usuario["nombre"], usuario["correo"], historial, preferencias))

# Cargar datos de un usuario seleccionado en el formulario
def cargar_usuario():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione un usuario de la tabla.")
        return
    
    indice = tabla.index(seleccion[0])
    usuario = usuarios[indice]

    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(0, usuario["nombre"])
    entrada_correo.delete(0, tk.END)
    entrada_correo.insert(0, usuario["correo"])
    entrada_historial.config(state="normal")
    entrada_historial.delete("1.0", tk.END)
    entrada_historial.insert("1.0", "\n".join(usuario["historial_compras"]))
    entrada_historial.config(state="disabled")
    entrada_preferencias.delete("1.0", tk.END)
    entrada_preferencias.insert("1.0", "\n".join(usuario["preferencias_peliculas"]))

# Eliminar un usuario seleccionado
def eliminar_usuario():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione un usuario de la tabla.")
        return

    indice = tabla.index(seleccion[0])
    usuario = usuarios.pop(indice)
    guardar_en_json()
    actualizar_tabla()
    messagebox.showinfo("Éxito", f"Usuario {usuario['nombre']} eliminado correctamente.")

# Cargar datos al iniciar
cargar_datos()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Usuarios")
ventana.geometry("800x600")

# Widgets del formulario
tk.Label(ventana, text="Nombre:", font=("Arial", 12)).pack(pady=5)
entrada_nombre = tk.Entry(ventana, font=("Arial", 12))
entrada_nombre.pack(pady=5)

tk.Label(ventana, text="Correo Electrónico:", font=("Arial", 12)).pack(pady=5)
entrada_correo = tk.Entry(ventana, font=("Arial", 12))
entrada_correo.pack(pady=5)

tk.Label(ventana, text="Historial de Compras (no editable):", font=("Arial", 12)).pack(pady=5)
entrada_historial = tk.Text(ventana, font=("Arial", 12), height=5, width=60, state="disabled")
entrada_historial.pack(pady=5)

tk.Label(ventana, text="Preferencias de Películas (una por línea):", font=("Arial", 12)).pack(pady=5)
entrada_preferencias = tk.Text(ventana, font=("Arial", 12), height=5, width=60)
entrada_preferencias.pack(pady=5)

# Botones
tk.Button(ventana, text="Registrar/Actualizar Usuario", font=("Arial", 12), command=registrar_usuario).pack(pady=10)
tk.Button(ventana, text="Cargar Usuario Seleccionado", font=("Arial", 12), command=cargar_usuario).pack(pady=5)
tk.Button(ventana, text="Eliminar Usuario", font=("Arial", 12), command=eliminar_usuario).pack(pady=5)

# Tabla de usuarios
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10)

columnas = ("Nombre", "Correo", "Historial de Compras", "Preferencias de Películas")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
tabla.pack()

# Configuración de las columnas
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, anchor=tk.W, width=150)

# Llenar la tabla al inicio
actualizar_tabla()

# Ejecutar la aplicación
ventana.mainloop()