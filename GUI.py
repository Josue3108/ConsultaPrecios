import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkbootstrap import Style
from PIL import Image, ImageTk
import sqlite3

from DataBase.Script import setup_database, connect_to_database
from DataBase.Import import import_products_from_excel

# Tus imports de funciones específicas
from Funcions.Load import load_products
from Funcions.Search import search_products
from Funcions.AddFortnight import initialize_fortnight, add_sales_per_fortnight
from Funcions.Addsale import Addsale
from Funcions.getPDF import generate_sales_report
from Funcions.GetFortnight import get_last_fortnight
from Funcions.DeleteSale import delete_sale_by_product_and_fortnight_id

import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS  # Ruta temporal cuando es ejecutable
    except AttributeError:
        base_path = os.path.abspath(".")  # Ruta normal cuando se ejecuta como script
    return os.path.join(base_path, relative_path)

class SalesApp:
    def __init__(self, root):
        style = Style("litera")
        root.title("Gestor de Ventas")
        root.configure(bg="white")
        root.geometry("800x700")
        root.resizable(False, False)

        # Conectar a la base de datos
        self.connection = connect_to_database()

        setup_database()

        try:
            initialize_fortnight(self.connection)
        except Exception as e:
            print(f"Error al inicializar la quincena: {e}")

        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame, padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame, width=200, padding=10)
        left_frame.pack(side=tk.RIGHT, fill=tk.Y)

        logo_frame = ttk.Frame(right_frame, padding=10)
        logo_frame.pack(fill=tk.X)

        try:
            image_path = resource_path("Images/BV_LABS.jpg")
            image = Image.open(image_path).resize((200, 200))
            self.logo_image = ImageTk.PhotoImage(image)
            ttk.Label(logo_frame, image=self.logo_image, anchor="center", background="white").pack(pady=10)
        except Exception as e:
            print(f"No se pudo cargar el logotipo: {e}")
            ttk.Label(logo_frame, text="LOGOTIPO DE LA EMPRESA", font=("Helvetica", 20, "bold"), anchor="center", background="white").pack(pady=10)

        # Botón para importar productos
        import_button = ttk.Button(right_frame, text="Importar Productos desde Excel", command=self.import_products)
        import_button.pack(pady=5)

        search_frame = ttk.Frame(right_frame, padding=10)
        search_frame.pack(fill=tk.X)
        ttk.Label(search_frame, text="Buscar Producto:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        search_button = ttk.Button(search_frame, text="Buscar", command=self.search_product)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        search_frame.columnconfigure(1, weight=1)
        self.search_entry.bind("<Return>", self.search_product_event)

        self.result_combobox = ttk.Combobox(right_frame, state="readonly", font=("Helvetica", 12))
        self.result_combobox.pack(fill=tk.X, padx=10, pady=10)

        self.company_vars = {c: tk.BooleanVar(value=True) for c in ["Lab SJ", "Suplilab", "CitoVet"]}
        company_frame = ttk.Frame(right_frame, padding=10)
        company_frame.pack(fill=tk.X)
        for company, var in self.company_vars.items():
            ttk.Checkbutton(company_frame, text=company, variable=var).pack(side=tk.LEFT, padx=5)

        quantity_frame = ttk.Frame(right_frame, padding=10)
        quantity_frame.pack(fill=tk.X)
        ttk.Label(quantity_frame, text="Cantidad:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(quantity_frame)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        quantity_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(right_frame, padding=10)
        button_frame.pack(fill=tk.X)
        button_frame.columnconfigure((0, 1), weight=1)
        button_frame.rowconfigure((0, 1), weight=1)
        ttk.Button(button_frame, text="Registrar Venta", command=self.register_sale).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Ver Reporte", command=self.view_report).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Nuevo Reporte", command=self.generate_new_report).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Borrar Venta", command=self.delete_selected_sale).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(left_frame, text="Ventas del Día", font=("Helvetica", 14, "bold"), background="lightblue", anchor="w").pack(fill=tk.X, pady=5)

        self.sales_tree = ttk.Treeview(left_frame, columns=("Producto", "Cantidad"), show="headings", height=10)
        self.sales_tree.heading("Producto", text="Producto")
        self.sales_tree.heading("Cantidad", text="Cantidad")

        self.sales_tree.column("Producto", width=250, anchor="w")
        self.sales_tree.column("Cantidad", width=100, anchor="center")

        self.sales_tree.tag_configure("oddrow", background="#f9f9f9")
        self.sales_tree.tag_configure("evenrow", background="#e9e9e9")

        self.sales_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Button(left_frame, text="Guardar Ventas", command=self.save_sales).pack(pady=5)

        self.products = load_products()
        self.pending_sales = []

    def import_products(self):
        file_path = resource_path("PRECIOS_LAB_SJ.xlsx")
        if not file_path:
            return

        success, message = import_products_from_excel(file_path)
        messagebox.showinfo("Importar Productos", message)
        if success:
            # Recargar productos tras la importación
            self.products = load_products()

    def search_product_event(self, event=None):
        self.search_product()

    def search_product(self):
        search_term = self.search_entry.get()
        selected_companies = [company for company, var in self.company_vars.items() if var.get()]
        filtered_products = search_products(self.products, search_term, selected_companies)
        self.result_combobox["values"] = filtered_products
        if filtered_products:
            self.result_combobox.current(0)
        else:
            self.result_combobox.set("")

    def register_sale(self):
        selected_item = self.result_combobox.get()
        quantity = self.quantity_entry.get()
        if not selected_item or not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showwarning("Error", "Selecciona un producto y cantidad válida.")
            return
        item_id = self.sales_tree.insert("", "end", values=(selected_item, quantity))
        self.pending_sales.append((item_id, selected_item, int(quantity)))
        print(f"Venta provisional agregada: {selected_item} x{quantity}")

    def delete_selected_sale(self):
        selected_item = self.sales_tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Selecciona una venta para borrar.")
            return
        for item in selected_item:
            values = self.sales_tree.item(item, "values")
            self.sales_tree.delete(item)
            self.pending_sales = [sale for sale in self.pending_sales if sale[1] != values[0] or str(sale[2]) != values[1]]
        messagebox.showinfo("Venta borrada", "La venta seleccionada ha sido borrada.")

    from tkinter import messagebox

    def save_sales(self):
        if not self.pending_sales:
            messagebox.showinfo("Información", "No hay ventas pendientes para guardar.")
            return

        confirm = messagebox.askyesno(
            "Confirmar Guardado",
            "¿Estás seguro que quieres guardar las ventas pendientes en la base de datos?\n"
            "Si confirmas, las ventas se guardarán y se eliminarán de la lista temporal."
        )
        if not confirm:
            return

        for _, product_name, quantity in self.pending_sales:
            Addsale(self.connection, product_name, quantity)

        # Limpiar las ventas pendientes y la vista visual solo si el usuario confirmó
        self.pending_sales.clear()

        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        messagebox.showinfo("Ventas guardadas", "Ventas guardadas correctamente y eliminadas de la lista temporal.")


    def view_report(self):
        try:
            data = get_last_fortnight(self.connection)
            generate_sales_report(data['id'])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}")

    def generate_new_report(self):
        try:
            add_sales_per_fortnight(self.connection)
            messagebox.showinfo("Reporte", "Nueva quincena agregada.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar nueva quincena:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesApp(root)
    root.mainloop()
