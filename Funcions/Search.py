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
