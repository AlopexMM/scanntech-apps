# # Reporte Uy
# 
# Uruguay solicita un reporte en el cual solo se visualicen clientes de base 3 que se encuentren instalados para pasar a BE 3
# 
# Termina quedando un reporte del listado de clientes de base uno, dos y tres

import pandas as pd
from os import path

path = "/home/mario/Descargas/kreporter.csv"

csv = pd.read_csv(path,sep=",", encoding="latin-1",dtype={"Num. de cliente":str})


# Borramos las columnas que no se necesitan
csv.drop(["Apellidos",
     "Lider",
     "Nro Unico",
     "Nombre Fantasia",
    "Direccion",
    "Ciudad",
    "Integrador",
    "Estado / Provincia",
    "Zona",
    "Supermercado Oriental:",
    "Fecha Estimada para Comenzar la Instalacion",
    "Fecha de Finalizacion de la Instalacion",
    "RUT/CUIT/CNPJ",
    "Unnamed: 15"],axis="columns",inplace=True)


# Borramos todas las lineas que tengan una celda vacia
csv.dropna(inplace=True)


# Renombramos las columnas que nos quedan para trabajar mejor
columna_renombrada = {"Num. de cliente":"num_cliente",
                     "Status (de Operaciones)":"status"}
csv.rename(columns=columna_renombrada,inplace=True)


# Pasamos a int todos los valores de num_cliente antes de filtrar los datos
csv.insert(loc=0,
           column="numcliente",
           value=csv["num_cliente"].astype(int))


# Eliminamos la columna que esta de mas
csv.drop("num_cliente",axis="columns",inplace=True)

# Filtro para clientes de base 1
csv_base3 = csv[((csv.numcliente >= 10000) & (csv.numcliente <= 10499)) & ((csv.status == "Instalado") | (csv.status == "Corte_Admin_Caja"))]
csv_base3 = csv_base3["numcliente"].drop_duplicates(keep="first")

# Filtro para clientes de base 2
csv_base2 = csv[((csv.numcliente >= 10500) & (csv.numcliente <= 10999)) & ((csv.status == "Instalado") | (csv.status == "Corte_Admin_Caja"))]
csv_base2 = csv_base3["numcliente"].drop_duplicates(keep="first")

# Filtro para clientes de base tres
csv_base3 = csv[((csv.numcliente >= 11000) & (csv.numcliente <= 11999)) & ((csv.status == "Instalado") | (csv.status == "Corte_Admin_Caja"))]
csv_base3 = csv_base3["numcliente"].drop_duplicates(keep="first")

csv_base1.to_csv("/home/mario/Documentos/base1.csv", encoding="latin-1", index=False,mode="w", header="Cliente")

csv_base2.to_csv("/home/mario/Documentos/base2.csv", encoding="latin-1", index=False,mode="w", header="Cliente")

csv_base3.to_csv("/home/mario/Documentos/base3.csv", encoding="latin-1", index=False,mode="w", header="Cliente")
