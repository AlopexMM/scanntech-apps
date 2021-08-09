# -*- coding: latin-1 -*-

''' En esta clase se puede encontrar las funciones que modifican el archivo de 
comprobantes'''

import sqlite3
import os
from typing import Generator


class Cbte:
	"""
	Comprobante object
	"""
	def __init__(self):
		self.fecha_de_comprobante = "00000000"
		self.tipo_de_comprobante = "082"
		self.punto_de_venta = "00000"
		self.numero_de_comprobante = "00000000000000000000"
		self.numero_de_comprobante_hasta = "00000000000000000000"
		self.codigo_de_documento_del_comprador = "99"
		self.numero_de_identificacion_del_comprador = "00000000000000000000"
		self.apellido_y_nombre_o_denominacion_del_comprador = "VENTA GLOBAL DIARIA           "
		self.importe_total_de_la_operacion = "000000000000000"
		self.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = "000000000000000"
		self.percepcion_a_no_categorizados = "000000000000000"
		self.importe_de_operaciones_exentas = "000000000000000"
		self.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = "000000000000000"
		self.importe_de_percepciones_de_ingresos_brutos = "000000000000000"
		self.importe_de_percepciones_impuestos_municipales = "000000000000000"
		self.importe_impuestos_internos = "000000000000000"
		self.codigo_de_moneda = "PES"
		self.tipo_de_cambio = "0001000000"
		self.cantidad_de_alicuotas_de_iva = "0"
		self.codigo_de_operacion = " "
		self.otros_tributos = "000000000000000"
		self.fecha_de_vencimiento_de_pago = "00000000"
		
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
	
	def set_cbte_data(self, data=None, fecha_de_comprobante=None,tipo_de_comprobante="082",punto_de_venta=None,numero_de_comprobante=None,numero_de_comprobante_hasta=None,codigo_de_documento_del_comprador="99",numero_de_identificacion_del_comprador="00000000000000000000",apellido_y_nombre_o_denominacion_del_comprador="VENTA GLOBAL DIARIA           ",importe_total_de_la_operacion = None,importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = None,percepcion_a_no_categorizados=None,importe_de_operaciones_exentas=None,importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales=None,importe_de_percepciones_de_ingresos_brutos=None,importe_de_percepciones_impuestos_municipales=None,importe_impuestos_internos=None,codigo_de_moneda="PES",tipo_de_cambio="0001000000",cantidad_de_alicuotas_de_iva=None,codigo_de_operacion=" ",otros_tributos="000000000000000",fecha_de_vencimiento_de_pago="00000000") -> None:
		"""Set variables in the object"""
		if data != None:
			"""This set the variables from a line of text"""
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
			return
		else:
			self.fecha_de_comprobante = fecha_de_comprobante
			self.tipo_de_comprobante = tipo_de_comprobante
			self.punto_de_venta = punto_de_venta
			self.numero_de_comprobante = numero_de_comprobante
			self.numero_de_comprobante_hasta = numero_de_comprobante_hasta
			self.codigo_de_documento_del_comprador = codigo_de_documento_del_comprador
			self.numero_de_identificacion_del_comprador = numero_de_identificacion_del_comprador
			self.apellido_y_nombre_o_denominacion_del_comprador = apellido_y_nombre_o_denominacion_del_comprador
			self.importe_total_de_la_operacion = importe_total_de_la_operacion
			self.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado
			self.percepcion_a_no_categorizados = percepcion_a_no_categorizados
			self.importe_de_operaciones_exentas = importe_de_operaciones_exentas
			self.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales
			self.importe_de_percepciones_de_ingresos_brutos = importe_de_percepciones_de_ingresos_brutos
			self.importe_de_percepciones_impuestos_municipales = importe_de_percepciones_impuestos_municipales
			self.importe_impuestos_internos = importe_impuestos_internos
			self.codigo_de_moneda = codigo_de_moneda
			self.tipo_de_cambio = tipo_de_cambio
			self.cantidad_de_alicuotas_de_iva = cantidad_de_alicuotas_de_iva
			self.codigo_de_operacion = codigo_de_operacion
			self.otros_tributos = otros_tributos
			self.fecha_de_vencimiento_de_pago = fecha_de_vencimiento_de_pago
			return

