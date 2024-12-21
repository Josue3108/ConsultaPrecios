from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
        c = canvas.Canvas(output_file, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 50, "Reporte de Producto")

        # Escribir los datos en el PDF
        y = height - 100
        for key, value in data.items():
            c.drawString(50, y, f"{key.capitalize()}: {value}")
            y -= 20  # Ajustar la posición vertical para cada línea

        # Finalizar y guardar el documento
        c.save()
        print(f"PDF guardado correctamente en: {output_file}")

    except PermissionError as e:
        print(f"Error: No se tienen permisos para escribir en esta ubicación: {e}")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
