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
# |7 | Numero Comprobante | Texto |4 |NO||
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
import numpy as np

from time import strftime


def verificador_cuit(cuit):

    # Base para la multiplicacion
    if len(cuit) == 11:
        if cuit != "11111111113":
            base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
            aux = 0
            for i in range(10):
                aux += int(cuit[i]) * base[i]
            aux = 11 - (aux % 11)
            if aux == 11:
                aux = 0
            elif aux == 10:
                aux = 9
            if int(cuit[10]) == aux:
                return True
            else:
                return False
    else:
        return False

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
    
        excel = pd.read_excel(self.excel_file, header=2 , skipfooter=7, convert_float=False)


        # Insertamos una columna que contenga el importe base,tipo agente, tipo comprobante, alicuota, importe percibido y contibuyente convenio multilateral
        prefix_general = excel.columns.get_loc("Total")
        excel.insert(loc=prefix_general,column="montoBase",value=(excel["Total"]-excel["IVA"]))
        excel.insert(loc=prefix_general,column="tipoAgente",value="1")
        excel.insert(loc=prefix_general,column="tipoComprobante",value=np.nan)
        excel.insert(loc=prefix_general,column="alicuota",value="003.00")
        excel.insert(loc=prefix_general,column="importePercibido",value=(excel["montoBase"]*0.03))
        excel.insert(loc=prefix_general,column="convMultiLateral",value="00")
        excel.insert(loc=prefix_general,column="motivo",value="061")
        
        # Completamos las celdas vacias de tipo factura
        excel["Tipo de Factura"].fillna("A", inplace=True)

        # Si las facturas son positivas se cambia NaN por TF
        values = excel["tipoComprobante"][excel.montoBase > 0]
        values.fillna("TF    ",inplace=True)
        excel.tipoComprobante.fillna(value=values,inplace=True)
        
        # Si la factura son negativas se cambia NaN por C
        values = excel["tipoComprobante"][excel.montoBase < 0]
        values.fillna("C     ",inplace=True)
        excel.tipoComprobante.fillna(value=values,inplace=True)

        # Campos de las columnas que no sirven mas luego de procesar el archivo
        columnas_quitar = ["Fecha Operación", "Documento",
                           "Total", "IVA", "Cajero", "Cliente"]

        # Quitamos las columnas que no sirven
        excel.drop(columnas_quitar,axis="columns",inplace=True)
        
        # Nos quedamos con lineas validas para reportar
        excel_reporte = excel[excel.montoBase != 0]
        excel_reporte.reset_index(inplace=True)
        
        d = {"tipo_agente":excel_reporte.tipoAgente,
             "motivo":excel_reporte.motivo,
             "cuit":pasar_string(excel_reporte["Nro.Documento"]),
             "fecha_percepcion":arreglo_fecha(excel_reporte["Fecha"]),
             "tipo_comprobante":excel_reporte.tipoComprobante,
             "letra_comprobante":excel_reporte["Tipo de Factura"],
             "punto_de_venta":pasar_string(excel_reporte["Registradora"],fill=4,decimal=False),
             "numero_comprobante":pasar_string(excel_reporte["Nro.Operación"],fill=8,decimal=False),
             "importe_base":pasar_string(excel_reporte.montoBase,fill=15,decimal=True),
             "alicuota":excel_reporte.alicuota,
             "importe_percibido":pasar_string(excel_reporte.importePercibido,fill=15,decimal=True),
             "contibuyente_conv_multi":excel_reporte.convMultiLateral}

        df = pd.DataFrame(data=d)
        
        reporte_ater = []
        for x in range(df["cuit"].count()):
            cuit_valido = verificador_cuit(df["cuit"][x])
            if cuit_valido:
                y = (df["tipo_agente"][x]+
                    df["motivo"][x]+
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
