import sqlite3

DATABASE_NAME = "ReportePagosBVLabs.db"

def search_products(products, search_term):
    """
    Filtra los productos que coinciden con el término de búsqueda.
    :param products: Lista de productos.
    :param search_term: Término de búsqueda.
    :return: Lista filtrada de productos.
    """
    return [product for product in products if search_term.lower() in product.lower()]
