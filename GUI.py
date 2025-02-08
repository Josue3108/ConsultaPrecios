import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from Funcions.Load import load_products
from Funcions.Search import search_products
from Funcions.AddFortnight import initialize_fortnight
from Funcions.Addsale import Addsale
from Funcions.getPDF import generate_sales_report
from Funcions.GetFortnight import get_last_fortnight
from Funcions.AddFortnight import add_sales_per_fortnight
from Funcions.DeleteSale import delete_sale_by_product_and_fortnight_id
from PIL import Image, ImageTk
import sqlite3

class SalesApp:
    def __init__(self, root):
        style = Style("litera")  
        root.title("Gestor de Ventas")
        root.configure(bg="white")  
        root.geometry("400x550")  
        root.resizable(False, False)  

        style.configure("TButton",
                        font=("Helvetica", 10, "bold"),
                        foreground="white",
                        background="blue",
                        padding=6,
                        relief="flat")

        style.map("TButton",
                  foreground=[('active', 'yellow')],
                  background=[('active', 'darkblue')])

        style.configure("search.TButton",
                        font=("Helvetica", 10, "bold"),
                        foreground="white",
                        background="green",
                        padding=6,
                        relief="flat")

        style.map("search.TButton",
                  foreground=[('active', 'yellow')],
                  background=[('active', 'darkgreen')])

        self.connection = sqlite3.connect("ReportePagosBVLabs.db")

        try:
            initialize_fortnight(self.connection)
        except Exception as e:
            print(f"Error al inicializar la quincena: {e}")

        logo_frame = ttk.Frame(root, padding=10)
        logo_frame.pack(fill=tk.X)

        try:
            image = Image.open("Images/BV LABS.jpg")
            image = image.resize((200, 200))
            self.logo_image = ImageTk.PhotoImage(image)
            ttk.Label(logo_frame, image=self.logo_image, anchor="center", background="white").pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar el logotipo: {e}")
            ttk.Label(logo_frame, text="LOGOTIPO DE LA EMPRESA", font=("Helvetica", 20, "bold"), anchor="center",
                      background="white").pack(pady=10)

        search_frame = ttk.Frame(root, padding=10)
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Buscar Producto:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        search_button = ttk.Button(search_frame, text="Buscar", style="search.TButton", command=self.search_product)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        search_frame.columnconfigure(1, weight=1)
        self.search_entry.bind("<Return>", self.search_product_event)

        self.result_combobox = ttk.Combobox(root, state="readonly", font=("Helvetica", 12))
        self.result_combobox.pack(fill=tk.X, padx=10, pady=10)

        quantity_frame = ttk.Frame(root, padding=10)
        quantity_frame.pack(fill=tk.X)

        ttk.Label(quantity_frame, text="Cantidad:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.quantity_entry = ttk.Entry(quantity_frame)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        quantity_frame.columnconfigure(1, weight=1)

        # FRAME PARA LOS BOTONES, 2 COLUMNAS x 2 FILAS
        button_frame = ttk.Frame(root, padding=10)
        button_frame.pack(fill=tk.X)

        button_frame.columnconfigure((0, 1), weight=1)  # 2 columnas
        button_frame.rowconfigure((0, 1), weight=1)  # 2 filas

        ttk.Button(button_frame, text="Registrar Venta", style="TButton", command=self.register_sale).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Ver Reporte", style="TButton", command=self.view_report).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Nuevo Reporte", style="TButton", command=self.generate_new_report).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Borrar Venta", style="TButton", command=self.delete_sale).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.products = load_products()

    def search_product_event(self, event=None):
        self.search_product()

    def search_product(self):
        search_term = self.search_entry.get()
        results = search_products(self.products, search_term)
        self.result_combobox["values"] = results
        if results:
            self.result_combobox.current(0)
        else:
            self.result_combobox.set("")

    def register_sale(self):
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
            print(f"Venta registrada: {selected_item} x{quantity}")
        except Exception as e:
            print(f"Error al registrar la venta: {e}")

    def view_report(self):
        data = get_last_fortnight(self.connection)
        generate_sales_report(data['id'])
        print("Reporte de ventas generado.")

    def generate_new_report(self):
        add_sales_per_fortnight(self.connection)

    def delete_sale(self):
        selected_item = self.result_combobox.get()
        if not selected_item:
            print("Por favor selecciona una venta para borrar.")
            return
        
        data = get_last_fortnight(self.connection)
        delete_sale_by_product_and_fortnight_id(self.connection ,selected_item, data['id'])


if __name__ == "__main__":
    root = tk.Tk()
    app = SalesApp(root)
    print("Interfaz iniciada")  # Debug
    root.mainloop()
