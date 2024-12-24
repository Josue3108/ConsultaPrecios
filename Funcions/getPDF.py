from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from tkinter import filedialog

def generate_pdf(data):
    """
    Esto genera un archivo PDF con la información y permite al usuario elegir la ubicación para guardarlo.

    Args:
        data (dict): Diccionario con las claves 'name', 'price', 'quantity', 'fortnight_name',
                     'total_price', 'iva', y 'total_iva_price'.

    Returns:
        None
    """
    # Abrir un cuadro de diálogo para seleccionar dónde guardar el archivo
    output_file = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Guardar reporte como"
    )

    if not output_file:
        print("Operación cancelada por el usuario.")
        return
    
    try:
        # Crear el PDF
        c = SimpleDocTemplate(output_file, pagesize=letter) #utiliza simpledocs para crear un pdf

        elements = []

        # Estilos para texto
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "Title",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=colors.darkblue,
            alignment=1,
        )
        #estilos para substexto , por si se necesita agregar
        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=12,
            textColor=colors.darkgray,
            alignment=1,
        )
        #iteracion para obtener los datos de presentacion del reporte:
        primera_venta = next(iter(data.values()))
        ventaQuincena = primera_venta["overall_Price"]
        ventaquincenaIva = primera_venta["overall_price_iva"]
        quincena = primera_venta["quincena"]
        # Título y subtítulo
        elements.append(Paragraph("Reporte de Ventas ", title_style))
        elements.append(Paragraph("\n"))  # Espacio
        elements.append(Paragraph(f"Reporte de la quincena: {quincena}", subtitle_style))
        elements.append(Paragraph("\n"))  # Espacio
        elements.append(Paragraph(f"Venta quincenal sin IVA : {ventaQuincena}", subtitle_style))
        elements.append(Paragraph("\n"))  # Espacio
        elements.append(Paragraph(f"Venta quincenal con IVA : {ventaquincenaIva}", subtitle_style))
        # Encabezados de la tabla , son los titulos del query
        table_data = [
            ["Producto", "Precio (CR)", "Cantidad", "Precio Total (CR)", "IVA (CR)", "Total con IVA (CR)"]
        ]
        for key, row in data.items():  # Iterar sobre los elementos del diccionario
            table_data.append([
                row["name"],  # Nombre del producto
                row['price'],  # Precio con 2 decimales
                row["quantity"],  # Cantidad
                row['total_price'],  # Precio total con 2 decimales
                row['iva'],  # IVA con 2 decimales
                row['total_price_with_iva']   # Total con IVA con 2 decimales
            ])


        # Tabla con estilo
        table = Table(table_data, colWidths=[100, 80, 60, 100, 100, 60, 100])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),  # Fondo para encabezado
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco en encabezado
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Centrar texto
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Fuente en encabezado
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),  # Fuente para datos
            ("FONTSIZE", (0, 0), (-1, -1), 10),  # Tamaño de fuente
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),  # Espaciado inferior en encabezado
            ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),  # Líneas de tabla
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Fondo para filas
        ]))
        elements.append(table)

    # Construir PDF
        c.build(elements)
        print(f"PDF guardado correctamente en: {output_file}")

    except PermissionError as e:
        print(f"Error: No se tienen permisos para escribir en esta ubicación: {e}")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")

