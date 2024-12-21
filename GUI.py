import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from Funcions.Load import load_products
from Funcions.Search import search_products
from Funcions.AddFortnight import initialize_fortnight
from Funcions.Addsale import Addsale
from Funcions.getPDF import generate_pdf
from Funcions.Getquincena import get_sales_last_fortnight
from PIL import Image, ImageTk
import sqlite3

class SalesApp:
    def __init__(self, root):
        style = Style("litera")  # Aplica el tema litera
        root.title("Gestor de Ventas")
        root.configure(bg="white")  # Fondo blanco

         # Establecer el tamaño fijo de la ventana
        root.geometry("400x500")  # Tamaño fijo (600x400 píxeles)
        root.resizable(False, False)  # Desactiva la capacidad de redimensionar la ventana


        # Personalización del estilo de los botones sin borde
        style.configure("TButton",
                        font=("Helvetica", 10, "bold"),  # Fuente más pequeña
                        foreground="white",  # Color de texto blanco
                        background="blue",  # Fondo azul para los botones generales
                        padding=6,  # Reducir padding para botones más pequeños
                        relief="flat")  # Sin borde

        style.map("TButton",
                  foreground=[('active', 'yellow')],  # Cambia el color del texto cuando el botón está activo
                  background=[('active', 'darkblue')])  # Cambia el color de fondo cuando el botón está activo

        # Personalización del botón de búsqueda (verde) sin borde
        style.configure("search.TButton",
                        font=("Helvetica", 10, "bold"),  # Fuente más pequeña
                        foreground="white",  # Color de texto blanco
                        background="green",  # Fondo verde para el botón de búsqueda
                        padding=6,  # Reducir padding para un tamaño más pequeño
                        relief="flat")  # Sin borde

        style.map("search.TButton",
                  foreground=[('active', 'yellow')],  # Cambia el color del texto cuando el botón está activo
                  background=[('active', 'darkgreen')])  # Cambia el color de fondo cuando el botón está activo

        # Conexión a la base de datos
        self.connection = sqlite3.connect("ReportePagosBVLabs.db")

        # Inicializar la quincena automáticamente
        try:
            initialize_fortnight(self.connection)
        except Exception as e:
            print(f"Error al inicializar la quincena: {e}")

        # Espacio para el logotipo
        logo_frame = ttk.Frame(root, padding=10)
        logo_frame.pack(fill=tk.X)

        try:
            image = Image.open("Images/BV LABS.jpg")
            image = image.resize((200, 200))  # Ajusta el tamaño según sea necesario
            self.logo_image = ImageTk.PhotoImage(image)
            ttk.Label(logo_frame, image=self.logo_image, anchor="center", background="white").pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar el logotipo: {e}")
            ttk.Label(logo_frame, text="LOGOTIPO DE LA EMPRESA", 
                    font=("Helvetica", 20, "bold"), anchor="center", background="white").pack(pady=10)

        # Frame para buscar productos
        search_frame = ttk.Frame(root, padding=10)
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Buscar Producto:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botón de búsqueda con estilo verde y sin borde
        search_button = ttk.Button(search_frame, text="Buscar", style="search.TButton", command=self.search_product)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        
        search_frame.columnconfigure(1, weight=1)

        self.search_entry.bind("<Return>", self.search_product_event)

        # Combobox para mostrar resultados
        self.result_combobox = ttk.Combobox(root, state="readonly", font=("Helvetica", 12))
        self.result_combobox.pack(fill=tk.X, padx=10, pady=10)

        # Cuadro para ingresar la cantidad
        quantity_frame = ttk.Frame(root, padding=10)
        quantity_frame.pack(fill=tk.X)

        ttk.Label(quantity_frame, text="Cantidad:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.quantity_entry = ttk.Entry(quantity_frame)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        quantity_frame.columnconfigure(1, weight=1)

        # Frame para botones
        button_frame = ttk.Frame(root, padding=10)
        button_frame.pack(fill=tk.X)

        # Botón para agregar artículo sin borde
        add_button = ttk.Button(button_frame, text="Registrar Venta", style="TButton", command=self.register_sale)
        add_button.grid(row=0, column=0, padx=5, pady=5)

        # Botón para ver reporte
        report_button = ttk.Button(button_frame, text="Ver Reporte", style="TButton", command=self.view_report)
        report_button.grid(row=0, column=1, padx=5, pady=5)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Cargar productos desde la base de datos
        self.products = load_products()

    def search_product_event(self, event=None):
        """Maneja el evento de presionar Enter en el campo de búsqueda."""
        self.search_product()

    def search_product(self):
        """Filtra los productos según el término ingresado."""
        search_term = self.search_entry.get()
        results = search_products(self.products, search_term)
        
        # Actualiza el combobox con los resultados
        self.result_combobox["values"] = results
        if results:
            self.result_combobox.current(0)  # Selecciona el primer elemento automáticamente
        else:
            self.result_combobox.set("")  # Limpia si no hay resultados

    def register_sale(self):
        """Registra la venta del artículo seleccionado en la base de datos."""
        selected_item = self.result_combobox.get()
        quantity = self.quantity_entry.get()

        if not selected_item:
            print("Por favor selecciona un producto.")
            return

        if not quantity.isdigit() or int(quantity) <= 0:
            print("Por favor ingresa una cantidad válida.")
            return

        try:
            Addsale(self.connection, selected_item, int(quantity))
        except Exception as e:
            print(f"Error al registrar la venta: {e}")

    def view_report(self):
        """Muestra el reporte de ventas."""
        data = get_sales_last_fortnight(self.connection)
        print(data)
        generate_pdf(data)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesApp(root)
    root.mainloop()
