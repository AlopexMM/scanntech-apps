#!/usr/bin/env python
# coding: utf-8

# # ARBA
# 
# ## Formato del reporte
# 
# |Descripción| Formato| Long.| Dec.| Desde| Hasta| Observación|
# |:----------|:-------|:-----|:----|:-----|:-----|:-----------|
# |Cuit contribuyente Percibido| Alfanumérico| 13| |1| 13| Formato 99-99999999-9|
# |Fecha Percepción| Fecha| 10|| 14| 23| Formato dd/mm/aaaa. Debe corresponder al periodo declarado.|
# |Tipo de Comprobante| Texto| 1|| 24| 24| Valores F=Factura, R=Recibo , C=Nota Crédito, D =Nota Debito.|
# |Letra Comprobante| Texto| 1|| 25| 25| Valores A,B,C, o “ ” (blanco)|
# |Numero Sucursal| Numérico| 4|| 26| 29| Mayor a cero. Completar con ceros a la izquierda.|
# |Numero Emisión| Numérico| 8|| 30| 37| Mayor a cero. Completar con ceros a la izquierda.|
# |Monto imponible| Numérico| 12| 2| 38| 49| Con separador decimal (, o.). Mayor a cero, o Excepto para Nota de crédito, donde el importe debe ser negativo y la base debe ser menor o igual a cero. Completar con ceros a la izquierda. En las notas de crédito el signo negativo ocupará la primera posición a la izquierda. |
# |Importe de Percepción| Numérico| 11| 2| 50| 60| Con separador decimal (, o.). Mayor a cero, excepto para notas de crédito donde debe ser negativo. Completar con ceros a la izquierda. En las notas de crédito el signo negativo ocupará la primera posición a la izquierda.|
# |Tipo Operación| Texto| 1|| 61| 61| A= Alta, B=Baja, M=Modificación.|
# 
# 
# Linea ejemplo: 30-71531396-718/10/2019FA001000009762000000914.2400000036.56a

# In[120]:


from os import path
from re import compile

import pandas as pd
from clases import generico


# In[121]:


# Funciones genericas
arba = generico.ArbaAter

def cuitMod(cuits):
    lista = []
    for cuit in cuits:
        cabeza = cuit[0:2]
        cuerpo = cuit[2:10]
        cola = cuit[10:]
        lista.append(cabeza + "-" + cuerpo + "-" + cola)
    return lista


# In[122]:


excel_archivo = "/home/mario/scanntech-apps/docs/tickets.xlsx"
padron = "/home/mario/scanntech-apps/docs/PadronRGSPer112019.txt" # Archivo de arba, esto tiene que ser dinamico en el futuro


# In[123]:


# Cargamos el excel de los tickets
tipos_datos = {"Registradora":int,
              "Nro.Operación":int,
               "Nro.Documento":str}
excel = pd.read_excel(excel_archivo, header=2, skipfooter=15,convert_float=False,dtype=tipos_datos)


# In[124]:


# Quitamos las columnas que no usamos en esta etapa
columnas_quitar = ["Fecha Operación","Cliente","Cajero","Importe Retención","Documento"]
excel.drop(columnas_quitar,axis="columns",inplace=True)


# In[125]:


# Completamos las celdas vacias del tipo de factura
excel["Tipo de Factura"].fillna("A", inplace=True)


# In[126]:


# Obtenemos la posicion en la que va la columna total sin iva
prefix_total_siva = excel.columns.get_loc("Nro.Documento")

# Insertamos la columna total sin iva
excel.insert(loc=prefix_total_siva,column="TotalSinIva", value=excel["Total"] - excel["IVA"])

#Quitamos las columnas total e iva ya que no las vamos a necesitar mas
columnas_quitar = ["Total","IVA"]
excel.drop(columnas_quitar,axis="columns",inplace=True)


# In[127]:


# Procesamos el archivo de de ARBA y creamos un data frame

padron_arba_df = pd.read_csv(padron,sep=";",header=None,names=["NumeroCuit","AlicuotaPercepcion"],usecols=[4,8],decimal=",")


# In[128]:


padron_arba = padron_arba_df.set_index("NumeroCuit")


# In[129]:


# Insertamos la columna alicuota que contenga los porcentajes del padron que encuentre
# Recorremos el listado de cuit del excel y genero una columna para insertar al dataframe
prefix_alicuota = excel.columns.get_loc("Nro.Documento")

valores_alicuota = []

for documento in excel["Nro.Documento"]:
    valores_alicuota.append(padron_arba.AlicuotaPercepcion.get(int(documento),default=0.00))

excel.insert(loc=prefix_alicuota,column="alicuota",value=valores_alicuota)


# In[130]:


# Creamos una columna con el calculo del monto percibido
prefix_monto_percibido = excel.columns.get_loc("Nro.Documento")

# Insertamos la columna
excel.insert(loc=prefix_monto_percibido,column="montoPercibido",value=(excel.TotalSinIva * excel.alicuota / 100))


# In[131]:


# Creamos un data frame que contenga solo las alicuotas qeu se pueden presentar
excel_reporte = excel[excel.alicuota > 0.0]


# In[132]:


datos_reportes = {
    "cuit": cuitMod(excel_reporte["Nro.Documento"]),
    "fechaPercepcion": arba.arreglo_fecha(fechas=excel_reporte["Fecha"]),
    "tipoComprobante": arba.valores_genericos(excel_reporte["Documento"].count(),"F"),
    "letraComprobante": excel_reporte["Tipo de Factura"],
    "numeroSucursal": arba.pasar_string(excel_reporte["Registradora"],fill=4),
    "numeroEmision": arba.pasar_string(excel_reporte["Nro.Operación"],fill=8),
    "montoImponible": arba.pasar_string(excel_reporte["TotalSinIva"],fill=12,decimal=True),
    "importePercepcion": arba.pasar_string(excel_reporte["montoPercibido"],fill=11,decimal=True),
    "tipoOperacion": arba.valores_genericos(excel_reporte["Documento"].count(),"a")
}


print(datos_reportes)




