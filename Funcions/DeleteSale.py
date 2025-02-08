import sqlite3

def delete_sale_by_product_and_fortnight_id(connection, product_name, fortnight_id):
    """
    Elimina una venta específica según el nombre del producto y el ID de la quincena.

    :param connection: Conexión a la base de datos SQLite.
    :param product_name: Nombre del producto cuya venta se eliminará.
    :param fortnight_id: ID de la quincena donde está registrada la venta.
    """
    try:
        cursor = connection.cursor()

        # Buscar el ID del producto según su nombre
        cursor.execute("SELECT id FROM Products WHERE name = ?", (product_name,))
        product = cursor.fetchone()
        if product is None:
            print(f"No se encontró un producto con el nombre '{product_name}'.")
            return False
        product_id = product[0]

        # Verificar si hay ventas de ese producto en la quincena dada
        cursor.execute("SELECT id FROM Sales WHERE product_id = ? AND fortnight_id = ?", (product_id, fortnight_id))
        sale = cursor.fetchone()
        if sale is None:
            print(f"No hay ventas registradas para el producto '{product_name}' en la quincena con ID {fortnight_id}.")
            return False

        # Eliminar la venta específica
        cursor.execute("DELETE FROM Sales WHERE product_id = ? AND fortnight_id = ?", (product_id, fortnight_id))
        connection.commit()
        print(f"La venta del producto '{product_name}' en la quincena con ID {fortnight_id} fue eliminada exitosamente.")
        return True

    except sqlite3.Error as e:
        connection.rollback()  # Revertir cambios en caso de error
        print(f"Error al eliminar la venta: {e}")
        return False

    finally:
        cursor.close()
