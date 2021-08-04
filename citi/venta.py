# -*- coding: latin-1 -*-

''' En esta clase se puede encontrar las funciones que modifican el archivo de 
comprobantes'''
# Funcion que devuelve un nro unico formado por valores que se encuentran
# en ambos reportes

import sqlite3
from typing import Generator


# def codigo_unico_cbte_alicuota(data):
#     codigo_unico = data['tipo de comprobante'] + \
#         data['punto de venta'] + \
#         data['numero de comprobante']
#     return codigo_unico

# class verificaciones:
#     def __init__(self):
#         self.comprobantes = comprobante()
#         self.alicuotas = alicuota()
#         return
    
#     def verificar_nro_alicuotas(self, cbte, alicuota):

#         resultado = []
        
        
#         for x in cbte:
            
#             # Contador de lineas de alicuotas que se encuentran en alicuotas
#             count_al = 0

#             # Obtenemos un diccionario de los campos
#             cbte_linea = self.comprobantes.campos_comprobante(x)

#             # Creamos un valor unico para contar las cantidad de alicuotas que hay
#             tmp_cbte = codigo_unico_cbte_alicuota(cbte_linea)

#             for y in alicuota:
                
#                 # Obtenemos un diccionario de los campos
#                 alicuota_linea = self.alicuotas.campos_alicuotas(y)

#                 # Creamos un valor unico para contar las cantidad de alicuotas que hay
#                 tmp_alicuota = codigo_unico_cbte_alicuota(alicuota_linea)

#                 # Verificamos con los valores unicos obtenidos,
#                 # de tener igualdad se suma uno al contador
#                 if tmp_cbte == tmp_alicuota:
#                     count_al = count_al + 1
                
#                 # Revisamos si hay IVA 0
#                 if alicuota_linea['alicuota de iva'] == '0003':
#                     cbte_linea['codigo de operacion'] = 'N'

#             # Terminamos de recorrer la lista y reemplazamos la cantidad de alicuotas por el monto de la cuenta
#             cbte_linea['cantidad de alicuotas de iva'] = str(count_al)
#             resultado.append(self.comprobantes.construir_linea_comprobante(cbte_linea))
#         return resultado


#     def verificar_monto_final(self, cbte, alicuota):
#         lista = []
        
#         # Revisamos cada linea de comprobantes
#         for x in cbte:

#             # Obtenemos el diccionario de los comprobantes para trabajarlo
#             cbte_linea = self.comprobantes.campos_comprobante(x)

#             # Armamos un codigo unico de operacion en comprobantes
#             x_operacion = codigo_unico_cbte_alicuota(cbte_linea)

#             # Declaramos la variable donde se van a acumular el IVA y el neto
#             # que encontremos en alicuotas y coincidan los codigos unicos
#             # de la linea de comprobante y la linea de alicuota
#             y_monto_x = 0

#             for y in alicuota:

#                 # Obtenemos el diccionario de las alicuotas para trabajarlo
#                 alicuota_linea = self.alicuotas.campos_alicuotas(y)

#                 # Armamos un codigo unico 
#                 y_operation = codigo_unico_cbte_alicuota(alicuota_linea)

#                 # Importes que se necesitan obtener
#                 y_monto_sin_impuesto = alicuota_linea['importe neto gravado']
#                 y_iva = alicuota_linea['impuesto liquidado']

#                 # Si los codigos unicos coinciden sumarizamos los montos del IVA y el neto
#                 if x_operacion == y_operation:
#                     y_monto_x = (y_monto_x + int(y_monto_sin_impuesto) + int(y_iva))

#             # Obtenemos el monto real en y_mas_x
#             y_mas_x = (
#                 y_monto_x +
#                 int(cbte_linea['importe total de conceptos que no integran el precio neto gravado']) +
#                 int(cbte_linea['percepcion a no categorizados']) +
#                 int(cbte_linea['importe de operaciones exentas']) +
#                 int(cbte_linea['importe de percepciones o pagos a cuenta de impuestos nacionales']) +
#                 int(cbte_linea['importe de percepciones de ingresos brutos']) +
#                 int(cbte_linea['importe de percepciones impuestos municipales']) +
#                 int(cbte_linea['importe impuestos internos'])
#                 )

