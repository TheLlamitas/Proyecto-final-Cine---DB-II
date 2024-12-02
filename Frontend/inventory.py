import tkinter as tk
from tkinter import messagebox, ttk
import json

# Lista para almacenar las funciones
funciones = []

# Archivo JSON para guardar los datos
archivo_datos = "funciones.json"

# Cargar funciones desde el archivo JSON
def cargar_datos():
    global funciones
    try:
        with open(archivo_datos, "r", encoding="utf-8") as archivo:
            funciones = json.load(archivo)
    except FileNotFoundError:
        funciones = []

# Guardar funciones en el archivo JSON
def guardar_datos():
    with open(archivo_datos, "w", encoding="utf-8") as archivo:
        json.dump(funciones, archivo, ensure_ascii=False, indent=4)

# Función para añadir una nueva función
def agregar_funcion():
    nombre = entrada_nombre.get()
    genero = entrada_genero.get()
    duracion = entrada_duracion.get()
    horario = entrada_horario.get()
    disponibilidad = entrada_disponibilidad.get()
    
    # Validaciones
    if not (nombre and genero and duracion and horario and disponibilidad):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    
    if not disponibilidad.isdigit() or int(disponibilidad) < 0:
        messagebox.showerror("Error", "La disponibilidad debe ser un número positivo.")
        return

    # Crear el diccionario de la función
    nueva_funcion = {
        "nombre": nombre,
        "genero": genero,
        "duracion": duracion,
        "horario": horario,
        "disponibilidad": int(disponibilidad)
    }
    funciones.append(nueva_funcion)
    guardar_datos()
    actualizar_tabla()
    limpiar_campos()
    messagebox.showinfo("Éxito", f"Función '{nombre}' añadida correctamente.")

# Función para limpiar los campos del formulario
def limpiar_campos():
    entrada_nombre.delete(0, tk.END)
    entrada_genero.delete(0, tk.END)
    entrada_duracion.delete(0, tk.END)
    entrada_horario.delete(0, tk.END)
    entrada_disponibilidad.delete(0, tk.END)

# Actualizar la tabla con los datos de las funciones
def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    for funcion in funciones:
        tabla.insert("", tk.END, values=(funcion["nombre"], funcion["genero"], funcion["duracion"], 
                                         funcion["horario"], funcion["disponibilidad"]))

# Función para eliminar una función seleccionada
def eliminar_funcion():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una función para eliminar.")
        return
    indice = tabla.index(seleccion[0])
    funciones.pop(indice)
    guardar_datos()
    actualizar_tabla()
    messagebox.showinfo("Éxito", "Función eliminada correctamente.")

# Cargar datos al iniciar
cargar_datos()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Inventarios - Funciones de Cine")
ventana.geometry("800x500")

# Títulos
tk.Label(ventana, text="Gestor de Funciones de Cine", font=("Arial", 16)).pack(pady=10)

# Frame para el formulario
frame_formulario = tk.Frame(ventana)
frame_formulario.pack(pady=10)

# Campos del formulario
tk.Label(frame_formulario, text="Nombre:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entrada_nombre = tk.Entry(frame_formulario, font=("Arial", 12))
entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_formulario, text="Género:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entrada_genero = tk.Entry(frame_formulario, font=("Arial", 12))
entrada_genero.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_formulario, text="Duración:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
entrada_duracion = tk.Entry(frame_formulario, font=("Arial", 12))
entrada_duracion.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_formulario, text="Horario de Función:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
entrada_horario = tk.Entry(frame_formulario, font=("Arial", 12))
entrada_horario.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_formulario, text="Disponibilidad de Entradas:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5)
entrada_disponibilidad = tk.Entry(frame_formulario, font=("Arial", 12))
entrada_disponibilidad.grid(row=4, column=1, padx=5, pady=5)

# Botones
tk.Button(frame_formulario, text="Agregar Función", font=("Arial", 12), command=agregar_funcion).grid(row=5, column=0, padx=10, pady=10, columnspan=2)
tk.Button(frame_formulario, text="Eliminar Función", font=("Arial", 12), command=eliminar_funcion).grid(row=6, column=0, padx=10, pady=10, columnspan=2)

# Tabla para mostrar las funciones
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10)

columnas = ("Nombre", "Género", "Duración", "Horario", "Disponibilidad")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
tabla.pack()

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, anchor=tk.CENTER, width=150)

# Llenar la tabla al inicio
actualizar_tabla()

# Ejecutar la aplicación
ventana.mainloop()