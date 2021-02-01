from openpyxl import load_workbook
from datetime import datetime, timedelta
from time import strftime

# Funciones
def verificador_cuit(cuit):

    # Base para la multiplicacion
    if len(cuit) == 11:
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

# Variables
EXCEL_DATE = datetime(year=1900,month=1,day=1)
cont = 4
tipo_agente = "1"
motivo = "061"
cuit = ""
fecha_percepcion = ""
tipo_comprobante = ""
letra_comprobante = ""
punto_venta = ""
numero_comprobante = ""
importe_base = ""
alicuota = "003.00"
importe_percibido = ""
contribuyente_conv_multi = "00"

# Carga de excel
wb = load_workbook('tickets.xlsx')
sheet = wb['0 - Tickets de Clientes con Fac']
rows = sheet.rows
next(rows)
next(rows)
next(rows)
for row in rows:
    linea = tipo_agente + motivo
    # Verificamos si la celda esta en blanco se cierra el for
    if row[0].value == None:
        break
    # Revisamos que el cuit este bien si no se continua con la siguiente linea
    try:
        if int(row[7].value) != 11111111113:
            if verificador_cuit(row[7].value):
                cuit = row[7].value
                linea += cuit
            else:
                continue
        else:
            continue
    except TypeError:
        print("Ocurrio un error con la cuit {} del nro de operacion {}.\nError ocurrido: Tipo de formato".format(row[7].value,row[4].value))
    # Como obtener el valor de la fecha
    if row[0].value != "Fecha":
        days = timedelta(days = (int(row[0].value) - 2))
        fecha_percepcion = (EXCEL_DATE + days).strftime("%d/%m/%Y")
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
    linea += alicuota
    # Obtenemos el importe percibido
    importe_percibido = row[9].value
    if importe_percibido == 0.0:
        continue
    else:
        linea += "{:.2f}".format(importe_percibido).zfill(15)
    # Agregamos el dato del convenio multilateral
    linea += contribuyente_conv_multi
    # Grabamos la linea en un archivo txt
    with open ("ater.txt", mode="a") as ofs:
        ofs.write(linea+"\r\n")
print("Se termino de procesar el excel, por favor revise el archivo ater.txt")
