import tkinter as tk
from tkinter import messagebox, ttk
import json

# Archivos JSON
archivo_usuarios = "usuarios.json"
archivo_funciones = "funciones.json"

# Datos en memoria
usuarios = []
funciones = []

# Cargar datos
def cargar_datos_usuarios():
    global usuarios
    try:
        with open(archivo_usuarios, "r", encoding="utf-8") as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        usuarios = []

def cargar_datos_funciones():
    global funciones
    try:
        with open(archivo_funciones, "r", encoding="utf-8") as archivo:
            funciones = json.load(archivo)
    except FileNotFoundError:
        funciones = []

# Guardar datos
def guardar_datos_usuarios():
    with open(archivo_usuarios, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, ensure_ascii=False, indent=4)

def guardar_datos_funciones():
    with open(archivo_funciones, "w", encoding="utf-8") as archivo:
        json.dump(funciones, archivo, ensure_ascii=False, indent=4)

# Actualizar tabla de funciones
def actualizar_tabla_funciones():
    for row in tabla_funciones.get_children():
        tabla_funciones.delete(row)
    for funcion in funciones:
        tabla_funciones.insert("", tk.END, values=(funcion["nombre"], funcion["genero"], funcion["duracion"], funcion["horario"], funcion["disponibilidad"]))

# Comprar entradas
def comprar_entradas():
    seleccion = tabla_funciones.selection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una función de la tabla.")
        return

    correo_usuario = combo_usuarios.get()
    if not correo_usuario:
        messagebox.showerror("Error", "Seleccione un usuario para realizar la compra.")
        return

    # Buscar usuario
    usuario = next((u for u in usuarios if u["correo"] == correo_usuario), None)
    if not usuario:
        messagebox.showerror("Error", "Usuario no encontrado.")
        return

    indice = tabla_funciones.index(seleccion[0])
    funcion = funciones[indice]
    nombre_funcion = funcion["nombre"]

    if funcion["disponibilidad"] <= 0:
        messagebox.showerror("Error", f"No hay entradas disponibles para '{nombre_funcion}'.")
        return

    # Solicitar cantidad de entradas
    try:
        cantidad = int(entrada_cantidad.get())
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingrese una cantidad válida de entradas.")
        return

    if cantidad > funcion["disponibilidad"]:
        messagebox.showerror("Error", f"Solo quedan {funcion['disponibilidad']} entradas disponibles para '{nombre_funcion}'.")
        return

    # Simulación de pago
    precio_por_entrada = 10  # Precio ficticio
    total = cantidad * precio_por_entrada
    if not messagebox.askyesno("Confirmación de Pago", f"El total es ${total}. ¿Desea continuar con el pago?"):
        return

    # Actualizar disponibilidad
    funcion["disponibilidad"] -= cantidad
    guardar_datos_funciones()
    actualizar_tabla_funciones()

    # Actualizar historial del usuario
    compra = f"{nombre_funcion} - {cantidad} entradas"
    if "historial_compras" not in usuario:
        usuario["historial_compras"] = []
    usuario["historial_compras"].append(compra)
    guardar_datos_usuarios()

    # Generar recibo
    generar_recibo(nombre_funcion, cantidad, total)

    # Limpiar cantidad de entradas
    entrada_cantidad.delete(0, tk.END)

# Generar recibo
def generar_recibo(funcion, cantidad, total):
    recibo = f"""
    --- RECIBO DE COMPRA ---
    Función: {funcion}
    Cantidad de entradas: {cantidad}
    Total pagado: ${total}
    ------------------------
    """
    messagebox.showinfo("Recibo de Compra", recibo)

# Configurar funciones iniciales (solo para primera vez)
def configurar_funciones_iniciales():
    global funciones
    funciones = [
        {"nombre": "Película 1", "genero": "Acción", "duracion": "120 min", "horario": "18:00", "disponibilidad": 50},
        {"nombre": "Película 2", "genero": "Comedia", "duracion": "90 min", "horario": "20:00", "disponibilidad": 30},
        {"nombre": "Película 3", "genero": "Drama", "duracion": "110 min", "horario": "16:00", "disponibilidad": 40},
    ]
    guardar_datos_funciones()

# Cargar datos al iniciar
cargar_datos_usuarios()
cargar_datos_funciones()
if not funciones:
    configurar_funciones_iniciales()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Compra de Entradas")
ventana.geometry("800x600")

# Selección de usuario
tk.Label(ventana, text="Seleccione un Usuario:", font=("Arial", 12)).pack(pady=5)
combo_usuarios = ttk.Combobox(ventana, font=("Arial", 12), values=[u["correo"] for u in usuarios])
combo_usuarios.pack(pady=5)

# Tabla de funciones
tk.Label(ventana, text="Funciones Disponibles:", font=("Arial", 12)).pack(pady=5)
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10)

columnas_funciones = ("Nombre", "Género", "Duración", "Horario", "Disponibilidad")
tabla_funciones = ttk.Treeview(frame_tabla, columns=columnas_funciones, show="headings", height=10)
tabla_funciones.pack()

# Configuración de columnas
for col in columnas_funciones:
    tabla_funciones.heading(col, text=col)
    tabla_funciones.column(col, anchor=tk.W, width=150)

actualizar_tabla_funciones()

# Entrada para cantidad de entradas
tk.Label(ventana, text="Cantidad de Entradas:", font=("Arial", 12)).pack(pady=5)
entrada_cantidad = tk.Entry(ventana, font=("Arial", 12))
entrada_cantidad.pack(pady=5)

# Botón para comprar
tk.Button(ventana, text="Comprar Entradas", font=("Arial", 12), command=comprar_entradas).pack(pady=20)

# Ejecutar la aplicación
ventana.mainloop()