#             # Modificamos el monto total de la operacion para que coincida con lo reportado
#             y_mas_x = str(y_mas_x).rjust(15, "0")
            
#             if cbte_linea['importe total de la operacion'] != y_mas_x:
#                 cbte_linea['importe total de la operacion'] = y_mas_x

#             # Se forma la linea final
#             lista.append(self.comprobantes.construir_linea_comprobante(cbte_linea))

#         return lista

#     def verificar_comprobantes_cero(self, cbte, alicuotas):

#         lista_cbte = []
#         alicuotas_a_quitar = []
#         self.lista_alicuotas = alicuotas

#         for x in cbte:

#             cbte_linea = self.comprobantes.campos_comprobante(x)

#             if int(cbte_linea['importe total de la operacion']) == 0:
#                 operacion = cbte_linea['tipo de comprobante'] + \
#                     cbte_linea['punto de venta'] + \
#                     cbte_linea['numero de comprobante']
#                 alicuotas_a_quitar.append(operacion)
#             else:
#                 lista_cbte.append(self.comprobantes.construir_linea_comprobante(cbte_linea))

#         for x in alicuotas:            
#             alicuota_linea = self.alicuotas.campos_alicuotas(x)

#             operacion_alicuota = alicuota_linea['tipo de comprobante'] + \
#                 alicuota_linea['punto de venta'] + \
#                 alicuota_linea['numero de comprobante']

#             for y in alicuotas_a_quitar:
#                 if operacion_alicuota == y:
#                     #print("{0} encontro este y se debe remover {1}".format(y,x))
#                     self.lista_alicuotas.remove(x)


#         return [lista_cbte, self.lista_alicuotas]
# # Verificadores

# def verificador_cuit(cuit):

#     # Cortamos la cadena de 20 caracteres para que me queden los ultimos 11
#     # y poder verificar el CUIT
    
#     cuit = cuit[9:20]
    
#     # Base para la multiplicacion
    
#     base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
#     aux = 0
#     for i in range(10):
#         aux += int(cuit[i]) * base[i]
#     aux = 11 - (aux % 11)
#     if aux == 11:
#         aux = 0
#     elif aux == 10:
#         aux = 9
#     if int(cuit[10]) == aux:
#         return True
#     else:
#         return False

# # Funciones propias de la clase
# # Funciones que pueden ser utilizadas por ambas clases
        
# def remplazo_tipo_operacion(data, comprobantes=False, alicuotas=False):
#     if comprobantes:

#         # Remplazo el tipo de comprobante en los datos

#         if (data.get('tipo de comprobante') == '006'):
#             data['tipo de comprobante']='082'
#         elif (data.get('tipo de comprobante') == '001'):
#             data['tipo de comprobante']= '081'
#         elif (data.get('tipo de comprobante') == '008'):
#             data['tipo de comprobante']='113'
#         elif (data.get('tipo de comprobante') == '003'):
#             data['tipo de comprobante']='112'
#         return data

#     elif alicuotas:
        
#         # Remplazo el tipo de comprobante en los datos incorrectos

#         if (data.get('tipo de comprobante') == '006'):
#             data['tipo de comprobante'] = '082'
#         elif (data.get('tipo de comprobante') == '001'):
#             data['tipo de comprobante'] = '081'
#         elif (data.get('tipo de comprobante') == '008'):
#             data['tipo de comprobante'] = '113'
#         elif (data.get('tipo de comprobante') == '003'):
#             data['tipo de comprobante'] = '112'
        
#         return data
#     else:
#         return data

# # Funciones que pertenecen solo a comprobantes

# def desde_hasta(data):
        
#     if (data.get('numero de comprobante') != data.get('numero de comprobante hasta')):
#         data['numero de comprobante hasta'] = data['numero de comprobante']
#         return data
#     else:
#         return data

# def verificar_comprador(data):

#     # Se verifica que el cuit y los datos del cliente cargados
#     # en la venta esten bien
#     # -----------------------------------------------------------------
#     # Se verifica el CUIT y si el monto es mayor o menor que 1000 pesos

