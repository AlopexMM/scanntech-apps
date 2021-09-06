# -*- coding: latin-1 -*-
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

from sqlalchemy.sql.expression import null

Base = declarative_base()
from typing import Generator

import os


class Cbte(Base):
    """
    Cbte object for line_cbtebase
    """

    __tablename__ = "ventas_cbte"
    id = Column(Integer,primary_key=True)
    id_extra = Column(String(28), nullable=False)
    fecha_de_comprobante = Column(String(8),nullable=False)
    tipo_de_comprobante = Column(String(3),nullable=False)
    punto_de_venta = Column(String(5),nullable=False)
    numero_de_comprobante = Column(String(20),nullable=False)
    numero_de_comprobante_hasta = Column(String(20),nullable=False)
    codigo_de_documento_del_comprador = Column(String(2),nullable=False)
    numero_de_identificacion_del_comprador = Column(String(20),nullable=False)
    apellido_y_nombre_o_denominacion_del_comprador = Column(String(30),nullable=False)
    importe_total_de_la_operacion = Column(String(15),nullable=False)
    importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = Column(String(15),nullable=False)
    percepcion_a_no_categorizados = Column(String(15),nullable=False)
    importe_de_operaciones_exentas = Column(String(15),nullable=False)
    importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = Column(String(15),nullable=False)
    importe_de_percepciones_de_ingresos_brutos = Column(String(15),nullable=False)
    importe_de_percepciones_impuestos_municipales = Column(String(15),nullable=False)
    importe_impuestos_internos = Column(String(15),nullable=False)
    codigo_de_moneda = Column(String(3),nullable=False)
    tipo_de_cambio = Column(String(10),nullable=False)
    cantidad_de_alicuotas_de_iva = Column(String(1),nullable=False)
    codigo_de_operacion = Column(String(1),nullable=False)
    otros_tributos = Column(String(15),nullable=False)
    fecha_de_vencimiento_de_pago = Column(String(8),nullable=False)

    def __repr__(self):
        message = f"""Cbte(
            id:{self.id!r},
            fecha_de_comprobante:{self.fecha_de_comprobante!r},
            tipo_de_comprobante:{self.tipo_de_comprobante!r},
            punto_de_venta:{self.punto_de_venta!r},
            numero_de_comprobante:{self.numero_de_comprobante!r},
	    numero_de_comprobante_hasta:{self.numero_de_comprobante_hasta!r},
	    codigo_de_documento_del_comprador = {self.codigo_de_documento_del_comprador!r},
    	    numero_de_identificacion_del_comprador = {self.numero_de_identificacion_del_comprador!r},
    	    apellido_y_nombre_o_denominacion_del_comprador = {self.apellido_y_nombre_o_denominacion_del_comprador!r},
    	    importe_total_de_la_operacion = {self.importe_total_de_la_operacion!r},
    	    importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = {self.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado!r},
    	    percepcion_a_no_categorizados = {self.percepcion_a_no_categorizados!r},
    	    importe_de_operaciones_exentas = {self.importe_de_operaciones_exentas!r},
    	    importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = {self.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales!r},
    	    importe_de_percepciones_de_ingresos_brutos = {self.importe_de_percepciones_de_ingresos_brutos!r},
    	    importe_de_percepciones_impuestos_municipales = {self.importe_de_percepciones_impuestos_municipales!r},
    	    importe_impuestos_internos = {self.importe_impuestos_internos!r}),
    	    codigo_de_moneda = {self.codigo_de_moneda!r}),
    	    tipo_de_cambio = {self.tipo_de_cambio!r},
    	    cantidad_de_alicuotas_de_iva = {self.cantidad_de_alicuotas_de_iva!r},
    	    codigo_de_operacion = {self.codigo_de_operacion!r},
    	    otros_tributos = {self.otros_tributos!r},
    	    fecha_de_vencimiento_de_pago = {self.fecha_de_comprobante!r}
	    )"""
        return message 

class Alicuota(Base):
    """
    Alicuota object for line_cbtebase
    """
    __tablename__ = "ventas_alicuotas"
    
    id = Column(Integer,primary_key=True)
    id_extra = Column(String(28),nullable=False)
    tipo_de_comprobante = Column(String(3),nullable=False)
    punto_de_venta = Column(String(5),nullable=False)
    numero_de_comprobante = Column(String(20),nullable=False)
    importe_neto_gravado = Column(String(15),nullable=False)
    alicuota_de_iva = Column(String(4),nullable=False)
    impuesto_liquidado = Column(String(15),nullable=False)

    def __repr__(self):
        return f"""Alicuotas(
		id:{self.id!r},
		cbte_id:{self.cbte_id!r},
		cbte_id:{self.cbte_id!r},
		tipo_de_comprobante:{self.tipo_de_comprobante!r},
		punto_de_venta:{self.punto_de_venta!r},
		numero_de_comprobante:{self.numero_de_comprobante!r},
		importe_neto_gravado:{self.importe_neto_gravado!r},
		alicuota_de_iva:{self.alicuota_de_iva!r},
		impuesto_liquidado:{self.impuesto_liquidado!r}
		)"""


