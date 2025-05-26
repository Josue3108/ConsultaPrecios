import sqlite3
from .GetFortnight import get_last_fortnight

def get_sales_by_supplier_last_fortnight(connection):
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
                Products.supplier AS supplier,
                Products.name AS name, 
                Products.price AS price, 
                Sales.quantity AS quantity, 
                (Products.price * Sales.quantity) AS total_price, 
                ROUND((Products.price * Products.tax_rate / 100.0), 2) AS iva, 
                ((Products.price + (Products.price * Products.tax_rate / 100.0)) * Sales.quantity) AS total_price_with_iva
            FROM Sales
            INNER JOIN Products ON Sales.product_id = Products.id
            INNER JOIN SalesperFortnight ON Sales.fortnight_id = SalesperFortnight.id
            WHERE SalesperFortnight.id = ?
            ORDER BY Products.supplier, Sales.quantity DESC
        ''', (id_quincena,))
        rows = cursor.fetchall()

        if not rows:
            print("No se encontraron ventas para la última quincena.")
            return None

        # Agrupar por proveedor
        data_by_supplier = {}
        for row in rows:
            supplier = row[0]
            if supplier not in data_by_supplier:
                data_by_supplier[supplier] = {
                    "quincena": nombre_quincena,
                    "ventas": []
                }
            data_by_supplier[supplier]["ventas"].append({
                "name": row[1],
                "price": row[2],
                "quantity": row[3],
                "total_price": row[4],
                "iva": row[5],
                "total_price_with_iva": row[6]
            })

        return data_by_supplier

    except sqlite3.Error as e:
        print(f"Error al obtener ventas por proveedor: {e}")
        return None
