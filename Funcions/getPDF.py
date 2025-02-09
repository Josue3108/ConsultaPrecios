import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Image
from tkinter import Tk, filedialog
import os
from datetime import datetime

def connect_to_database():
    """Conecta a la base de datos SQLite."""
    connection = sqlite3.connect("ReportePagosBVLabs.db")
    print(f"Conectado a la base de datos: ReportePagosBVLabs.db")
    return connection

def get_sales_by_fortnight(connection, fortnight_id):
    """Obtiene las ventas de productos para una quincena específica, incluyendo el porcentaje de IVA."""
    query = '''
        SELECT 
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
        WHERE SalesperFortnight.id = ?;
    '''
    cursor = connection.cursor()
    cursor.execute(query, (fortnight_id,))
    sales_data = cursor.fetchall()
    cursor.close()
    return sales_data

def generate_sales_report(fortnight_id):
    """Genera un reporte de ventas por quincena en formato PDF con ubicación seleccionada por el usuario."""
    try:
        conn = connect_to_database()
        print("Obteniendo ventas...")
        sales = get_sales_by_fortnight(conn, fortnight_id)
        
        if not sales:
            print(f"No se encontraron ventas para la quincena con ID {fortnight_id}.")
            return
        
        sales_fortnight = sales[0][5]  # Nombre de la quincena
        safe_filename = f"Reporte_Ventas_{sales_fortnight}"
        safe_filename = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in safe_filename)

        print("Seleccionando ubicación para guardar el archivo...")
        root = Tk()
        root.withdraw()
        root.update()
        output_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar Reporte de Ventas",
            initialfile=safe_filename
        )
        root.destroy()
        
        if not output_filename:
            print("Generación del reporte cancelada.")
            return

        print("Generando el PDF...")
        c = canvas.Canvas(output_filename, pagesize=A4)
        width, height = A4
        
        # Agregar logo en la esquina superior izquierda
        logo_path = "Images\BV LABS.jpg"  # Ruta del logo
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 40, height - 80, width=80, height=50, mask='auto')
        
        current_date = datetime.now().strftime("%d/%m/%Y")
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.black)
        c.drawString(450, height - 50, f"Fecha: {current_date}")
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.darkblue)
        c.drawString(50, height - 100, f"Reporte de Ventas - {sales_fortnight}")
        
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
        
        for row in sales:
            product_name = row[0]
            price = float(row[1].replace(',', ''))
            quantity = row[2]
            iva_percentage = row[6] / 100  # Convertir a decimal
            
            total_product = price * quantity
            iva_value = total_product * iva_percentage
            total_with_iva = total_product + iva_value
            
            total_price += total_product
            total_iva += iva_value
            
            max_product_length = 30  # Número máximo de caracteres por línea
            product_lines = [product_name[i:i+max_product_length] for i in range(0, len(product_name), max_product_length)]
            
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
        conn.close()
        print(f"Reporte guardado como: {output_filename}")
    
    except Exception as e:
        print(f"Error al generar el reporte: {e}")
    finally:
        if conn:
            conn.close()

