#!/usr/bin/python3
#! -*- encoding=utf-8 -*-

import io
import argparse
import os

from citi import Venta, Compra, Verificaciones
from collections import namedtuple   

# Funciones

def record_copy(path, lista):
        
        p = path.split('.txt')
        lista_grabar = lista
        with open(p[0] + '_PROCESADO.txt', mode='w', encoding='latin-1', newline='\r\n') as f:
            for line in lista_grabar:
                f.write(line + '\n')
        return

def get_path(path):
    if path == None:
        path = os.getcwd()
        return path
    return

# Programa

def main():
   
    parser = argparse.ArgumentParser()
    
    # ArgParser debe tomar la palabra clave citi, ater, arba para saber que funciones debe realizar y este le 
    # trasladara la información a otro script que ejecutara la funcion deseada
    # Hubo modificaciones ne el repositorio citiapp cambiar las librerias del citi
    
    parser.add_argument('-cv',
    help='Procesa los reportes del citi ventas',
    action='store_true')
    
    parser.add_argument('-cc', 
    help='Procesa los reportes del citi compras',
    action='store_true')
    
    parser.add_argument('--path',
    help='Dirección donde se encuentra el archivo a procesar',
    type=str)

    args = parser.parse_args()
    path = args.path
    if path == None:
        path = get_path(path)
    
    # Armamos una namedtuple para obtener de forma dinamica el nombre del reporte

    archivos = namedtuple('archivos', ['venta_cbte','venta_alicuota','compra_cbte','compra_alicuota'])
    reporte = archivos('REGINFO_CV_VENTAS_CBTE.txt',
        'REGINFO_CV_VENTAS_ALICUOTAS.txt',
        'REGINFO_CV_COMPRAS_CBTE.txt',
        'REGINFO_CV_COMPRAS_ALICUOTAS.txt')
    
    if args.cv:

        try:

            cbte = Venta.comprobante()
            alicuota = Venta.alicuota()
            lista_cbte = cbte.procesamiento_comprobantes(os.path.join(path, reporte.venta_cbte))
            lista_alicuotas = alicuota.procesamiento_alicuotas(os.path.join(path, reporte.venta_alicuota))
            check_ok = Verificaciones.verificaciones()
            lista_cbte = check_ok.verificar_nro_alicuotas(lista_cbte,lista_alicuotas)
            lista_cbte = check_ok.verificar_monto_final(lista_cbte, lista_alicuotas)
            record_copy(os.path.join(path,reporte.venta_cbte),lista_cbte)
            record_copy(os.path.join(path, reporte.venta_alicuota), lista_alicuotas)
        except FileNotFoundError:
            print('No se encuentran los archivos:\n{}\n{}'.format(reporte.venta_alicuota, reporte.venta_cbte))
        return 
    
    if args.cc:

        try:

            cbte = Compra.comprobante()
            alicuota = Compra.alicuota()
            lista_cbte = cbte.procesar_comprobante(os.path.join(path,reporte.compra_cbte))
            lista_alicuota = alicuota.procesar_alicuota(os.path.join(path,reporte.compra_alicuota))
            comprobar = Compra.verificacion()
            lista_cbte = comprobar.comprobacion(lista_cbte, lista_alicuota)
            record_copy(os.path.join(path,reporte.compra_cbte), lista_cbte)
            record_copy(os.path.join(path,reporte.compra_alicuota), lista_alicuota) 

        except FileNotFoundError:
            print('No se encuentran los archivos:\n{}\n{}'.format(reporte.compra_cbte, reporte.compra_alicuota))
        return  
# Init

if __name__ == '__main__':
    main()
