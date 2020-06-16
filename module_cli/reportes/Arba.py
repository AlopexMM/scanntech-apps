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

from os import path

import pandas as pd

# Funciones genericas
def grabar(datos,nombre):
        with open(nombre,"w",encoding="latin-1") as file:
                file.writelines(datos)
        return
    
def valores_genericos(rango, valor):
    # Rango es el tamaño de la lista y valor es el dato que va a contener
    lista = []
    for x in range(rango):
        lista.append(valor)
    return lista

def arreglo_fecha(fechas):
    lista = []
    for x in fechas:
        lista.append(x.strftime("%d/%m/%Y"))
    return lista

def pasar_string(datos,fill=None,decimal=None):
    lista = []
    if decimal:
        for x in datos:
            x = format(x,".2f")
            lista.append(str(x).zfill(fill))
    elif decimal == False:
        for x in datos:
            x = str(x).split(".")
            lista.append(x[0].zfill(fill))
    else:
        for x in range(len(datos)):
            d = str(datos[x])
            lista.append(d.zfill(fill))
    return lista

def cuitMod(cuits):
    
    lista = []
    for cuit in cuits:
        cabeza = cuit[0:2]
        cuerpo = cuit[2:10]
        cola = cuit[10:]
        lista.append(str(cabeza + "-" + cuerpo + "-" + cola))
    return lista

class Arba:

    def __init__(self,excel_archivo, padron_archivo):
        self.directorio_=path.dirname(excel_archivo)
        self.excel_file = excel_archivo
        self.padron_ = padron_archivo
        return

    def correr_reporte(self):

        # Cargamos el excel de los tickets
        tipos_datos = {"Nro.Documento":str}
        excel = pd.read_excel(self.excel_file, header=2, skipfooter=7,convert_float=False,dtype=tipos_datos)

        # Quitamos las columnas que no usamos en esta etapa
        columnas_quitar = ["Fecha Operación","Cliente","Cajero","Importe Retención","Documento"]
        excel.drop(columnas_quitar,axis="columns",inplace=True)

        # Completamos las celdas vacias del tipo de factura
        excel["Tipo de Factura"].fillna("A", inplace=True)

        # Obtenemos la posicion en la que va la columna total sin iva
        prefix_total_siva = excel.columns.get_loc("Nro.Documento")

        # Insertamos la columna total sin iva
        excel.insert(loc=prefix_total_siva,column="TotalSinIva", value=excel["Total"] - excel["IVA"])

        # Quitamos las columnas total e iva ya que no las vamos a necesitar mas
        columnas_quitar = ["Total","IVA"]
        excel.drop(columnas_quitar,axis="columns",inplace=True)

        # Procesamos el archivo de de ARBA y creamos un data frame
        padron_arba_df = pd.read_csv(self.padron_,sep=";",header=None,names=["NumeroCuit","AlicuotaPercepcion"],usecols=[4,8],decimal=",")

        padron_arba = padron_arba_df.set_index("NumeroCuit")

        # Insertamos la columna alicuota que contenga los porcentajes del padron que encuentre
        # Recorremos el listado de cuit del excel y genero una columna para insertar al dataframe
        prefix_alicuota = excel.columns.get_loc("Nro.Documento")

        valores_alicuota = []

        for documento in excel["Nro.Documento"]:
            valores_alicuota.append(float(padron_arba.AlicuotaPercepcion.get(int(documento),default=0.00)))



        excel.insert(loc=prefix_alicuota,column="alicuota",value=valores_alicuota)


        # Creamos una columna con el calculo del monto percibido
        prefix_monto_percibido = excel.columns.get_loc("Nro.Documento")

        # Insertamos la columna
        excel.insert(loc=prefix_monto_percibido,column="montoPercibido",value=(excel.TotalSinIva * excel.alicuota / 100))

        # Creamos un data frame que contenga solo las alicuotas que se pueden presentar
        #excel_reporte = excel[excel.alicuota > 0.0]
        print(excel.dtypes)
        excel_reporte = excel[excel.montoPercibido != 0.0]

        # Esto lo hago para corregir el nro del index, ya que el filtro anterior me quito algunas lineas
        excel_reporte.reset_index(inplace=True)

        datos_reportes = {
            "cuit": cuitMod(excel_reporte["Nro.Documento"]),
            "fechaPercepcion": arreglo_fecha(fechas=excel_reporte["Fecha"]),
            "tipoComprobante": valores_genericos(excel_reporte["Nro.Documento"].count(),"F"),
            "letraComprobante": excel_reporte["Tipo de Factura"],
            "numeroSucursal": pasar_string(excel_reporte["Registradora"],fill=4,decimal=False),
            "numeroEmision": pasar_string(excel_reporte["Nro.Operación"],fill=8,decimal=False),
            "montoImponible": pasar_string(excel_reporte["TotalSinIva"],fill=12,decimal=True),
            "importePercepcion": pasar_string(excel_reporte["montoPercibido"],fill=11,decimal=True),
            "tipoOperacion": valores_genericos(excel_reporte["Nro.Documento"].count(),"a")
        }

        reporte = pd.DataFrame(data=datos_reportes)
        reporte_arba = []

        #print(reporte.head(10))

        for x in range(reporte["cuit"].count()):
            y = (reporte["cuit"][x] +
                reporte["fechaPercepcion"][x] +
                reporte["tipoComprobante"][x] +
                reporte["letraComprobante"][x] +
                reporte["numeroSucursal"][x] +
                reporte["numeroEmision"][x] +
                reporte["montoImponible"][x] +
                reporte["importePercepcion"][x] +
                reporte["tipoOperacion"][x])
            reporte_arba.append( y + "\r\n")

        grabar(reporte_arba, path.join(self.directorio_, "arba.txt"))
        return
