import pandas as pd
from pathlib import Path
from datetime import datetime
class excelMgr:
    # Constructor de la clase (método especial)
    def __init__(self):
        self.currentExcel = None  # Archivo excel a abrir
        self.precios = None #variable que obtiene
        self.nombreArticulo =None
        self.ruta = None # nombre de la ruta al archivo

    # Método que permite crear el excel, será utilizado cada
    #15 dias para abrir dicho metodo(se hace una verificacion).
    #en las columnas de dicho excel
    def crearExcel(self):
        #aca se debe verificar si fechaExcel-fecha actual =15 o mayor , de ser asi
        #ejecuta el codigo de abajo
        #se crean las columnas del nuevo excel.
        ruta_por_defecto = 'C:\\Users\\Luis\\Desktop\\BreteLaboral' #ruta en donde guardar el excel
        nuevo_excel = pd.DataFrame(columns=['NAME', 'PRICE', 'QUANTITY','FechaExcel'])
        # Obtener la fecha actual como un objeto datetime
        fecha_actual = datetime.now()

        # Convertir la fecha actual a string en el formato dia, mes año
        fecha_actual_str = fecha_actual.strftime('%d-%m-%Y')
        # Ruta completa donde se guardará el archivo Excel
        ruta_completa = Path(ruta_por_defecto) / f'datos_{fecha_actual_str}.xlsx'#esta ruta cambiarla para cuando
        #el programa pase a etapa de deploy, asumiendo que en la computadora del trabajo
        #ya existe o definieron en que carpeta se va a guardar.
        nuevo_excel.to_excel(ruta_completa, index=False)
    def guardarExcel(self,ttemporal,nombreExcel,ruta):
        ruta_completa = Path(ruta) / f'datos_{nombreExcel}.xlsx'  # esta ruta cambiarla para cuando
        # el programa pase a etapa de deploy, asumiendo que en la computadora del trabajo
        # ya existe o definieron en que carpeta se va a guardar.
        ttemporal.to_excel(ruta_completa, index=False)


    # Otro método de instancia
    def leerExcel(self, ruta): #excel de guardado
        # Replace with your actual file path
        self.currentExcel = pd.read_excel(ruta)#setea el excel actual al excel
        self.ruta = ruta
        #seleccionado con la ruta, esto debe cambiar couando se incorpore la GUI.

    def añadirCarrito(self,nomArt, ttemporal,ruta):# metodo que toma el excel de precios
        #crea una tabla temporal y guarda en el archivo seleccionado
        # basicamente lo que debe de hacer es leer el excel de la lista de precios
        # añade en una tabla temporal los productos comprados
        # si el produjcto ya esta en esa tabla temporal , entonces le incrementa en 1 la cantidad
        # si el producto no existe en dicha tabla temporal(carrito de compras) lo añade
        if not ttemporal.loc[ttemporal['NAME'] == nomArt].empty:#sees if the product exists
            times = ttemporal.loc[ttemporal['NAME'] == nomArt, 'QUANTITY'].iloc[0]
            ttemporal.loc[ttemporal['NAME'] == nomArt, 'QUANTITY'] = times + 1 #if the product exists sums one to the quantity
            print("incremento")
        else:
            # Replace with your actual file path
            df = pd.read_excel(ruta)
            new_df = df.loc[df['NAME'] == nomArt].copy()#else the product gets registered as a new product
            new_df['QUANTITY'] = 1
            ttemporal = pd.concat([ttemporal, new_df])
            print("añado")
        return ttemporal

        #basicamente lo que debe de hacer es leer el excel de la lista de precios
        #añade en una tabla temporal los productos comprados
        #si el produjcto ya esta en esa tabla temporal , entonces le incrementa en 1 la cantidad
        #si el producto no existe en dicha tabla temporal(carrito de compras) lo añade







