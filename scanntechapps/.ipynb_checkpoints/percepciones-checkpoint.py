import os
import pandas as pd
import re

# Funcion que busca la pocicion en el padron para obtener el valor de percepcion
def busquedaPadron(cuit):
	padron = re.compile(r'\bPadronRGSPer[0-9][0-9][0-9][0-9][0-9][0-9].txt\b')
	padron = busquedaArchivo(padron)
	#padron = os.path.abspath('padron.txt')
	with open(padron, "r") as file:
		for l in file:
			linea = l.split(";")
			if linea[4] == cuit:
				return str(linea[8])
	return '-1'

# Recorremos la carpera en busca de cada uno de los archivos

def busquedaArchivo(archivo):
	for dirName, subDirList, fileList in os.walk("./"):
		for fName in fileList:
			if re.match(archivo, fName) != None:
				return os.path.abspath(fName)
	return

# Carga del excel para verificar los tickets

ticketsClientesFacturaPercepcion = re.compile(
	r'''\bTickets de Clientes con Factura y PercepciÃ³n_[0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9]-[0-9][0-9]_[0-9][0-9]_[0-9][0-9].xlsx''')
ticketsClientesFacturaPercepcion = busquedaArchivo(ticketsClientesFacturaPercepcion)
dfColumnasExcel = [0]
dfTicketClientesFacturaPercepcion = pd.read_excel(ticketsClientesFacturaPercepcion, usecols=dfColumnasExcel)
dfTicketClientesFacturaPercepcion.drop_duplicates(subset='Nro.Documento', keep='first', inplace=True)

# Arrays para el padron

cuitPadron = []
percepcion = []

# Cargamos el padron y los recorremos

# Creamos un DataFrame con los datos obtenidos del padron

for x in dfTicketClientesFacturaPercepcion['Nro.Documento']:
	y = busquedaPadron(str(x))
	if y > '-1':
		cuitPadron.append(str(x))
		percepcion.append(y)

excel = {
	'cuit':cuitPadron,
	'percepcion': percepcion
}
dfExcel = pd.DataFrame(data=excel)
dfExcel.drop_duplicates(subset='cuit',keep='first',inplace=True)
dfExcel.to_excel('cuitConPercepcion.xlsx', index=False)
