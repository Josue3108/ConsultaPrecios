import sqlite3

def search_products_by_name(connection, search_text):
    """Busca productos cuyo nombre contenga el texto proporcionado."""
    try:
        cursor = connection.cursor()
        
        # Consulta para buscar productos cuyo nombre contenga el texto proporcionado
        query = '''
            SELECT id, name, price 
            FROM Products 
            WHERE name LIKE ?;
        '''
        
        # El "%" se usa como comodín para buscar coincidencias con el texto proporcionado
        cursor.execute(query, ('%' + search_text + '%',))
        results = cursor.fetchall()
        
        if results:
            # Si se encuentran productos, los mostramos en un formato adecuado
            products = []
            for row in results:
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'price': row[2]
                })
            return products
        else:
            print(f"No se encontraron productos con el nombre que contenga '{search_text}'.")
            return []
    except sqlite3.Error as e:
        print(f"Error al realizar la consulta: {e}")
        return []
    finally:
        cursor.close()
        #funcion que busca las ventas totales por nombre de producto en un mes y año especifico, falta de mejorarlo
        #considerar que falta hacer suma de precios para obtener el total.
def search_sales_by_month_year(connection, month, year):
    """Busca productos cuyo nombre contenga el texto proporcionado."""
    try:
        cursor = connection.cursor()
        
        # Consulta para buscar productos cuyo nombre contenga el texto proporcionado
        query = '''
            SELECT Products.name AS prod_name, SUM(Sales.quantity) AS vent_prod, SalesperFortnight.month AS mes  ,SalesperFortnight.year AS year_table,
            SUM(Sales.quantity * Products.price) AS total_vendido
            FROM Sales 
            INNER JOIN SalesperFortnight ON Sales.fortnight_id = SalesperFortnight.id
            INNER JOIN Products ON Sales.product_id = Products.id
            GROUP BY prod_name HAVING mes=month AND year_table =year AND total_vendido > 0
            ORDER BY total_vendido DESC
        '''
        
        # El "%" se usa como comodín para buscar coincidencias con el texto proporcionado
        cursor.execute(query,)
        results = cursor.fetchall()
        
        if results:
            return results
        else:
            print(f"No se encontraron registros de ventas para el mes y año especificado")
            return []
    except sqlite3.Error as e:
        print(f"Error al realizar la consulta: {e}")
        return []
    finally:
        cursor.close()
