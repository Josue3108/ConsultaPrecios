import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from tkinter import Tk, filedialog
import os
from datetime import datetime

# Conectar a la base de datos
def connect_to_database():
    """Conecta a la base de datos SQLite."""
    connection = sqlite3.connect("ReportePagosBVLabs.db")
    print(f"Conectado a la base de datos: ReportePagosBVLabs.db")
    return connection

# Función para obtener las ventas por quincena
def get_sales_by_fortnight(connection, fortnight_id):
    """Obtiene las ventas de productos para una quincena específica."""
    query = '''
        SELECT 
            Products.name AS product_name,
            Products.price AS product_price,
            Sales.quantity AS product_quantity,
            SalesperFortnight.month AS sales_month,
            SalesperFortnight.year AS sales_year,
            SalesperFortnight.fortnight_name AS sales_fortnight
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

# Función para generar el reporte de ventas en PDF
def generate_sales_report(fortnight_id):
    """Genera un reporte de ventas por quincena en formato PDF con ubicación seleccionada por el usuario."""
    conn = connect_to_database()
    sales = get_sales_by_fortnight(conn, fortnight_id)
    
    if not sales:
        print(f"No se encontraron ventas para la quincena con ID {fortnight_id}.")
        return
    
    sales_fortnight = sales[0][5]  # Nombre de la quincena
    
    safe_filename = f"Reporte_Ventas_{sales_fortnight}.pdf"
    safe_filename = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in safe_filename)

    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    output_filename = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")],
        title="Guardar Reporte de Ventas",
        initialfile=safe_filename
    )

    if not output_filename:
        print("Generación del reporte cancelada.")
        return

    try:
        c = canvas.Canvas(output_filename, pagesize=A4)
        width, height = A4
        
        # **Encabezado con logo**
        logo_path = "Images\BV LABS.jpg"  # Asegúrate de que el archivo está en la misma carpeta
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 50, height - 80, width=100, height=50, preserveAspectRatio=True, mask='auto')
        
        # **Fecha de facturación**
        current_date = datetime.now().strftime("%d/%m/%Y")
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)
        c.drawString(450, height - 50, f"Fecha: {current_date}")
        
        # **TÍTULO**
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkblue)
        c.drawString(50, height - 100, f"Reporte de Ventas - {sales_fortnight}")
        
        # **Encabezado de columnas**
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.red)
        c.drawString(50, height - 130, "Producto")
        c.drawString(200, height - 130, "Precio")
        c.drawString(300, height - 130, "Cantidad")
        c.drawString(400, height - 130, "Total Producto")
        
        # **Datos de ventas**
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        y = height - 150
        max_product_name_width = 140
        total_price = 0
        
        for row in sales:
            price = float(row[1].replace(',', ''))
            quantity = row[2]
            total_product = price * quantity
            
            total_price += total_product
            
            product_name = row[0]
            lines = []
            current_line = ""
            for word in product_name.split():
                if c.stringWidth(current_line + " " + word, "Helvetica", 10) <= max_product_name_width:
                    current_line += " " + word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
            
            for i, line in enumerate(lines):
                c.drawString(50, y - i * 12, line)
            y -= len(lines) * 12
            
            c.drawString(200, y, f"¢ {price:,.2f}")
            c.drawString(300, y, str(quantity))
            c.drawString(400, y, f"¢ {total_product:,.2f}")
            y -= 20

        iva = total_price * 0.13
        total_with_iva = total_price + iva
        
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)
        c.drawString(50, y - 20, f"Total sin IVA: ¢ {total_price:,.2f}")
        c.drawString(50, y - 40, f"IVA (13%): ¢ {iva:,.2f}")
        c.drawString(50, y - 60, f"Total con IVA: ¢ {total_with_iva:,.2f}")
        
        c.save()
        conn.close()
        print(f"Reporte guardado como: {output_filename}")
    
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
