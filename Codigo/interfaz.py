import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import logica

#Funciones

def create_circle(zone, color):

    canvas.delete("circle")

    x = logica.zone_dictionary.get(zone)[2]
    y = logica.zone_dictionary.get(zone)[3]

    radius = 13
    canvas.create_oval(x+radius, y+radius, x-radius, y-radius, fill = color, outline = color, tags = "circle")

def execute(temp, wind_v, r_hum, met_r, zone):

    result = logica.calc_athb(temp, wind_v, r_hum, met_r, zone)

    label_output.configure(text = "El indice de habitabilidad (ATHB) es: " + str(result))

    color = ""

    if result < 0.75 and result > -0.75:
        color = "#1ECE53"
        sugg_label.configure(text="Sugerencias: -0.75 a 0.75 (Verde): Se sugiere usar una ropa cómoda, con un valor de clo entre 0.5 y 1.5. Por ejemplo, una camisa de manga larga, \nun pantalón de tela y unos zapatos de cuero.")
    
    elif result < 1.5 and result > -1.5:
        color = "#F1D405" 
        if result >= 0.75:
            sugg_label.configure(text="Sugerencias: 0.75 a 1.5 (Amarillo): Se sugiere usar una ropa fresca, con un valor de clo entre 0.25 y 0.5. Por ejemplo, una camiseta de algodón, \nun pantalón corto y unas sandalias.")
        elif result <= -0.75:
            sugg_label.configure(text="Sugerencias: -1.5 a -0.75 (Amarillo): Se sugiere usar una ropa abrigada, con un valor de clo entre 1.5 y 2. Por ejemplo, un suéter de lana, un \npantalón grueso y unos zapatos cerrados.")
    else:
        color = "#F13005"
        if result >=1.5:
            sugg_label.configure(text="Sugerencias: 1.5 a 3 (Rojo): Se sugiere usar una ropa muy ligera, con un valor de clo inferior a 0.25. Por ejemplo, un traje de baño, unas gafas \nde sol y un sombrero.")
        elif result <= -1.5:
            sugg_label.configure(text="Sugerencias: -3 a -1.5 (Rojo): Se sugiere usar una ropa muy abrigada, con un valor de clo superior a 2. Por ejemplo, un abrigo de invierno, un \ngorro, unos guantes y unas botas.")

    create_circle(zone, color)

# Ventana del programa

root = tk.Tk()

root.geometry("1125x700")
root.resizable(False, False)
root.title("Habitabilidad")

# Posición del mouse 

label_position = ttk.Label(root)
label_position.place(x = 25, y = 675)
root.bind("<Motion>", lambda event: label_position.configure(text=f"{event.x}, {event.y}"))

# Imagen de grafo

img = ImageTk.PhotoImage(Image.open("static/grafo.png").resize((600, 500)))

# Canvas

canvas = tk.Canvas(root, width = 600, height = 500)
canvas.place(x = 25, y = 15)
canvas.create_image(0, 0, anchor = tk.NW, image = img)

# Labels espacios

ttk.Label(
    root,
    text = "Lista de espacios",
    font = "bold"
).place(x = 655, y = 25)

ttk.Label(
    root,
    text = "Area (m²)",
    font = "bold"
).place(x = 805, y = 25)

ttk.Label(
    root,
    text = "Parametros",
    font = "bold"
).place(x = 900, y = 25)

for zone in logica.zone_dictionary:

    index = logica.zone_dictionary.get(zone)[0]+1

    ttk.Label(
        root, 
        text = str(index)+". " + zone
        ).place(x = 655, y = (index+1)*25)
    
    ttk.Label(
        root, 
        text = str(logica.zone_dictionary.get(zone)[1])
        ).place(x = 810, y = (index+1)*25)
    

# Combobox de elección

ttk.Label(
    root,
    text = "Espacio a evaluar",
    font = "bold"
).place(x = 900, y = 55)

zone_string = tk.StringVar()

combo_zone = ttk.Combobox(
    root,
    textvariable = zone_string,
    values = list(logica.zone_dictionary.keys()),
    width = 27
)
combo_zone.place(x = 900, y = 85)

# Introducción de variables

ttk.Label(
    root,
    text = "Temperatura (C°)",
    font = "bold"
).place(x = 900, y = 115)
temp_input = tk.IntVar()
temp_entry = ttk.Entry(width = 30, textvariable = temp_input)
temp_entry.place(x = 900, y = 145)

ttk.Label(
    root,
    text = "Humedad (%)",
    font = "bold"
).place(x = 900, y = 175)
hum_input = tk.IntVar()
hum_entry = ttk.Entry(width = 30, textvariable = hum_input)
hum_entry.place(x = 900, y = 205)

ttk.Label(
    root,
    text = "Equivalente metabolico",
    font = "bold"
).place(x = 900, y = 235)
met_input = tk.IntVar()
met_entry = ttk.Entry(width= 30, textvariable=met_input)
met_entry.place(x = 900, y = 265)

ttk.Label(
    root, 
    text = "Velocidad del viento (m/s)",
    font = "bold"
).place(x = 900, y = 295)
wind_input = tk.IntVar()
wind_entry = ttk.Entry(width = 30, textvariable=wind_input)
wind_entry.place(x = 900, y = 325)

# Display de resultado

label_output = ttk.Label(
    root, 
    text = "El indice de habitabilidad (ATHB) es: ",
    font = "bold"
)
label_output.place(x = 30, y = 540)

sugg_label = ttk.Label(
    root,
    text = "Sugerencias: ",
    font = "bold"
)
sugg_label.place(x = 30, y = 570)

# Boton

button = ttk.Button(
    root,
    text = "Ejecutar",
    command = lambda: execute(temp_input.get(), wind_input.get(), hum_input.get(), met_input.get(), zone_string.get())
)
button.place(x = 1010, y = 650)


root.mainloop()