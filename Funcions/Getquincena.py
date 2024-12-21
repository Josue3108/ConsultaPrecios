import sqlite3
from .GetFortnight import get_last_fortnight

def get_sales_last_fortnight(connection):
    """
    Obtiene producto, cantidad vendida, precio unitario, precio total sin IVA y precio total con IVA.

    Parameters:
        connection: sqlite3.Connection - Conexión activa a la base de datos.

    Returns:
        dict - Información de las ventas de la última quincena o None si no existe ninguna.
    """
    try:
        cursor = connection.cursor()
        # Obtener la última quincena
        busqueda_quincena = get_last_fortnight(connection)
        if not busqueda_quincena:
            print("No se encontró la última quincena.")
            return None
        
        id_quincena = busqueda_quincena["id"]

        # Ejecutar la consulta
        cursor.execute('''
            SELECT 
                Products.name, 
                Products.price, 
                Sales.quantity, 
                Products.price * Sales.quantity AS total_price, 
                (Products.price * 0.13) AS iva, 
                ((Products.price * 0.13) + Products.price) * Sales.quantity AS total_price_with_iva
            FROM Sales
            INNER JOIN Products ON Sales.product_id = Products.id
            INNER JOIN SalesperFortnight ON Sales.fortnight_id = SalesperFortnight.id
            WHERE SalesperFortnight.id = ?
            ORDER BY Sales.quantity DESC
        ''', (id_quincena,))

        rows = cursor.fetchall()

        if rows:
            # Convertir los resultados a un formato de diccionario
            result = {}
            for i, row in enumerate(rows):
                result[f"venta_{i+1}"] = {
                    "name": row[0],
                    "price": row[1],
                    "quantity": row[2],
                    "total_price": row[3],
                    "iva": row[4],
                    "total_price_with_iva": row[5],
                }
            return result
        else:
            print("No se encontraron ventas para la última quincena.")
            return None

    except sqlite3.Error as e:
        print(f"Error al obtener las ventas de la última quincena: {e}")
        return None