#     resultado_cuit = verificador_cuit(
#         data.get('numero de identificacion del comprador')
#         )
    
#     # El nro de comprador si aparece no es valido por lo que se lo cambia por 
#     # 80 que es para facturas

#     if (data.get('codigo de documento del comprador') == '87'):
#         data['codigo de documento del comprador'] = '80'
    
#     # Verificamos que este bien para para las NOTAS DE CREDITO y DEBITO

#     if (data.get('tipo de comprobante') == '113'):
#         data['codigo de documento del comprador'] = '99'


#     # Si el nro de comprador es 99 se analiza si el monto es mayor o menor de 1000 pesos
    
#     if (data.get('codigo de documento del comprador') == '99'):
#         if (int(data.get('importe total de la operacion')) < 1000):
#             data['numero de identificacion del comprador'] = '00000000000000000000'
#             data['apellido y nombre o denominacion del comprador'] = 'CONSUMIDOR FINAL              '
#         elif (int(data.get('importe total de la operacion')) >= 1000):
#             data['numero de identificacion del comprador'] = '00000000000000000000'
#             data['apellido y nombre o denominacion del comprador'] = 'VENTA GLOBAL DIARIA           '
#     elif (resultado_cuit == False):
#         if (int(data.get('importe total de la operacion')) < 1000):
#             data['codigo de documento del comprador'] = '99'
#             data['numero de identificacion del comprador'] = '00000000000000000000'
#             data['apellido y nombre o denominacion del comprador'] = 'CONSUMIDOR FINAL              '
#         elif (int(data.get('importe total de la operacion')) >= 1000):
#             data['codigo de documento del comprador'] = '99'
#             data['numero de identificacion del comprador'] = '00000000000000000000'
#             data['apellido y nombre o denominacion del comprador'] = 'VENTA GLOBAL DIARIA           '
    
#     return data

# def revision_alicuotasAlicuotas(data):
    
#     # Se verifica que el codigo de alicuota no sea el de No gavado de ser asi
#     # se cambia por el de 0%

#     if data.get('alicuota de iva') == '0001':
#         data['alicuota de iva'] = '0003'
    
#     return data

# # Funciones que pertenecen solo a Alicuotas

# # Clases

# class comprobante:

#     def __init__(self):
#         return
    
#     def campos_comprobante(self, linea):

#         # Formato de comprobantes segun AFIP
#         # Tomamos la linea y devolvemos un diccionario con todas las partes para una
#         # facil revisión de los datos

#         campos_cbte = {
#             'fecha de comprobante': linea[0:8],
#             'tipo de comprobante': linea[8:11],
#             'punto de venta': linea[11:16],
#             'numero de comprobante': linea[16:36],
#             'numero de comprobante hasta': linea[36:56],
#             'codigo de documento del comprador': linea[56:58],
#             'numero de identificacion del comprador': linea[58:78],
#             'apellido y nombre o denominacion del comprador': linea[78:108],
#             'importe total de la operacion': linea[108:123],
#             'importe total de conceptos que no integran el precio neto gravado': linea[123:138],
#             'percepcion a no categorizados': linea[138:153],
#             'importe de operaciones exentas': linea[153:168],
#             'importe de percepciones o pagos a cuenta de impuestos nacionales': linea[168:183],
#             'importe de percepciones de ingresos brutos': linea[183:198],
#             'importe de percepciones impuestos municipales': linea[198:213],
#             'importe impuestos internos': linea[213:228],
#             'codigo de moneda': linea[228:231],
#             'tipo de cambio': linea[231:241],
#             'cantidad de alicuotas de iva': linea[241:242],
#             'codigo de operacion': linea[242:243],
#             'otros tributos': linea[243:258],
#             'fecha de vencimiento de pago': linea[258:266]
#         }

#         return campos_cbte

#     # Construimos la linea en el orden correcto para evitar errores en otras partes del programa
    
