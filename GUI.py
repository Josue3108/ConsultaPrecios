import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from Funcions.Load import load_products
from Funcions.Search import search_products

class SalesApp:
    def __init__(self, root):
        # Estilo tonos pastel
        style = Style("minty")  # Tema claro con tonos pastel
        root.title("Gestor de Ventas")
        root.configure(bg="white")  # Fondo blanco

        # Espacio para el logotipo
        logo_frame = ttk.Frame(root, padding=10, style="TFrame")
        logo_frame.pack(fill=tk.X)
        ttk.Label(logo_frame, text="LOGOTIPO DE LA EMPRESA", 
                  font=("Helvetica", 20, "bold"), anchor="center", background="white").pack(pady=10)

        # Encabezado
        header = ttk.Label(root, text="Gestor de Ventas de Tienda", 
                           font=("Helvetica", 16), anchor="center", background="white")
        header.pack(pady=10)

        # Frame para buscar productos
        search_frame = ttk.Frame(root, padding=10, style="TFrame")
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Buscar Producto:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        search_button = ttk.Button(search_frame, text="Buscar", style="primary.TButton", command=self.search_product)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        
        search_frame.columnconfigure(1, weight=1)

        # Combobox para mostrar resultados
        self.result_combobox = ttk.Combobox(root, state="readonly", font=("Helvetica", 12))
        self.result_combobox.pack(fill=tk.X, padx=10, pady=10)

        # Botón para agregar artículo
        add_button = ttk.Button(root, text="Agregar Artículo", style="success.TButton", command=self.add_item)
        add_button.pack(pady=10)

        # Cargar productos desde la base de datos
        self.products = load_products()

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

    def add_item(self):
        """Agrega el artículo seleccionado del Combobox."""
        selected_item = self.result_combobox.get()
        if selected_item:
            print(f"Artículo agregado: {selected_item}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesApp(root)
    root.mainloop()
