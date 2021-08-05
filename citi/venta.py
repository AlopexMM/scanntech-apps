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
			os.remove("ventas.db")
		except FileNotFoundError:
			print("Base no encontrada no te preocupes la creare")
		finally:
			conn = sqlite3.connect("ventas.db")
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