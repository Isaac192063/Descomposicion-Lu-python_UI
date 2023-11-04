import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Fracción")

# Definir la fracción
numerador = 3
denominador = 4

# Usar una fuente Unicode con símbolos de fracción
fuente = ("Arial", 24)

# Etiqueta para mostrar la fracción con identificación de numerador y denominador
fraccion_label = tk.Label(ventana, text=f"{numerador}⁄{denominador}", font=fuente)
numerador_label = tk.Label(ventana, text="Numerador", font=("Arial", 12))
denominador_label = tk.Label(ventana, text="Denominador", font=("Arial", 12))

# Colocar las etiquetas en la ventana
numerador_label.pack()
fraccion_label.pack()
denominador_label.pack()

ventana.mainloop()