#     def construir_linea_comprobante(self, data):
#         linea = data['fecha de comprobante'] + \
#         data['tipo de comprobante'] + \
#         data['punto de venta'] + \
#         data['numero de comprobante'] + \
#         data['numero de comprobante hasta'] + \
#         data['codigo de documento del comprador'] + \
#         data['numero de identificacion del comprador'] + \
#         data['apellido y nombre o denominacion del comprador'] + \
#         data['importe total de la operacion'] + \
#         data['importe total de conceptos que no integran el precio neto gravado'] + \
#         data['percepcion a no categorizados'] + \
#         data['importe de operaciones exentas'] + \
#         data['importe de percepciones o pagos a cuenta de impuestos nacionales'] + \
#         data['importe de percepciones de ingresos brutos'] + \
#         data['importe de percepciones impuestos municipales'] + \
#         data['importe impuestos internos'] + \
#         data['codigo de moneda'] + \
#         data['tipo de cambio'] + \
#         data['cantidad de alicuotas de iva'] + \
#         data['codigo de operacion'] + \
#         data['otros tributos'] + \
#         data['fecha de vencimiento de pago']

#         return linea

#     def procesamiento_comprobantes(self, archivo):
#         nueva_lista = []
#         try:
#             with open(archivo, mode='r', encoding='latin-1') as lista:

#                 for linea in lista:
#                     data = self.campos_comprobante(linea)
#                     data = remplazo_tipo_operacion(data,comprobantes=True)
#                     data = desde_hasta(data)
#                     data = verificar_comprador(data)
#                     nueva_lista.append(self.construir_linea_comprobante(data))

#                 return nueva_lista
#         except Exception as error:
#             print(error)
#             return

#     def remove_ptv(self, ptv, archivo):
#         nueva_lista = []
#         try:
#             with open(archivo, mode='r', encoding='latin-1') as lista:
#                 for linea in lista:
#                     data = self.campos_comprobante(linea)
#                     if data['punto de venta'] != ptv:
#                         nueva_lista.append(self.construir_linea_comprobante(data))
#             return nueva_lista
#         except Exception as e:
#             print(e)
    
#     def input_database(self,archivo):
#         try:
#             con = sqlite3.connect('ventas.db')
#             cur = con.cursor()
#             with open(archivo,mode='r', encoding='latin-1') as lista:
#                 for linea in lista:
#                     data = self.campos_comprobante(linea)
#                     cur.execute('''INSERT INTO cbte VALUES (
#                         ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (data['fecha de comprobante'],
#                         data['tipo de comprobante'],
#                         data['punto de venta'],
#                         data['numero de comprobante'],
#                         data['numero de comprobante hasta'],
#                         data['codigo de documento del comprador'],
#                         data['numero de identificacion del comprador'],
#                         data['apellido y nombre o denominacion del comprador'],
#                         data['importe total de la operacion'],
#                         data['importe total de conceptos que no integran el precio neto gravado'],
#                         data['percepcion a no categorizados'],
#                         data['importe de operaciones exentas'],
#                         data['importe de percepciones o pagos a cuenta de impuestos nacionales'],
#                         data['importe de percepciones de ingresos brutos'],
#                         data['importe de percepciones impuestos municipales'],
#                         data['importe impuestos internos'],
#                         data['codigo de moneda'],
#                         data['tipo de cambio'],
#                         data['cantidad de alicuotas de iva'],
#                         data['codigo de operacion'],
#                         data['otros tributos'],
#                         data['fecha de vencimiento de pago']))
#             con.commit()
#             con.close()
#         except Exception as e:
#             print(e)

# class alicuota:

#     def __init__(self):
#         return

#     def campos_alicuotas(self, linea):

#         # Formato que tienen las lineas de alicuotas
#         campos_ali = {
#             'tipo de comprobante': linea[0:3],
#             'punto de venta': linea[3:8],
#             'numero de comprobante': linea[8:28],
#             'importe neto gravado': linea[28:43],
#             'alicuota de iva': linea[43:47],
#             'impuesto liquidado': linea[47:62]
#         }

#         return campos_ali
    
#     def construir_linea_alicuota(self, data):
#         linea = data['tipo de comprobante'] + \
#         data['punto de venta'] + \
#         data['numero de comprobante'] + \
#         data['importe neto gravado'] + \
#         data['alicuota de iva'] + \
#         data['impuesto liquidado']

#         return linea

#     def procesamiento_alicuotas(self, archivo):
#         nueva_lista = []
#         try:
#             with open(archivo, mode='r', encoding='latin-1') as lista:

