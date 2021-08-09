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
Procesa un reporte excel del modulo de reportes del sistema Scanntech y produce la exportación de ARBA
"""

from openpyxl import load_workbook
from datetime import datetime, timedelta
from time import strftime
from afip.cuit import Cuit
from sys import exit
from subprocess import call as terminal_command
from pyfiglet import figlet_format

class Arba(object):

    def __init__(self, *args):
        self.argv = args[0]
        self.excel_date = datetime(year=1900,month=1,day=1)
        self.cuit = Cuit()
    
    def help_app(self):
        msg = """\
            Arba necesita un archivo excel de donde puede sacar los datos de las facturas
            y el padron que se le entrega a Uy, consultar a dgiovagnoli@scanntech.com o mmori@scanntech.com
            por estos archivos
            """
        print(msg)
    
    def __cuits_arba(self, file):
        with open(file, mode='r') as f:
           list_cuit = dict()
           for line in f.readlines():
               l = line.split(';')
               if l[10] == '1':
                   list_cuit[l[4]] = l[8]
        return list_cuit
    
    def run(self):
        try:
            wb = load_workbook(self.argv[1])
            padron = self.__cuits_arba(self.argv[2])
        except IndexError:
            self.help_app()
            exit()
        

        sheet = wb['0 - Tickets de Clientes con Fac']
        rows = sheet.rows
        next(rows)
        next(rows)
        next(rows)
        for row in rows:
            linea = ""
            # Verifico si se encuentra vacia la fecha, de ser None se termina el for
            if row[0].value == None:
                break
            try:
                # Verifico el cuit
                cuit = str(row[7].value)
                if self.cuit.verificador(str(row[7].value).replace('.','')):
                    cuit = str(row[7].value).replace('.','')
                    cuit = f'{cuit[0:2]}-{cuit[2:10]}-{cuit[10:]}'
                    linea += cuit
                else:
                    continue
            except TypeError:
                print("Ocurrio un error con la cuit {} del nro de operacion {}.\nError ocurrido: Tipo de formato".format(row[8].value, row[4].value))
            # Obtenemos la fecha
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
                tipo_comprobante = "F"
            elif row[3].value == "NOTA DE CREDITO":
                tipo_comprobante = "C"
            linea += tipo_comprobante
            # Obtenemos la letra de la factura
            letra_comprobante = str(row[5].value)
            linea += letra_comprobante
            # Obtenemos el punto de venta
            punto_venta = int(row[2].value)
            linea += str(punto_venta).zfill(4)
            # Numero de comprobante
            numero_comprobante = row[4].value
            linea += str(numero_comprobante).replace(".","").replace(",","").zfill(8)
            # Obtenemos el importe base
            total = row[10].value
            iva = row[11].value
            if total == 0.0:
                continue
            else:
                monto_base = float(total) - float(iva)
                linea += "{:.2f}".format(monto_base).zfill(12)
            # Obtenemos el importe percibido
            if row[7].value in padron.keys():
                if padron[str(row[7].value)] == '0.00':
                    continue
                else:
                    alicuota = padron[str(row[7].value)]
                    monto_percibido = monto_base * float(alicuota.replace(',','.')) / 100
                    linea += '{:.2f}'.format(monto_percibido).zfill(11)
            else:
                continue
            # Agregamos el dato de tipo de operacion
            linea += 'A'
            # Grabamos la linea en un archivo txt
            with open("arba.txt", mode="a") as ofs:
                ofs.write(linea+"\r\n")
        terminal_command("clear")
        print(figlet_format("Archivo procesado"))


if __name__ == '__main__':
    from sys import argv
    arba = Arba(argv)
    arba.run()
