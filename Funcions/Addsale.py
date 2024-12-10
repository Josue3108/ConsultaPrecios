import sqlite3
""" funcion que inserta en la tabla sales"""
def Addsale(connection,prodName, quantity,quincena):
    try:
        cursor = connection.cursor()
        
        # Paso 1: Obtener el product_id usando el nombre del producto (prodName)
        cursor.execute('''SELECT id FROM Products WHERE name = ?''', (prodName,))
        product_row = cursor.fetchone()
        
        if product_row is None:
            print(f"Producto '{prodName}' no encontrado.")
            return
        
        product_id = product_row[0] # obtengo on [0] dado que el id es el primer elemento
        
        # Paso 2: Obtener el fortnight_id basado en la quincena
        cursor.execute('''SELECT id FROM SalesperFortnight WHERE fortnight_name = ?''', (quincena,))
        fortnight_row = cursor.fetchone()
        
        if fortnight_row is None:
            print(f"Quincena '{quincena}' no encontrada.")
            return
        
        fortnight_id = fortnight_row[0]
        
        # Paso 3: Insertar los datos en la tabla Sales
        cursor.execute('''
            INSERT INTO Sales (product_id, fortnight_id, quantity)
            VALUES (?, ?, ?)
        ''', (product_id, fortnight_id, quantity))
        
        connection.commit()
        print(f"Venta de {quantity} unidades del producto '{prodName}' registrada exitosamente.")
        
    except Exception as e:
        print("Error al agregar la venta:", e)
        connection.rollback()
    return []

     