#                 for linea in lista:
#                     data = self.campos_alicuotas(linea)
#                     data = remplazo_tipo_operacion(data, alicuotas=True)
#                     data = revision_alicuotasAlicuotas(data)
#                     nueva_lista.append(self.construir_linea_alicuota(data))
#                 return nueva_lista
#         except Exception as error:
#             print(error)
#             return

#     def remove_ptv(self, ptv, archivo):
#         nueva_lista = []
#         try:
#             with open(archivo, mode='r', encoding='latin-1') as lista:
#                 for linea in lista:
#                     data = self.campos_alicuotas(linea)
#                     if data['punto de venta'] != ptv:
#                         nueva_lista.append(self.construir_linea_alicuota(data))
#             return nueva_lista
#         except Exception as e:
#             print(e)

#     def input_database(self,archivo):
#         try:
#             con = sqlite3.connect('ventas.db')
#             cur = con.cursor()
#             with open(archivo,mode='r', encoding='latin-1') as lista:
#                 for linea in lista:
#                     data = self.campos_alicuotas(linea)
#                     cur.execute('''INSERT INTO alicuotas VALUES (
#                         ?,?,?,?,?,?)''', (
#                             data['tipo de comprobante'],
#                             data['punto de venta'],
#                             data['numero de comprobante'],
#                             data['importe neto gravado'],
#                             data['alicuota de iva'],
#                             data['impuesto liquidado']))
#             con.commit()
#             con.close()
#         except Exception as e:
#             print(e)
class Cbte:
	"""
	Comprobante object
	"""
	def __init__(self):
		self.fecha_de_comprobante = ""
		self.tipo_de_comprobante = ""
		self.punto_de_venta = ""
		self.numero_de_comprobante = ""
		self.numero_de_comprobante_hasta = ""
		self.codigo_de_documento_del_comprador = ""
		self.numero_de_identificacion_del_comprador = ""
		self.apellido_y_nombre_o_denominacion_del_comprador = ""
		self.importe_total_de_la_operacion = ""
		self.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = ""
		self.percepcion_a_no_categorizados = ""
		self.importe_de_operaciones_exentas = ""
		self.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = ""
		self.importe_de_percepciones_de_ingresos_brutos = ""
		self.importe_de_percepciones_impuestos_municipales = ""
		self.importe_impuestos_internos = ""
		self.codigo_de_moneda = ""
		self.tipo_de_cambio = ""
		self.cantidad_de_alicuotas_de_iva = ""
		self.codigo_de_operacion = ""
		self.otros_tributos = ""
		self.fecha_de_vencimiento_de_pago = ""
		
	def get_cbte_data(self) -> str:
		"""Return a line str with the content of variables"""
		data = self.fecha_de_comprobante + \
			self.tipo_de_comprobante + \
			self.punto_de_venta + \
			self.numero_de_comprobante + \
			self.numero_de_comprobante_hasta + \
			self.codigo_de_documento_del_comprador + \
			self.numero_de_identificacion_del_comprador + \
			self.apellido_y_nombre_o_denominacion_del_comprador + \
			self.importe_total_de_la_operacion + \
			self.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado + \
			self.percepcion_a_no_categorizados + \
			self.importe_de_operaciones_exentas + \
			self.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales + \
			self.importe_de_percepciones_de_ingresos_brutos + \
			self.importe_de_percepciones_impuestos_municipales + \
			self.importe_impuestos_internos + \
			self.codigo_de_moneda + \
			self.tipo_de_cambio + \
			self.cantidad_de_alicuotas_de_iva + \
			self.codigo_de_operacion + \
			self.otros_tributos + \
			self.fecha_de_vencimiento_de_pago 
		return data
	
	def set_cbte_data(self,data) -> None:
		"""Set variables in the object"""
		self.fecha_de_comprobante = data[0:8]
		self.tipo_de_comprobante = data[8:11]
		self.punto_de_venta = data[11:16]
		self.numero_de_comprobante = data[16:36]
		self.numero_de_comprobante_hasta = data[36:56]
		self.codigo_de_documento_del_comprador = data[56:58]
		self.numero_de_identificacion_del_comprador = data[58:78]
		self.apellido_y_nombre_o_denominacion_del_comprador = data[78:108]
		self.importe_total_de_la_operacion = data[108:123]
		self.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = data[123:138]
		self.percepcion_a_no_categorizados = data[138:153]
		self.importe_de_operaciones_exentas = data[153:168]
		self.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = data[168:183]
		self.importe_de_percepciones_de_ingresos_brutos = data[183:198]
		self.importe_de_percepciones_impuestos_municipales = data[198:213]
		self.importe_impuestos_internos = data[213:228]
		self.codigo_de_moneda = data[228:231]
		self.tipo_de_cambio = data[231:241]
		self.cantidad_de_alicuotas_de_iva = data[241:242]
		self.codigo_de_operacion = data[242:243]
		self.otros_tributos = data[243:258]
		self.fecha_de_vencimiento_de_pago = data[258:266]

