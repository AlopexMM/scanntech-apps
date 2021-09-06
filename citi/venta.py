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

    def _file_generator(self, file) -> Generator:
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

    def _process_cbte_and_alicuota(self):
        """Process cbte and alicuota
           This verified if the number of operation and until operation
        """
        try:
            while True:
                line_cbte = next(self.cbte_file)
                cbte = Cbte(
                    id_extra = line_cbte[8:36],
                    fecha_de_comprobante = line_cbte[0:8],
                    tipo_de_comprobante = line_cbte[8:11],
                    punto_de_venta = line_cbte[11:16],
                    numero_de_comprobante = line_cbte[16:36],
                    numero_de_comprobante_hasta = line_cbte[36:56],
                    codigo_de_documento_del_comprador = line_cbte[56:58],
                    numero_de_identificacion_del_comprador = line_cbte[58:78].replace("-","").zfill(20),
                    apellido_y_nombre_o_denominacion_del_comprador = line_cbte[78:108],
                    importe_total_de_la_operacion = line_cbte[108:123],
                    importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = line_cbte[123:138],
                    percepcion_a_no_categorizados = line_cbte[138:153],
                    importe_de_operaciones_exentas = line_cbte[153:168],
                    importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = line_cbte[168:183],
                    importe_de_percepciones_de_ingresos_brutos = line_cbte[183:198],
                    importe_de_percepciones_impuestos_municipales = line_cbte[198:213],
                    importe_impuestos_internos = line_cbte[213:228],
                    codigo_de_moneda = line_cbte[228:231],
                    tipo_de_cambio = line_cbte[231:241],
                    cantidad_de_alicuotas_de_iva = line_cbte[241:242],
                    codigo_de_operacion = line_cbte[242:243],
                    otros_tributos = line_cbte[243:258],
                    fecha_de_vencimiento_de_pago = line_cbte[258:266],
                )
                line_alicuota = next(self.alicuotas_file)
                alicuota = Alicuota(
                    id_extra = line_cbte[8:36],
                    tipo_de_comprobante = line_alicuota[0:3],
                    punto_de_venta = line_alicuota[3:8],
                    numero_de_comprobante = line_alicuota[8:28],
                    importe_neto_gravado = line_alicuota[28:43],
                    alicuota_de_iva = line_alicuota[43:47],
                    impuesto_liquidado = line_alicuota[47:62],
                )
                self.session.add(cbte)
                self.session.add(alicuota)
                self.session.flush()
            self.session.commit()
        except StopIteration:
            print("Se procesaron los datos correctamente.")

