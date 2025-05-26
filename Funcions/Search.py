import sqlite3

DATABASE_NAME = "ReportePagosBVLabs.db"

def search_products(products, search_term, selected_companies):
    """
    Filtra los productos que coinciden con el término de búsqueda y las empresas seleccionadas.
    
    :param products: Lista de tuplas (producto, empresa).
    :param search_term: Término de búsqueda.
    :param selected_companies: Lista de empresas seleccionadas.
    :return: Lista filtrada de productos.
    """
    return [
        product for product, supplier in products
        if search_term.lower() in product.lower() and supplier in selected_companies
    ]
