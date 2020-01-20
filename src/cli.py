#!/usr/bin/env python3
#! -*- encoding=latin-1 -*-

import argparse
import os

from citi import Venta, Compra, Verificaciones
from collections import namedtuple
from zipfile import ZipFile, is_zipfile

# Funciones

def grabar_zip(archivos_):
    with ZipFile("reporte.zip", mode='w') as zp:
        for archivo in archivos_:
            zp.write(archivo)
    return

def record_copy(lista, archivo_txt):
        p = archivo_txt.split(".")
        lista_grabar = lista
        with open(p[0] + '_PROCESADO.txt', mode='w', encoding='latin-1', newline='\r\n') as f:
            for line in lista_grabar:
                f.write('\n'.join(line))
        return

# Programa

# Preparamos el entorno
home = os.environ['HOME']
base_path = os.path.join(os.environ['HOME'],'reporteScanntech')
if os.path.isdir(base_path) == False:
    os.mkdir(base_path)

directorio_ejecucion = os.getcwd()

archivos = namedtuple(
    'archivos', ['venta_cbte', 'venta_alicuota', 'compra_cbte', 'compra_alicuota'])
reporte = archivos('REGINFO_CV_VENTAS_CBTE.txt',
                   'REGINFO_CV_VENTAS_ALICUOTAS.txt',
                   'REGINFO_CV_COMPRAS_CBTE.txt',
                   'REGINFO_CV_COMPRAS_ALICUOTAS.txt')

##########################

# Funciones que llama el parser
def citi_ventas(args):
    exportacion = args.exportacion.split('=')
    exp = os.path.abspath(exportacion[1])
    try:
        if is_zipfile(exp):
            with ZipFile(exp) as zp:
                zp.extract(reporte.venta_cbte)
                zp.extract(reporte.venta_alicuota)
        else:
            "El archivo no es un zip"
    except ValueError:
        print("No se encuentran los archivos de ventas dentro del zip")
    
    cbte = Venta.comprobante()
    alicuota = Venta.alicuota()
    
    lista_cbte = cbte.procesamiento_comprobantes(
        os.path.join(directorio_ejecucion, reporte.venta_cbte))
    lista_alicuotas = alicuota.procesamiento_alicuotas(
        os.path.join(directorio_ejecucion, reporte.venta_alicuota))
    check_ok = Verificaciones.verificaciones()
    lista_cbte = check_ok.verificar_nro_alicuotas(
        lista_cbte, lista_alicuotas)
    lista_cbte = check_ok.verificar_monto_final(
        lista_cbte, lista_alicuotas)
    lista_cbte, lista_alicuotas = check_ok.verificar_comprobantes_cero(
        lista_cbte, lista_alicuotas)
    
    # Grabar el reporte dentro de un zip
    archivos_ = []
    archivos_.append(record_copy(archivo_txt=os.path.join(directorio_ejecucion, reporte.venta_cbte), lista=lista_cbte))
    archivos_.append(record_copy(archivo_txt=os.path.join(directorio_ejecucion, reporte.venta_alicuota),lista=lista_alicuotas))
    grabar_zip(archivos_)

def citi_compras(args):
    exportacion = args.exportacion.split('=')
    exp = os.path.abspath(exportacion[1])
    try:
        if is_zipfile(exp):
            with ZipFile(exp) as zp:
                zp.extract(reporte.compra_cbte)
                zp.extract(reporte.compra_alicuota)
        else:
            "El archivo no es un zip"
    except ValueError:
        print("No se encuentran los archivos de ventas dentro del zip")
    
    cbte = Compra.Comprobante()
    alicuota = Compra.Alicuota()
    
    lista_cbte = cbte.procesar_comprobante(
        os.path.join(directorio_ejecucion, reporte.compra_cbte))
    
    lista_alicuota = alicuota.procesar_alicuota(
        os.path.join(directorio_ejecucion, reporte.compra_alicuota))
    
    comprobar = Compra.Verificacion()
    
    lista_cbte = comprobar.comprobacion(lista_cbte, lista_alicuota)
    
    # Grabar el reporte dentro de un zip
    archivos_ = []
    archivos_.append(record_copy(archivo_txt=os.path.join(
        directorio_ejecucion, reporte.venta_cbte), lista=lista_cbte))
    archivos_.append(record_copy(archivo_txt=os.path.join(
        directorio_ejecucion, reporte.venta_alicuota), lista=lista_alicuota))
    grabar_zip(archivos_)

def arba(args):
    pass

def ater(args):
    pass

# Creamos el parser de los argumentos
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(help="""Debajo de cada nombre se encuentra las distintas funciones de cada comando""")

# CITI Ventas
citi_v = subparser.add_parser(
    'citi-ventas', '-cv', help='Procesa los reportes del citi compras')
citi_v.add_argument('exportacion','-e', type=str, help="Archivo zip")
citi_v.set_defaults(func=citi_ventas)

# CITI Compras
citi_c = subparser.add_parser(
    'citi-compras', '-cc', help='Procesa los reportes del citi compras'
)
citi_c.add_argument('exportacion','-e',type=str,help='Archivo zip')
citi_c.set_defaults(func=citi_compras)

# ARBA
arba_ = subparser.add_parser(
    'arba',help='''Procesa el reporte de ARBA a partir del padron y el reporte tickets factura de clientes y percepcion''')
arba_.add_argument('excel',type=str, help='Tickets factura de clientes y percepciones')
arba_.add_argument('padron',type=str,help='Padron de ARBA')
arba_.set_defaults(arba)

# ATER
ater_ = subparser.add_parser(
    'ater', help='''Procesa el reporte de ATER a partir del reporte tickets factura de clientes y percepciones''')
ater_.add_argument('excel', type=str,
                   help='tickets factura de clientes y percepciones')
ater_.set_defaults(func=ater)