class Alicuota:
	"""
	Alicuota object
	"""
	def __init__(self) -> None:
		self.tipo_de_comprobante = "082"
		self.punto_de_venta = "00000"
		self.numero_de_comprobante = "00000000000000000000"
		self.importe_neto_gravado = "000000000000000"
		self.alicuota_de_iva = "0000"
		self.impuesto_liquidado = "000000000000000"

	def set_alicuota_data(self, data = None, tipo_de_comprobante = "082", punto_de_venta = "00000", numero_de_comprobante = "00000000000000000000", importe_neto_gravado = "000000000000000", alicuota_de_iva = "0000", impuesto_liquidado = "000000000000000") -> None:
		"""Set data of the object"""
		if data != None:
			self.tipo_de_comprobante = data[0:3]
			self.punto_de_venta = data[3:8]
			self.numero_de_comprobante = data[8:28]
			self.importe_neto_gravado = data[28:43]
			self.alicuota_de_iva = data[43:47]
			self.impuesto_liquidado = data[47:62]
			return
		else:
			self.tipo_de_comprobante = tipo_de_comprobante
			self.punto_de_venta = punto_de_venta
			self.numero_de_comprobante = numero_de_comprobante
			self.importe_neto_gravado = importe_neto_gravado
			self.alicuota_de_iva = alicuota_de_iva
			self.impuesto_liquidado = impuesto_liquidado
		return
	
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
		self.db = "ventas.db"

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
			os.remove(self.db)
		except FileNotFoundError:
			print("Base no encontrada no te preocupes la creare")
		finally:
			conn = sqlite3.connect(self.db)
			cur = conn.cursor()
			cur.execute('''CREATE TABLE cbte (
		    	"fecha_de_comprobante",
                    	"tipo_de_comprobante",
                    	"punto_de_venta",
                    	"numero_de_comprobante",
                    	"numero_de_comprobante_hasta",
                    	"codigo_de_documento_del_comprador",
                    	"numero_de_identificacion_del_comprador",
                    	"apellido_y_nombre_o_denominacion_del_comprador",
                    	"importe_total_de_la_operacion",
                    	"importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado",
                    	"percepcion_a_no_categorizados",
                    	"importe_de_operaciones_exentas",
                    	"importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales",
                    	"importe_de_percepciones_de_ingresos_brutos",
                    	"importe_de_percepciones_impuestos_municipales",
                    	"importe_impuestos_internos",
                    	"codigo_de_moneda",
                    	"tipo_de_cambio",
                    	"cantidad_de_alicuotas_de_iva",
                    	"codigo_de_operacion",
                    	"otros_tributos",
                    	"fecha_de_vencimiento_de_pago")''')
			cur.execute('''CREATE TABLE alicuotas ("tipo_de_comprobante",
                        "punto_de_venta",
                        "numero_de_comprobante",
                        "importe_neto_gravado",
                        "alicuota_de_iva",
                        "impuesto_liquidado")''')
			conn.commit()
			for l in self.cbte:
				db_cbte = Cbte()
				db_cbte.set_cbte_data(l)
				cur.execute('''INSERT INTO cbte VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
					db_cbte.fecha_de_comprobante,
                        		db_cbte.tipo_de_comprobante,
                        		db_cbte.punto_de_venta,
                        		db_cbte.numero_de_comprobante,
                        		db_cbte.numero_de_comprobante_hasta,
                        		db_cbte.codigo_de_documento_del_comprador,
                        		db_cbte.numero_de_identificacion_del_comprador,
                        		db_cbte.apellido_y_nombre_o_denominacion_del_comprador,
                        		db_cbte.importe_total_de_la_operacion,
                        		db_cbte.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado,
                        		db_cbte.percepcion_a_no_categorizados,
                        		db_cbte.importe_de_operaciones_exentas,
                        		db_cbte.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales,
                        		db_cbte.importe_de_percepciones_de_ingresos_brutos,
                        		db_cbte.importe_de_percepciones_impuestos_municipales,
                        		db_cbte.importe_impuestos_internos,
                        		db_cbte.codigo_de_moneda,
                        		db_cbte.tipo_de_cambio,
                        		db_cbte.cantidad_de_alicuotas_de_iva,
                        		db_cbte.codigo_de_operacion,
                        		db_cbte.otros_tributos,
                        		db_cbte.fecha_de_vencimiento_de_pago))
			conn.commit()
			for l in self.alicuota:
				db_alicuota = Alicuota()
				db_alicuota.set_alicuota_data(l)
				cur.execute('''INSERT INTO alicuotas VALUES (?,?,?,?,?,?)''', (
                            		db_alicuota.tipo_de_comprobante,
                            		db_alicuota.punto_de_venta,
                            		db_alicuota.numero_de_comprobante,
                            		db_alicuota.importe_neto_gravado,
                            		db_alicuota.alicuota_de_iva,
                            		db_alicuota.impuesto_liquidado))
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
				for _ in range(int(cbte.cantidad_de_alicuotas_de_iva)):
					line_alicuota = next(self.alicuota_file)
					alicuota.set_alicuota_data(line_alicuota)
					alicuota.numero_de_comprobante = cbte.numero_de_comprobante_hasta
					self.alicuota.append(alicuota.get_alicuota_data())
		except StopIteration:
			print("Se procesaron los datos correctamente, se procede a grabarlos")
	
	def process_tbl(self, tblerrores) -> None:
		"""Process tblerrores.txt and process the database according the operations obtain from the file"""
		duplicates = []
		with open(tblerrores, "r", encoding="latin-1") as f:
			for l in f.readlines():
				line = l.split(";")
				if line[0] == 0 or line[0] == "0":
					e = line[1].split(" ")
					if e[0] == "COMPROBANTE":
						if e[1] == "DUPLICADO":
							duplicate = {}
							errors = e[6].split("/")
							duplicate["tipo_operacion"] = errors[0]
							duplicate["punto_venta"] = errors[1].split("-")[0]
							duplicate["numero_operacion"] = "%" + errors[1].split("-")[1]
							duplicates.append(duplicate)
		if len(duplicates) > 0:
			self._process_duplicate(duplicates)
	
	def _process_duplicate(self, operations):
		"""Proces file duplicates removing all duplicates and impact one line of VENTA GLOBAL DIARIA"""
		conn = sqlite3.connect(self.db)
		cur = conn.cursor()
		for l in operations:
			alicuotas = cur.execute("""SELECT tipo_de_comprobante,punto_de_venta,numero_de_comprobante,importe_neto_gravado,alicuota_de_iva,impuesto_liquidado FROM alicuotas WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""",(l["tipo_operacion"],l["punto_venta"],l["numero_operacion"]))
			cod_alicuota = {
				"0004":0,
				"0005":0,
				"0003":0,
			}
			iva21 = Alicuota()
			iva105 = Alicuota()
			iva3 = Alicuota()
			for row in alicuotas:
				if row == "0003":
					cod_alicuota["0003"] = 1
					importe_neto_gravado = str(int(iva3.importe_neto_gravado) + int(row[3])).zfill(15)
					impuesto_liquidado = str(int(iva3.impuesto_liquidado) + int(row[5])).zfill(15)
					iva3.set_alicuota_data(punto_de_venta=row[1],numero_de_comprobante=row[2],importe_neto_gravado=importe_neto_gravado,alicuota_de_iva="0003",impuesto_liquidado=impuesto_liquidado)
				if row == "0004":
					cod_alicuota["0004"] = 1
					importe_neto_gravado = str(int(iva105.importe_neto_gravado) + int(row[3])).zfill(15)
					impuesto_liquidado = str(int(iva105.impuesto_liquidado) + int(row[5])).zfill(15)
					iva105.set_alicuota_data(punto_de_venta=row[1],numero_de_comprobante=row[2],importe_neto_gravado=importe_neto_gravado,alicuota_de_iva="0004",impuesto_liquidado=impuesto_liquidado)
				if row == "0005":
					cod_alicuota["0005"] = 1
					importe_neto_gravado = str(int(iva21.importe_neto_gravado) + int(row[3])).zfill(15)
					impuesto_liquidado = str(int(iva21.impuesto_liquidado) + int(row[5])).zfill(15)
					iva21.set_alicuota_data(punto_de_venta=row[1],numero_de_comprobante=row[2],importe_neto_gravado=importe_neto_gravado,alicuota_de_iva="0005",impuesto_liquidado=impuesto_liquidado)
			cur.execute("""DELETE FROM alicuotas WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""",(l["tipo_operacion"],l["punto_venta"],l["numero_operacion"]))
			conn.commit()
			if cod_alicuota["0003"] == 1:
				cur.execute('''INSERT INTO alicuotas VALUES (?,?,?,?,?,?)''', (
                            		iva3.tipo_de_comprobante,
                            		iva3.punto_de_venta,
                            		iva3.numero_de_comprobante,
                            		iva3.importe_neto_gravado,
                            		iva3.alicuota_de_iva,
                            		iva3.impuesto_liquidado))
			if cod_alicuota["0004"] == 1:
				cur.execute('''INSERT INTO alicuotas VALUES (?,?,?,?,?,?)''', (
                            		iva105.tipo_de_comprobante,
                            		iva105.punto_de_venta,
                            		iva105.numero_de_comprobante,
                            		iva105.importe_neto_gravado,
                            		iva105.alicuota_de_iva,
                            		iva105.impuesto_liquidado))
			if cod_alicuota["0005"] == 1:
				cur.execute('''INSERT INTO alicuotas VALUES (?,?,?,?,?,?)''', (
                            		iva21.tipo_de_comprobante,
                            		iva21.punto_de_venta,
                            		iva21.numero_de_comprobante,
                            		iva21.importe_neto_gravado,
                            		iva21.alicuota_de_iva,
                            		iva21.impuesto_liquidado))
			conn.commit()
			cont_alicuota = 0
			for x in cod_alicuota:
				if x == 1:
					cont_alicuota += x
			cbtes = cur.execute("""SELECT fecha_de_comprobante,tipo_de_comprobante,punto_de_venta,numero_de_comprobante,numero_de_comprobante_hasta,codigo_de_documento_del_comprador,numero_de_identificacion_del_comprador,apellido_y_nombre_o_denominacion_del_comprador,importe_total_de_la_operacion,importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado,percepcion_a_no_categorizados,importe_de_operaciones_exentas,importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales,importe_de_percepciones_de_ingresos_brutos,importe_de_percepciones_impuestos_municipales,importe_impuestos_internos,tipo_de_cambio,cantidad_de_alicuotas_de_iva,codigo_de_operacion,otros_tributos,fecha_de_vencimiento_de_pago 
			    FROM cbte WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""", (l["tipo_operacion"],l["punto_venta"],l["numero_operacion"]))
			cbte = Cbte()
			
			for row in cbtes:
				importe_total_de_la_operacion = int(row[8]) + int(cbte.importe_total_de_la_operacion) 
				importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = int(row[9]) + int(cbte.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado)
				percepcion_a_no_categorizados = int(row[10]) + int(cbte.percepcion_a_no_categorizados)
				importe_de_operaciones_exentas = int(row[11]) + int(cbte.importe_de_operaciones_exentas)
				importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = int(row[12]) + int(cbte.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales)
				importe_de_percepciones_de_ingresos_brutos = int(row[13]) + int(cbte.importe_de_percepciones_de_ingresos_brutos)
				importe_de_percepciones_impuestos_municipales = int(row[14]) + int(cbte.importe_de_percepciones_impuestos_municipales)
				importe_impuestos_internos = int(row[15]) + int(cbte.importe_impuestos_internos)

				cbte.set_cbte_data(fecha_de_comprobante=row[0],
				punto_de_venta=row[2],
				numero_de_comprobante=row[3],
				numero_de_comprobante_hasta=row[4],
				importe_total_de_la_operacion = str(importe_total_de_la_operacion).zfill(15),
				importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = str(importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado).zfill(15),
				percepcion_a_no_categorizados = str(percepcion_a_no_categorizados).zfill(15),
				importe_de_operaciones_exentas = str(importe_de_operaciones_exentas).zfill(15),
				importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = str(importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales).zfill(15),
				importe_de_percepciones_de_ingresos_brutos = str(importe_de_percepciones_de_ingresos_brutos).zfill(15),
				importe_de_percepciones_impuestos_municipales = str(importe_de_percepciones_impuestos_municipales).zfill(15),
				importe_impuestos_internos = str(importe_impuestos_internos).zfill(15),
				cantidad_de_alicuotas_de_iva=str(cont_alicuota))
			
			cur.execute("""DELETE FROM cbte WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""",(l["tipo_operacion"],l["punto_venta"],l["numero_operacion"]))
			conn.commit()
			cur.execute('''INSERT INTO cbte VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
					cbte.fecha_de_comprobante,
                        		cbte.tipo_de_comprobante,
                        		cbte.punto_de_venta,
                        		cbte.numero_de_comprobante,
                        		cbte.numero_de_comprobante_hasta,
                        		cbte.codigo_de_documento_del_comprador,
                        		cbte.numero_de_identificacion_del_comprador,
                        		cbte.apellido_y_nombre_o_denominacion_del_comprador,
                        		cbte.importe_total_de_la_operacion,
                        		cbte.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado,
                        		cbte.percepcion_a_no_categorizados,
                        		cbte.importe_de_operaciones_exentas,
                        		cbte.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales,
                        		cbte.importe_de_percepciones_de_ingresos_brutos,
                        		cbte.importe_de_percepciones_impuestos_municipales,
                        		cbte.importe_impuestos_internos,
                        		cbte.codigo_de_moneda,
                        		cbte.tipo_de_cambio,
                        		cbte.cantidad_de_alicuotas_de_iva,
                        		cbte.codigo_de_operacion,
                        		cbte.otros_tributos,
                        		cbte.fecha_de_vencimiento_de_pago))
			conn.commit()
		