class Alicuota:
	"""
	Alicuota object
	"""
	def __init__(self) -> None:
		self.tipo_de_comprobante = ""
		self.punto_de_venta = ""
		self.numero_de_comprobante = ""
		self.importe_neto_gravado = ""
		self.alicuota_de_iva = ""
		self.impuesto_liquidado = ""

	def set_alicuota_data(self, data) -> None:
		"""Set data of the object"""
		self.tipo_de_comprobante = data[0:3]
		self.punto_de_venta = data[3:8]
		self.numero_de_comprobante = data[8:28]
		self.importe_neto_gravado = data[28:43]
		self.alicuota_de_iva = data[43:47]
		self.impuesto_liquidado = data[47:62]
	
	def get_alicuota_data(self) -> str:
		"""Get data string in one line"""
		data = self.tipo_de_comprobante + \
			self.punto_de_venta + \
			self.numero_de_comprobante + \
			self.importe_neto_gravado + \
			self.alicuota_de_iva + \
			self.impuesto_liquidado
		return data

class Venta:
	"""
	Object to process CBTE and ALICUOTAS files
	"""
	def __init__(self, cbte, alicuota):
		self.cbte_file = self.file_generator(cbte)
		self.alicuota_file = self.file_generator(alicuota)
		self.cbte = []
		self.alicuota = []

	def file_generator(self, file) -> Generator:
		"""Creates a generator from a txt file"""
		with open(file, "r", encoding="latin-1") as f:
			for l in f.readlines():
				line = l.replace("\n","")
				yield line
	
	def write_file(self, filename, data_to_use = None) -> None:
		"""Write a file in the current location"""
		try:
			with open(filename, "w", encoding="latin-1", newline="\r\n") as f:
				if data_to_use == "cbte":
					for line in self.cbte:
                				f.write(line + '\n')
				else:
					for line in self.alicuota:
						f.write(line + '\n')
		except Exception as e:
			print(e)

	def create_database(self) -> None:
		"""Write a sqlite3 database in the current location"""
		try:
			conn = sqlite3.connect("ventas.db")
			cur = conn.cursor()
			#TODO add a key plus the data of the object
		except Exception as e:
			print(e)
		finally:
			conn.commit()
			conn.close()

	def process_cbte_and_alicuota(self) -> None:
		"""Process cbte and alicuota
		   This verified if the number of operation and until operation
		"""
		try:
			while True:
				line_cbte = next(self.cbte_file)
				cbte = Cbte()
				cbte.set_cbte_data(line_cbte)
				cbte.numero_de_comprobante = cbte.numero_de_comprobante_hasta
				key = cbte.fecha_de_comprobante + cbte.tipo_de_comprobante + cbte.punto_de_venta + cbte.numero_de_comprobante
				alicuota = Alicuota()
				self.cbte.append(cbte.get_cbte_data())
				for _ in range(cbte.cantidad_de_alicuotas_de_iva):
					line_alicuota = next(self.alicuota_file)
					alicuota.set_alicuota_data(line_alicuota)
					alicuota.numero_de_comprobante = cbte.numero_de_comprobante_hasta
					self.alicuota.append(alicuota.get_alicuota_data())
		except StopIteration:
			print("Se procesaron los datos correctamente, se procede a grabarlos")