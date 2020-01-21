# # Datos
# 
# La exportacion debe contener los siguientes datos
# 
# | IDCampo | Concepto | Tipo | Longitud | Separador ||
# |---------|----------|------|----------|-----------|---|
# |1| Tipo de Agente | Numérico | 1 | NO ||
# |2 | Motivo Movimiento | Numérico | 3 |NO||
# |3 | CUIT del cliente/ proveedor | CUIT |11 |NO||
# |4 | Fecha Percepcion | Fecha |10 |SI |/|
# |5 | Tipo de Comprobante | Texto |6 |NO||
# |6 | Letra Comprobante | Texto |1| NO||
# |7 | Numero Comprobante | Texto |12 |NO||
# |8 | Importe Base | Numérico |15 | SI |.|
# |9 | Alicuota | Numérico | 6 |SI |.|
# |10| Importe Percibido | Numérico | 15 | SI| . | 
# |11| Anulación | Numérico | 1 | NO||
# |12| Contribuyente Conv. Multilat. | Numérico | 1 | NO||
# 
# **Alicuota: 3%**
# 
# **Tipo de Archivo: .txt**
# 
# **Ejemplo de una línea del archivo de importación:**
# 
# 11942011111111201/06/2019F A123476789012000000000100.12002.00000000000010.0001
# 
# 1612095500069302/12/2019     FA000100006265000000000637,18003,00000000000019,1200
# 
# 

import os
import pandas as pd

from time import strftime

def valores_genericos(rango, valor):
    lista = []
    for x in range(rango):
        lista.append(valor)
    return lista

def monto_alicuota(monto,alicuota):
    return [x * alicuota / 100 for x in monto]

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
            lista.append(str(x).replace(".",",").zfill(fill))
    elif decimal == False:
        for x in datos:
            x = str(x).split(".")
            lista.append(x[0].zfill(fill))
    else:
        for x in range(len(datos)):
            lista.append(str(datos[x]))
    return lista

def escribir_reporte(datos, dir_):
    with open(os.path.join(dir_,"ater.txt"),"w",encoding="latin-1") as file:
        file.writelines(datos)
    return
    

class Ater:

    def __init__(self, excel_archivo):
        self.excel_file = excel_archivo
        self.directorio_trabajo = os.path.dirname(excel_archivo)    

    def correr_reporte(self):
    
        excel = pd.read_excel(self.excel_file, header=2 , skipfooter=15, convert_float=False)
        cant_rows = excel["Fecha"].count()

        # Calculamos los datos necesarios para la formación del dataframe final de la exportación
        # primer valor 016
        # Linea de ejemplo:
        # 1612095500069302/12/2019     FA000100006265000000000637,18003,00000000000019,1200

        tipo_agente = valores_genericos(cant_rows,"016")
        tipo_comprobante = valores_genericos(cant_rows,"     F")
        importe_base = excel["Total"]-excel["IVA"]
        alicuota = valores_genericos(cant_rows,"003,00")
        importe_percibido = monto_alicuota((excel["Total"]-excel["IVA"]), 3)
        contribuyente_conv_multilat = valores_genericos(cant_rows,"00")


        d = {"tipo_agente":tipo_agente,
             "cuit":pasar_string(excel["Nro.Documento"]),
             "fecha_percepcion":arreglo_fecha(excel["Fecha"]),
             "tipo_comprobante":tipo_comprobante,
             "letra_comprobante":excel["Tipo de Factura"],
             "punto_de_venta":pasar_string(excel["Registradora"],fill=4,decimal=False),
             "numero_comprobante":pasar_string(excel["Nro.Operación"],fill=8,decimal=False),
             "importe_base":pasar_string(importe_base,fill=15,decimal=True),
             "alicuota":alicuota,
             "importe_percibido":pasar_string(importe_percibido,fill=15,decimal=True),
             "contibuyente_conv_multi":contribuyente_conv_multilat}

        df = pd.DataFrame(data=d)
        df["letra_comprobante"].fillna("A",inplace=True)
        #df.to_csv("prueba.csv",index=False)


        reporte_ater = []
        for x in range(cant_rows):
            if df["cuit"][x] != "0" and df["cuit"][x] != "11111111113":
                y = (df["tipo_agente"][x]+
                    df["cuit"][x]+
                    df["fecha_percepcion"][x]+
                    df["tipo_comprobante"][x]+
                    df["letra_comprobante"][x]+
                    df["punto_de_venta"][x]+
                    df["numero_comprobante"][x]+
                    df["importe_base"][x]+
                    df["alicuota"][x]+
                    df["importe_percibido"][x]+
                    df["contibuyente_conv_multi"][x])
            reporte_ater.append(y+"\r\n")


        escribir_reporte(reporte_ater,self.directorio_trabajo)
