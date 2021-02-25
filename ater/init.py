"""MIT License

Copyright (c) 2020 Mario Mori

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
"""
Procesa un reporte excel del modulo de reportes del sistema Scanntech y produce la exportación de ATER
"""

from openpyxl import load_workbook
from datetime import datetime, timedelta
from time import strftime
from afip.cuit import Cuit
from sys import exit

# Class

class Ater(object):
    
    def __init__(self, *args):
        self.argv = args[0]
        self.excel_date = datetime(year=1900,month=1, day=1)
        self.cuit = Cuit()
        self.tipo_agente = "1"
        self.motivo = "061"
        self.alicuota = "003.00"
        self.contribuyente_conv_multi = "00"
    
    def help_app(self):
        msg = """\
                Ater necesita un archivo excel de donde puede sacar los datos en el modulo de reportes
                se encuentra el reporte \"Tickets de clientes con factura y percepcion\"
                """
        print(msg)
    
    def run(self):
    
        # Carga de excel
        try:
            wb = load_workbook(self.argv[1])
        except IndexError:
            self.help_app()
            exit()
        
        sheet = wb['0 - Tickets de Clientes con Fac']
        rows = sheet.rows
        next(rows)
        next(rows)
        next(rows)
        for row in rows:
            linea = self.tipo_agente + self.motivo
            # Verificamos si la celda esta en blanco se cierra el for
            if row[0].value == None:
                break
            # Revisamos que el cuit este bien si no se continua con la siguiente linea
            try:
                if self.cuit.verificador(row[7].value):
                    cuit = row[7].value
                    linea += cuit
                else:
                    continue
            except TypeError:
                print("Ocurrio un error con la cuit {} del nro de operacion {}.\nError ocurrido: Tipo de formato".format(row[7].value,row[4].value))
            # Como obtener el valor de la fecha
            if row[0].value != "Fecha":
                try:
                    days = timedelta(days = (int(row[0].value) - 2))
                    fecha_percepcion = (self.excel_date + days).strftime("%d/%m/%Y")
                    linea += fecha_percepcion
                except TypeError:
                    dia = row[0].value
                    fecha_percepcion = dia.strftime("%d/%m/%Y")
                    linea += fecha_percepcion
            if row[3].value == "FACTURA":
                tipo_comprobante = "TF    "
            elif row[3].value == "NOTA DE CREDITO":
                tipo_comprobante = "C     "
            linea += tipo_comprobante
            # Obtenemos la letra de la factura
            letra_comprobante = row[5].value
            linea += letra_comprobante 
            # Obtenemos el punto de venta
            punto_venta = int(row[2].value)
            linea += str(punto_venta).zfill(4)
            # Numero de comprobante
            numero_comprobante = row[4].value
            linea += str(numero_comprobante).zfill(8)
            # Obtenemos el importe base
            total = row[10].value
            iva = row[11].value
            if total == 0.0:
                continue
            else:
                monto_base = total - iva
                linea += "{:.2f}".format(monto_base).zfill(15)
            # Agregamos la alicuota de la percepcion
            linea += self.alicuota
            # Obtenemos el importe percibido
            importe_percibido = row[9].value
            if importe_percibido == 0.0:
                continue
            else:
                linea += "{:.2f}".format(importe_percibido).zfill(15)
            # Agregamos el dato del convenio multilateral
            linea += self.contribuyente_conv_multi
            # Grabamos la linea en un archivo txt
            with open ("ater.txt", mode="a") as ofs:
                ofs.write(linea+"\r\n")
        print("Se termino de procesar el excel, por favor revise el archivo ater.txt")
    
