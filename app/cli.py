#!/usr/bin/env python3
#! -*- encoding=latin-1 -*-

import argparse
import os
import sys

from reportes import Venta, Compra, Verificaciones, Arba, Ater
from collections import namedtuple
from zipfile import ZipFile, is_zipfile

# Funciones

def grabar_zip(archivos_, dir_):
    zip_ = os.path.join(dir_,"reporte.zip")
    os.chdir(dir_)
    with ZipFile(zip_, mode='w') as zp:
        for archivo in archivos_:
            zp.write(os.path.basename(archivo))
    return

def record_copy(lista, archivo_txt):
        p = archivo_txt.split(".")
        lista_grabar = lista
        with open(p[0] + '_PROCESADO.txt', mode='w', encoding='latin-1', newline='\r\n') as f:
            for line in lista_grabar:
                f.write(line + '\n')
        return (p[0] + '_PROCESADO.txt')


def zip_exctract(zip_, dir_, archivos_=None):
    if archivos_ == None: # Para reporte ARBA y ATER
        try:
            if is_zipfile(zip_):
                with ZipFile(zip_, mode="r") as zf:
                    arch = zf.namelist()
                    arch1 = arch[0]
                    arch1 = arch1.replace(" ", "+")
                    zf.extract(arch[0], dir_)
            else:
                sys.exit("No existe el archivo zip {}".format(zip_))
        except ValueError:
            print("No hay archivos dentro del zip")
        except UnboundLocalError:
            print("El nombre del archivo es incorrecto")

        excel_1 = os.path.join(dir_, arch[0])
        excel_2 = os.path.join(dir_, arch1)
        os.rename(excel_1, excel_2)
        return excel_2
    
    else:
        try:
            if is_zipfile(zip_):
                with ZipFile(zip_) as zp:
                    for archivo in archivos_: zp.extract(archivo,dir_)
            else:
                sys.exit("No existe el archivo zip {}".format(zip_))
        except ValueError:
            print("No se encuentran los archivos de ventas dentro del zip")

def archivo_path(parametro):
    path_ = parametro.split("=")
    return path_[1]

def remover_archivos(files_):
    for file_ in files_:
        os.remove(file_)

# Programa

# Preparamos el entorno

archivos = namedtuple(
    'archivos', ['venta_cbte', 'venta_alicuota', 'compra_cbte', 'compra_alicuota'])
reporte = archivos('REGINFO_CV_VENTAS_CBTE.txt',
                   'REGINFO_CV_VENTAS_ALICUOTAS.txt',
                   'REGINFO_CV_COMPRAS_CBTE.txt',
                   'REGINFO_CV_COMPRAS_ALICUOTAS.txt')

##########################
# TODO Probar todos los casos ejecutando de desde consola

# Funciones que llama el parser
def citi_ventas(args):
    exp = archivo_path(args.exportacion)
    directorio_ejecucion = os.path.dirname(os.path.abspath(exp))
    
    zip_exctract(archivos_=(reporte.venta_cbte,reporte.venta_alicuota),zip_=exp,dir_=directorio_ejecucion)
    
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
    archivos_.append(
        os.path.join(
            directorio_ejecucion,
            record_copy(archivo_txt=os.path.join(directorio_ejecucion, reporte.venta_cbte), lista=lista_cbte)))
    archivos_.append(
        os.path.join(
            directorio_ejecucion, record_copy(archivo_txt=os.path.join(directorio_ejecucion, reporte.venta_alicuota), lista=lista_alicuotas)))
    
    grabar_zip(archivos_, directorio_ejecucion)
    
    # Se suman estos dos archivos para eliminar
    archivos_.append(os.path.join(directorio_ejecucion, reporte.venta_cbte))
    archivos_.append(os.path.join(
        directorio_ejecucion, reporte.venta_alicuota))

    remover_archivos(archivos_)

def citi_compras(args):
    exp = archivo_path(args.exportacion)
    directorio_ejecucion = os.path.dirname(os.path.abspath(exp))
    
    zip_exctract(archivos_=(reporte.compra_cbte, reporte.compra_alicuota),
                     zip_=exp, dir_=directorio_ejecucion)
    
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
    archivos_.append(
        os.path.join(
            directorio_ejecucion,
            record_copy(archivo_txt=os.path.join(directorio_ejecucion, reporte.compra_cbte), lista=lista_cbte)))
    archivos_.append(
        os.path.join(
            directorio_ejecucion,record_copy(archivo_txt=os.path.join(directorio_ejecucion, reporte.compra_alicuota), lista=lista_alicuota)))

    grabar_zip(archivos_,directorio_ejecucion)

    # Se suman estos dos archivos para eliminar
    archivos_.append(os.path.join(directorio_ejecucion, reporte.compra_cbte))
    archivos_.append(os.path.join(
        directorio_ejecucion, reporte.compra_alicuota))
    
    remover_archivos(archivos_)

def arba(args):
    excel_ = archivo_path(args.excel)
    directorio_ejecucion = os.path.dirname(os.path.abspath(excel_))
    padron_ = archivo_path(args.padron)
    
    excel = zip_exctract(zip_=excel_,dir_=directorio_ejecucion)
    
    arba = Arba.Arba(excel_archivo=excel, padron_archivo=padron_)
    
    arba.correr_reporte()
    
    os.remove(excel)

def ater(args):
    excel = archivo_path(args.excel)
    ater = Ater.Ater(excel_archivo=excel)
    ater.correr_reporte()
    os.remove(excel)

# Creamos el parser de los argumentos
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(help="""Debajo de cada nombre se encuentra las distintas funciones de cada comando""")

# CITI Ventas
citi_v = subparser.add_parser(
    'citi-ventas', help='Procesa los reportes del citi compras')
citi_v.add_argument('exportacion', type=str, help="Archivo zip")
citi_v.set_defaults(func=citi_ventas)

# CITI Compras
citi_c = subparser.add_parser(
    'citi-compras', help='Procesa los reportes del citi compras'
)
citi_c.add_argument('exportacion',type=str,help='Archivo zip')
citi_c.set_defaults(func=citi_compras)

# ARBA
arba_ = subparser.add_parser(
    'arba',help='''Procesa el reporte de ARBA a partir del padron y el reporte tickets factura de clientes y percepcion''')
arba_.add_argument('excel',type=str, help='Tickets factura de clientes y percepciones')
arba_.add_argument('padron',type=str,help='Padron de ARBA')
arba_.set_defaults(func=arba)

# ATER
ater_ = subparser.add_parser(
    'ater', help='''Procesa el reporte de ATER a partir del reporte tickets factura de clientes y percepciones''')
ater_.add_argument('excel', type=str,
                   help='tickets factura de clientes y percepciones')
ater_.set_defaults(func=ater)

args = parser.parse_args()
args.func(args)
