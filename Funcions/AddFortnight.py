import sqlite3
from datetime import datetime

def add_sales_per_fortnight(connection):
    """
    Genera un registro en la tabla SalesperFortnight basado en el mes y el año actuales.
    Inicialmente se genera la primera quincena. Si ya existe, genera la siguiente quincena,
    hasta un máximo de cuatro registros por mes.

    Parameters:
        connection: sqlite3.Connection - Conexión activa a la base de datos.

    Returns:
        bool - True si el registro fue creado exitosamente, False en caso de error o si ya existen cuatro quincenas.
    """
    try:
        # Obtener el mes y el año actuales
        now = datetime.now()
        month = now.month
        year = now.year

        cursor = connection.cursor()

        # Verificar cuántas quincenas existen para el mes y el año actuales
        cursor.execute('''
            SELECT COUNT(*) FROM SalesperFortnight WHERE month = ? AND year = ?
        ''', (month, year))
        count = cursor.fetchone()[0]

        if count >= 4:
            print(f"Ya existen las 4 quincenas para {month:02d}/{year}.")
            return False

        # Determinar el nombre de la siguiente quincena a crear
        quincena_names = [
            f"Primera Quincena {month:02d}/{year}",
            f"Segunda Quincena {month:02d}/{year}",
            f"Tercera Quincena {month:02d}/{year}",
            f"Cuarta Quincena {month:02d}/{year}"
        ]

        quincena_name = quincena_names[count]  # Seleccionar la quincena correspondiente

        # Insertar la siguiente quincena en la tabla SalesperFortnight
        cursor.execute('''
            INSERT INTO SalesperFortnight (month, year, fortnight_name)
            VALUES (?, ?, ?)
        ''', (month, year, quincena_name))

        connection.commit()
        print(f"Registro de '{quincena_name}' creado exitosamente.")
        return True

    except sqlite3.Error as e:
        print(f"Error al agregar registro de quincena: {e}")
        connection.rollback()
        return False

# Ejemplo de uso
if __name__ == "__main__":
    connection = sqlite3.connect("ReportePagosBVLabs.db")

    if add_sales_per_fortnight(connection):
        print("Quincena agregada correctamente.")
    else:
        print("Hubo un problema al agregar la quincena o ya están todas creadas.")

    connection.close()
