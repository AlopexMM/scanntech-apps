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
from pyfiglet import figlet_format
from subprocess import call as terminal_command

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
                se encuentra el reporte \"ater\"
                """
        print(msg)
    def _parser_line(self,line):
        return [line[45:60],line[65:81],line[25:27]]

    def results_of_report(self, report_file):
        try:
            totals = {
                'monto_base' : 0.0,
                'monto_percibido' : 0.0
            }
            with open(report_file,mode="r",encoding="latin-1") as f:
                for line in f.readlines():
                    values_of_line = self._parser_line(line)
                    if values_of_line[2] == "TF":
                        totals['monto_base'] += float(values_of_line[0])
                        totals['monto_percibido'] += float(values_of_line[1])
                    else:
                        totals['monto_base'] -= float(values_of_line[0])
                        totals['monto_percibido'] -= float(values_of_line[1])
            print(totals)
        except Exception as e:
            print(e)
            raise e
        return

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
                if self.cuit.verificador(str(row[8].value).replace(".","")):
                    cuit = str(row[8].value).replace(".","")
                    linea += cuit
                else:
                    continue
            except TypeError:
                print("Ocurrio un error con la cuit {} del nro de operacion {}.\nError ocurrido: Tipo de formato".format(row[8].value,row[4].value))
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
            if row[1].value == "FACTURA":
                tipo_comprobante = "TF    "
            elif row[1].value == "NOTA DE CREDITO":
                tipo_comprobante = "C     "
            linea += tipo_comprobante
            # Obtenemos la letra de la factura
            letra_comprobante = row[2].value
            linea += letra_comprobante
            # Obtenemos el punto de venta
            punto_venta = int(row[3].value)
            linea += str(punto_venta).zfill(4)
            # Numero de comprobante
            numero_comprobante = row[4].value
            linea += str(numero_comprobante).replace(".","").zfill(8)
            # Obtenemos el importe base
            total = row[5].value
            iva = row[6].value
            if total == 0.0:
                continue
            else:
                monto_base = float(total) - float(iva)
                linea += "{:.2f}".format(monto_base).zfill(15)
            # Agregamos la alicuota de la percepcion
            linea += self.alicuota
            # Obtenemos el importe percibido
            importe_percibido = row[7].value
            if importe_percibido == 0.0:
                continue
            else:
                linea += "{:.2f}".format(importe_percibido).zfill(15)
            # Agregamos el dato del convenio multilateral
            linea += self.contribuyente_conv_multi
            # Grabamos la linea en un archivo txt
            with open ("ater.txt", mode="a") as ofs:
                ofs.write(linea+"\r\n")
        terminal_command("clear")
        self.results_of_report("ater.txt")
        print(figlet_format("Archivo procesado"))
