import sqlite3
from datetime import datetime

def get_last_fortnight(connection):
    """
    Obtiene la última quincena creada dentro del mes y el año actuales.

    Parameters:
        connection: sqlite3.Connection - Conexión activa a la base de datos.

    Returns:
        dict - Información de la última quincena creada o None si no existe ninguna.
    """
    try:
        # Obtener el mes y el año actuales
        now = datetime.now()
        month = now.month
        year = now.year

        cursor = connection.cursor()

        # Obtener la última quincena creada para el mes y el año actuales
        cursor.execute('''
            SELECT id, month, year, fortnight_name
            FROM SalesperFortnight
            WHERE month = ? AND year = ?
            ORDER BY id DESC
            LIMIT 1
        ''', (month, year))

        row = cursor.fetchone()

        if row:
            return {
                "id": row[0],
                "month": row[1],
                "year": row[2],
                "fortnight_name": row[3]
            }
        else:
            print(f"No hay quincenas registradas para {month:02d}/{year}.")
            return None

    except sqlite3.Error as e:
        print(f"Error al obtener la última quincena: {e}")
        return None