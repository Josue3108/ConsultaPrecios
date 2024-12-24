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
        nombre_quincena = busqueda_quincena["fortnight_name"]
        # Ejecutar la consulta
        cursor.execute('''
            SELECT 
                Products.name AS name, 
                Products.price AS price, 
                Sales.quantity AS quantity, 
                (Products.price * Sales.quantity) AS total_price, 
                ROUND((Products.price * 0.13),2) AS iva, 
                (((Products.price * 0.13) + Products.price) * Sales.quantity) AS total_price_with_iva,
                SUM(Products.price * Sales.quantity) OVER() AS overall_Price,
                SUM((((Products.price * 0.13) + Products.price) * Sales.quantity)) OVER() as overall_price_iva
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
                    "price":row[1], #forzado de conversion de tipos, quick fix
                    "quantity": row[2],
                    "total_price": int(row[3]),
                    "iva": float(row[4]),
                    "total_price_with_iva": float(row[5]),
                    "overall_Price": int(row[6]),
                    "overall_price_iva": float(row[7]),
                    "quincena":nombre_quincena
                }
            return result
        else:
            print("No se encontraron ventas para la última quincena.")
            return None

    except sqlite3.Error as e:
        print(f"Error al obtener las ventas de la última quincena: {e}")
        return None
