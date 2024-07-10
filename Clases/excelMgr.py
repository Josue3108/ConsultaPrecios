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

    # Otro método de instancia
    def leerExcel(self, ruta):
        # Replace with your actual file path
        self.currentExcel = pd.read_excel(ruta)#setea el excel actual al excel
        self.ruta = ruta
        #seleccionado con la ruta, esto debe cambiar couando se incorpore la GUI.

    def modifExcel(self,item, data):
        #falta corregir
        datos = pd.DataFrame(columns=['NAME', 'PRICE', 'QUANTITY'])
        # esto es el mismo método para leer el excel e incrementarle los valores
        prices = data
        # Check if the item exists in the DataFrame and if there are any null values in the subset
        if self.currentExcel.loc[self.currentExcel['NAME'] == item].isnull().any().any():
            new_df = self.currentExcel.loc[self.currentExcel['NAME'] == item].copy()  # Use .copy() to avoid SettingWithCopyWarning
            new_df['QUANTITY'] = 1
            return new_df #devuelve el dataframe,si encuentra valores
        #nulos entonces va a obtener unicamente los valores que no sean nulos
        else:
            #si el articulo existe, entonces incremente en 1 la cantidad
            if not prices.loc[prices['NAME'] == item].empty:
                times = prices.loc[prices['NAME'] == item, 'QUANTITY'].iloc[0]
                prices.loc[prices['NAME'] == item, 'QUANTITY'] = times + 1
            else:
                new_df = self.currentExcel.loc[self.currentExcel['NAME'] == item].copy()
                new_df['QUANTITY'] = 1
                prices = pd.concat([prices, new_df])
            ruta_por_defecto = 'C:\\Users\\Luis\\Desktop\\BreteLaboral'
            ruta_completa = Path(ruta_por_defecto) / f'datos_{self.ruta.split('\\')[-1]}.xlsx'
            new_df.to_excel(ruta_por_defecto, index=False) #esti es lo que guarda el excel
            print(f'Se han guardado los cambios en el archivo Excel: {ruta_por_defecto}')
    # Example usage

#idealmente esto debe de ser una lista de todos lo que se compró
# #por el momento guarda 1 unico dato para hacer las pruebas,posteriormente
#debe de utilizarse una lista para ir almacenando todos los articulos que se deseen guardar