class Venta:
	"""
	Object to process CBTE and ALICUOTAS files
	"""
	def __init__(self,cbte=None,alicuotas=None):
		self.engine = create_engine("sqlite+pysqlite:///:memory:")
		Base.metadata.create_all(self.engine)
		self.cbte_file = self._file_generator(cbte)
		self.alicuotas_file = self._file_generator(alicuotas)
        	self.session = Session(self.engine)
        	self.cbte_template = {
                	"fecha_de_comprobante" : "0".zfill(8),
                	"tipo_de_comprobante" : "082",
                	"punto_de_venta" : "0".zfill(5),
                	"numero_de_comprobante" : "0".zfill(20),
                	"numero_de_comprobante_hasta" : "0".zfill(20),
                	"codigo_de_documento_del_comprador" : "99",
                	"numero_de_identificacion_del_comprador" : "0".zfill(20),
                	"apellido_y_nombre_o_denominacion_del_comprador" : "VENTA GLOBAL DIARIA           ",
                	"importe_total_de_la_operacion" : 0,
                	"importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado" : 0,
                	"percepcion_a_no_categorizados" : 0,
                	"importe_de_operaciones_exentas" : 0,
                	"importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales" : 0,
                	"importe_de_percepciones_de_ingresos_brutos" : 0,
                	"importe_de_percepciones_impuestos_municipales" : 0,
                	"importe_impuestos_internos" : 0,
                	"codigo_de_moneda" : "PES",
                	"tipo_de_cambio" : "0001000000",
                	"cantidad_de_alicuotas_de_iva" : "0",
                	"codigo_de_operacion" : " ",
                	"otros_tributos" : "0".zfill(15),
                	"fecha_de_vencimiento_de_pago" : "0".zfill(8),
        	}	
        	self.alicuota_template = {
        	    "tipo_de_comprobante" : "082",
        	    "punto_de_venta" : "00000",
        	    "numero_de_comprobante" : "0".zfill(20),
        	    "importe_neto_gravado" : 0,
        	    "alicuota_de_iva" : "0".zfill(4),
        	    "impuesto_liquidado" : 0
        	}

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

	def process_cbte_and_alicuota(self,ptv=None) -> None:
		"""Process cbte and alicuota
		   This verified if the number of operation and until operation
		"""
		try:
			while True:
				line_cbte = next(self.cbte_file)
				cbte = Cbte()
				cbte.set_cbte_data(data=line_cbte)
				cbte.numero_de_comprobante = cbte.numero_de_comprobante_hasta
				alicuota = Alicuota()
				if ptv == None:
					self.cbte.append(cbte.get_cbte_data())
					for _ in range(int(cbte.cantidad_de_alicuotas_de_iva)):
						line_alicuota = next(self.alicuota_file)
						alicuota.set_alicuota_data(data=line_alicuota)
						alicuota.numero_de_comprobante = cbte.numero_de_comprobante_hasta
						self.alicuota.append(alicuota.get_alicuota_data())
				else:
					if cbte.punto_de_venta == ptv.zfill(5):
						for _ in range(int(cbte.cantidad_de_alicuotas_de_iva)):
							line_alicuota = next(self.alicuota_file)
						continue
					else:
						self.cbte.append(cbte.get_cbte_data())
						for _ in range(int(cbte.cantidad_de_alicuotas_de_iva)):
							line_alicuota = next(self.alicuota_file)
							alicuota.set_alicuota_data(data=line_alicuota)
							alicuota.numero_de_comprobante = cbte.numero_de_comprobante_hasta
							self.alicuota.append(alicuota.get_alicuota_data())
		except StopIteration:
			print("Se procesaron los datos correctamente, se procede a grabarlos")
	
	def process_tbl(self, tblerrores) -> None:
		"""Process tblerrores.txt and process the database according the operations obtain from the file"""
		try:
			duplicates = []
			with open(tblerrores, "r", encoding="latin-1") as f:
				for l in f.readlines():
					line = l.replace("\n","").split(";")
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
		except Exception as e:
			print(e)
			raise e
	
	def _process_duplicate(self, operations):
		"""Proces file duplicates removing all duplicates and impact one line of VENTA GLOBAL DIARIA"""
		conn = sqlite3.connect(self.db)
		cur = conn.cursor()
		total = len(operations)
		count_advance = 0
		for l in operations:
			# Process the duplicates operations in alicuotas
			count_advance += 1
			# alicuotas = cur.execute("""SELECT tipo_de_comprobante,punto_de_venta,numero_de_comprobante,SUM(importe_neto_gravado),alicuota_de_iva,SUM(impuesto_liquidado) FROM alicuotas WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""",(l["tipo_operacion"],l["punto_venta"],l["numero_operacion"]))
			cod_alicuota = [
				"0004",
				"0005",
				"0003",
			]
			cont_alicuota = 0
			alicuota_iva3 = 0
			for row in cod_alicuota:
				iva = Alicuota()
				cur.execute("""SELECT tipo_de_comprobante,punto_de_venta,numero_de_comprobante,SUM(importe_neto_gravado),alicuota_de_iva,SUM(impuesto_liquidado) FROM alicuotas WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ? and alicuota_de_iva is ?;""",(l["tipo_operacion"],l["punto_venta"],l["numero_operacion"],row))
				query = set(cur.fetchall())
				for q in query:
					if q[0] != None:
						iva.set_alicuota_data(tipo_de_comprobante=q[0],punto_de_venta=q[1],numero_de_comprobante=q[2],importe_neto_gravado=str(q[3]).zfill(15),alicuota_de_iva=q[4],impuesto_liquidado=str(q[5]).zfill(15))
						cur.execute("""DELETE FROM alicuotas WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""",("082",l["punto_venta"],l["numero_operacion"]))
						conn.commit()
						cur.execute('''INSERT INTO alicuotas VALUES (?,?,?,?,?,?)''', (
							iva.tipo_de_comprobante,
							iva.punto_de_venta,
							iva.numero_de_comprobante,
							iva.importe_neto_gravado,
							iva.alicuota_de_iva,
							iva.impuesto_liquidado)) 
						conn.commit()
						cont_alicuota += 1
						if row == "0003":
							alicuota_iva3 = 1
			codigo_operacion = " "
			if alicuota_iva3 == 1:
				codigo_operacion = "N"
			if cont_alicuota == 0:
				cur.execute("""DELETE FROM cbte WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""",(l["tipo_operacion"],l["punto_venta"],l["numero_operacion"]))
			else:
				# Process the duplicates operations in cbte
				cur.execute("""SELECT fecha_de_comprobante,tipo_de_comprobante,punto_de_venta,numero_de_comprobante,numero_de_comprobante_hasta,codigo_de_documento_del_comprador,numero_de_identificacion_del_comprador,apellido_y_nombre_o_denominacion_del_comprador,SUM(importe_total_de_la_operacion),SUM(importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado),SUM(percepcion_a_no_categorizados),SUM(importe_de_operaciones_exentas),SUM(importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales),SUM(importe_de_percepciones_de_ingresos_brutos),SUM(importe_de_percepciones_impuestos_municipales),SUM(importe_impuestos_internos),codigo_de_moneda,tipo_de_cambio,cantidad_de_alicuotas_de_iva,codigo_de_operacion,otros_tributos,fecha_de_vencimiento_de_pago FROM cbte WHERE tipo_de_comprobante is ? and punto_de_venta is ? and numero_de_comprobante like ?;""", (l["tipo_operacion"],l["punto_venta"],l["numero_operacion"]))

				query_cbte = set(cur.fetchall())
				cbte = Cbte()
				for q in query_cbte:
					# Delete the duplicates operations in cbte and insert one with the sum of all duplicates
					cbte.set_cbte_data(fecha_de_comprobante=q[0],tipo_de_comprobante=q[1],punto_de_venta=q[2],numero_de_comprobante=q[3],numero_de_comprobante_hasta=q[4],codigo_de_documento_del_comprador=q[5],numero_de_identificacion_del_comprador=q[6],apellido_y_nombre_o_denominacion_del_comprador=q[7],importe_total_de_la_operacion = str(q[8]).zfill(15),importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = str(q[9]).zfill(15),percepcion_a_no_categorizados = str(q[10]).zfill(15),importe_de_operaciones_exentas = str(q[11]).zfill(15),importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = str(q[12]).zfill(15),importe_de_percepciones_de_ingresos_brutos = str(q[13]).zfill(15),importe_de_percepciones_impuestos_municipales = str(q[14]).zfill(15),importe_impuestos_internos = str(q[15]).zfill(15),codigo_de_moneda=q[16],tipo_de_cambio=q[17],cantidad_de_alicuotas_de_iva=str(cont_alicuota),codigo_de_operacion=codigo_operacion,otros_tributos=q[20],fecha_de_vencimiento_de_pago=q[21])
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
			advance = "{:.2f}%".format(count_advance*100.0/total)
			if advance == "50.00%":
				print(advance)
			elif advance == "100.00%":
				print(advance)
		if len(self.cbte) > 0:
			self.cbte.clear()
		if len(self.alicuota) > 0:
			self.alicuota.clear()
		cur.execute("""DELETE FROM cbte WHERE fecha_de_comprobante is "";""")
		conn.commit()
		try:
			for x in cur.execute("""SELECT * FROM cbte;"""):
				if x[0] is None:
					continue
				else:
					self.cbte.append("".join(x))
			for x in cur.execute("""SELECT * FROM alicuotas;"""):
				self.alicuota.append("".join(x))
			self.write_file("ventas_cbte.txt", data_to_use="cbte")
			self.write_file("ventas_alicuotas.txt")
			print("Se quitaron los duplicados y se grabaron los archivos ventas_cbte.txt / ventas_alicuotas.txt")
		except Exception as e:
			print(e)
			raise e
		finally:
			conn.close()
		return
