import sqlite3

# Nombre de la base de datos
DATABASE_NAME = "ReportePagosBVLabs.db"

# Función para conectar a la base de datos
def connect_to_database():
    """Conecta a la base de datos SQLite. Si no existe, se crea automáticamente."""
    connection = sqlite3.connect(DATABASE_NAME)
    print(f"Conectado a la base de datos: {DATABASE_NAME}")
    return connection

# Función para crear la tabla Products
def create_table_products(connection):
    """Crea la tabla Products en la base de datos."""
    try:
        cursor = connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL
            );
        ''')
        connection.commit()
        print("Tabla 'Products' creada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'Products': {e}")
    finally:
        cursor.close()

# Función para crear la tabla SalesperFortnight
def create_table_salesperfortnight(connection):
    """Crea la tabla SalesperFortnight en la base de datos."""
    try:
        cursor = connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SalesperFortnight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL,
                year INTEGER NOT NULL,
                fortnight INTEGER NOT NULL CHECK(fortnight IN (1, 2))
            );
        ''')
        connection.commit()
        print("Tabla 'SalesperFortnight' creada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'SalesperFortnight': {e}")
    finally:
        cursor.close()

# Función para crear la tabla Sales
def create_table_sales(connection):
    """Crea la tabla Sales en la base de datos."""
    try:
        cursor = connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                fortnight_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES Products (id) ON DELETE CASCADE,
                FOREIGN KEY (fortnight_id) REFERENCES SalesperFortnight (id) ON DELETE CASCADE
            );
        ''')
        connection.commit()
        print("Tabla 'Sales' creada exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla 'Sales': {e}")
    finally:
        cursor.close()

# Función para consultar información sobre ventas para un ID de SalesperFortnight
def get_sales_by_fortnight_id(connection, fortnight_id):
    """Obtiene el nombre del producto, su precio, cantidad, mes, año y quincena para un ID de SalesperFortnight."""
    try:
        cursor = connection.cursor()
        
        query = '''
            SELECT 
                Products.name AS product_name,
                Products.price AS product_price,
                Sales.quantity AS product_quantity,
                SalesperFortnight.month AS sales_month,
                SalesperFortnight.year AS sales_year,
                SalesperFortnight.fortnight AS sales_fortnight
            FROM Sales
            INNER JOIN Products ON Sales.product_id = Products.id
            INNER JOIN SalesperFortnight ON Sales.fortnight_id = SalesperFortnight.id
            WHERE Sales.fortnight_id = ?;
        '''
        
        cursor.execute(query, (fortnight_id,))
        results = cursor.fetchall()
        
        if results:
            for row in results:
                print(f"Producto: {row[0]}, Precio: {row[1]}, Cantidad: {row[2]}, "
                      f"Mes: {row[3]}, Año: {row[4]}, Quincena: {row[5]}")
        else:
            print(f"No se encontraron ventas para la quincena con ID {fortnight_id}.")
    except sqlite3.Error as e:
        print(f"Error al realizar la consulta: {e}")
    finally:
        cursor.close()

# Función principal
if __name__ == "__main__":
    # Conectar a la base de datos
    conn = connect_to_database()
    
    # Crear las tablas
    create_table_products(conn)
    create_table_salesperfortnight(conn)
    create_table_sales(conn)
    
    # Ejecutar consulta de ejemplo (puedes cambiar el ID para probar)
    fortnight_id_to_query = 1  # Cambia este ID según los datos que tengas
    print(f"Consultando ventas para el ID de quincena {fortnight_id_to_query}:")
    get_sales_by_fortnight_id(conn, fortnight_id_to_query)
    
    # Cerrar la conexión
    conn.close()
    print("Conexión cerrada.")
