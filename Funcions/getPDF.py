from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from tkinter import Tk, filedialog
import os
import sqlite3
import traceback
from datetime import datetime
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller lo define al ejecutar el .exe
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def connect_to_database():
    """Conecta a la base de datos SQLite."""
    db_path = resource_path("ReportePagosBVLabs.db")
    connection = sqlite3.connect(db_path)
    print(f"Conectado a la base de datos: {db_path}")
    return connection

def get_sales_grouped_by_supplier(connection, fortnight_id):
    """Devuelve un diccionario {proveedor: lista_de_ventas} para una quincena específica."""
    query = '''
        SELECT 
            Products.supplier AS supplier_name,
            Products.name AS product_name,
            Products.price AS product_price,
            Sales.quantity AS product_quantity,
            SalesperFortnight.month AS sales_month,
            SalesperFortnight.year AS sales_year,
            SalesperFortnight.fortnight_name AS sales_fortnight,
            Products.tax_rate AS product_iva
        FROM Sales
        INNER JOIN Products ON Sales.product_id = Products.id
        INNER JOIN SalesperFortnight ON Sales.fortnight_id = SalesperFortnight.id
        WHERE SalesperFortnight.id = ?
        ORDER BY supplier_name;
    '''
    cursor = connection.cursor()
    cursor.execute(query, (fortnight_id,))
    rows = cursor.fetchall()
    cursor.close()

    grouped = {}
    for row in rows:
        supplier = row[0]
        if supplier not in grouped:
            grouped[supplier] = []
        grouped[supplier].append(row[1:])
    return grouped

def generate_sales_report(fortnight_id):
    """Genera un PDF de ventas agrupando productos por proveedor para una quincena específica."""
    conn = None
    try:
        conn = connect_to_database()
        grouped_sales = get_sales_grouped_by_supplier(conn, fortnight_id)

        if not grouped_sales:
            print(f"No se encontraron ventas para la quincena con ID {fortnight_id}.")
            return

        for supplier, sales in grouped_sales.items():
            sales_fortnight = sales[0][5]
            safe_supplier = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in supplier)
            safe_fortnight = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in sales_fortnight)
            safe_filename = f"Reporte_{safe_supplier}_{safe_fortnight}.pdf"

            root = Tk()
            root.withdraw()
            root.update()
            output_filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")],
                title=f"Guardar Reporte de {supplier}",
                initialfile=safe_filename
            )
            root.destroy()

            if not output_filename:
                print(f"Generación del reporte para {supplier} cancelada.")
                continue

            products_summary = {}
            for row in sales:
                product_name = row[0]
                product_price = float(row[1].replace(',', '')) if isinstance(row[1], str) else float(row[1])
                quantity = row[2]
                iva_percentage = row[6] / 100

                if product_name not in products_summary:
                    products_summary[product_name] = {
                        "price": product_price,
                        "quantity": quantity,
                        "iva_percentage": iva_percentage
                    }
                else:
                    products_summary[product_name]["quantity"] += quantity

            c = canvas.Canvas(output_filename, pagesize=A4)
            width, height = A4

            logo_path = resource_path("Images/BV LABS.jpg")
            if os.path.exists(logo_path):
                c.drawImage(logo_path, 40, height - 80, width=80, height=50, mask='auto')

            current_date = datetime.now().strftime("%d/%m/%Y")
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.black)
            c.drawString(450, height - 50, f"Fecha: {current_date}")

            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.darkblue)
            c.drawString(50, height - 100, f"Reporte de Ventas - {sales_fortnight} - {supplier}")

            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.red)
            c.drawString(50, height - 130, "Producto")
            c.drawString(180, height - 130, "Cantidad")
            c.drawString(240, height - 130, "IVA %")
            c.drawString(280, height - 130, "Precio")
            c.drawString(360, height - 130, "Total sin IVA")
            c.drawString(450, height - 130, "Total con IVA")

            c.setFont("Helvetica", 7)
            c.setFillColor(colors.black)
            y = height - 150
            total_price = 0
            total_iva = 0

            for product_name, data in products_summary.items():
                price = data["price"]
                quantity = data["quantity"]
                iva_percentage = data["iva_percentage"]

                total_product = price * quantity
                iva_value = total_product * iva_percentage
                total_with_iva = total_product + iva_value

                total_price += total_product
                total_iva += iva_value

                max_product_length = 30
                product_lines = [product_name[i:i + max_product_length] for i in range(0, len(product_name), max_product_length)]

                for line in product_lines:
                    c.drawString(50, y, line)
                    y -= 12

                c.drawString(200, y + 12, str(quantity))
                c.drawString(240, y + 12, f"{iva_percentage * 100:.1f}%")
                c.drawString(280, y + 12, f"¢ {price:,.2f}")
                c.drawString(360, y + 12, f"¢ {total_product:,.2f}")
                c.drawString(450, y + 12, f"¢ {total_with_iva:,.2f}")
                y -= 18

            total_with_iva_final = total_price + total_iva
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.black)
            c.drawString(50, y - 20, f"Total sin IVA: ¢ {total_price:,.2f}")
            c.drawString(50, y - 40, f"Total IVA: ¢ {total_iva:,.2f}")
            c.drawString(50, y - 60, f"Total con IVA: ¢ {total_with_iva_final:,.2f}")

            c.save()
            print(f"Reporte de {supplier} guardado como: {output_filename}")

    except Exception as e:
        print(f"Error al generar el reporte: {e}")
        traceback.print_exc()
    finally:
        if conn:
            conn.close()
