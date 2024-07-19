from Clases.excelMgr import excelMgr
import pandas as pd

excelmngr= excelMgr() #creo la instancia de excel manager

file_path = 'C:\\Users\\Luis\\Desktop\\BreteLaboral\\ConsultaPrecios\\PRECIOS_LAB_SJ1.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)
tabla_temporal = pd.DataFrame(columns=['NAME', 'PRICE', 'QUANTITY'])
#las 3 lineas anteriores lo que hacen es: decir la ruta al excel de precios
#leer el excel de precios
#crear la tabla temporal con las columnas  nombre, precio y quantity

#añadido de articulos a la tabla temporal
tabla_temporal=excelmngr.añadirCarrito('IgE ANTI ATUN',tabla_temporal,file_path)
tabla_temporal=excelmngr.añadirCarrito('IgE ANTI ATUN',tabla_temporal,file_path)
tabla_temporal=excelmngr.añadirCarrito('IgE ANTI BLOMIA TROPICALIS',tabla_temporal,file_path)
print(tabla_temporal)#imprime la tabla
excelmngr.guardarExcel(tabla_temporal,"chocobito",'C:\\Users\\Luis\\Desktop\\BreteLaboral')
#guarda el excel , con el nombre de los datos,preferiblemente la fecha de excel, y la ruta de donde guardarlo