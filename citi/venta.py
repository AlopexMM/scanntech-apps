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
        try:
            self.engine = create_engine("sqlite+pysqlite:///:memory:")
            Base.metadata.create_all(self.engine)
            self.cbte_file = self._file_generator(cbte)
            self.alicuotas_file = self._file_generator(alicuotas)
            self.session = Session(self.engine)
        except Exception as e:
            print(e)
            raise e
        self.cbte_template = {
            "id_extra":"",
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
            "id_extra": "",
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

    def _write_file(self):
        """Write a file in the current location"""
        try:
            with open("ventas_cbte.txt", mode="a", encoding="latin-1",newline="\r\n") as fc:
                data_c = self.session.query(Cbte).all()
                for c in data_c:
                    linec = c.fecha_de_comprobante + \
                        c.tipo_de_comprobante + \
                        c.punto_de_venta + \
                        c.numero_de_comprobante + \
                        c.numero_de_comprobante_hasta + \
                        c.codigo_de_documento_del_comprador + \
                        c.numero_de_identificacion_del_comprador + \
                        c.apellido_y_nombre_o_denominacion_del_comprador + \
                        c.importe_total_de_la_operacion + \
                        c.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado + \
                        c.percepcion_a_no_categorizados + \
                        c.importe_de_operaciones_exentas + \
                        c.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales + \
                        c.importe_de_percepciones_de_ingresos_brutos + \
                        c.importe_de_percepciones_impuestos_municipales + \
                        c.importe_impuestos_internos + \
                        c.codigo_de_moneda + \
                        c.tipo_de_cambio + \
                        c.cantidad_de_alicuotas_de_iva + \
                        c.codigo_de_operacion + \
                        c.otros_tributos + \
                        c.fecha_de_vencimiento_de_pago + \
                        "\n"
                    fc.write(linec)
            with open("ventas_alicuotas.txt", "a", encoding="latin-1", newline="\r\n") as fa:
                data_a = self.session.query(Alicuota).all()
                for a in data_a:
                    linea = a.tipo_de_comprobante + \
                        a.punto_de_venta + \
                        a.numero_de_comprobante + \
                        a.importe_neto_gravado + \
                        a.alicuota_de_iva + \
                        a.impuesto_liquidado + \
                        "\n"
                    fa.write(linea)
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
            print("Se creo la base de datos correctamente.")

    def _delete_alicuotas_without_cbte(self):
        """Delete alicuotas without cbte"""
        alicuotas = self.session.query(Alicuota).all()
        for a in alicuotas:
            c = self.session.query(Cbte).filter(a.id_extra == Cbte.id_extra).all()
            if len(c) == 0:
                self.session.delete(a)
            self.session.flush()
        self.session.commit()
        print("Se eliminaron las alicuotas que no tienen comprobante.")
        return

    def _merge_alicuotas(self, alicuota):
        """Merge alicuotas duplicates"""
        alis = {
            "0003": { "flag":False, "a": self.alicuota_template },
            "0004":{ "flag":False, "a": self.alicuota_template },
            "0005":{ "flag":False, "a": self.alicuota_template }
        }

        for al in alicuota:
            alis[al.alicuota_de_iva]["a"]["id_extra"] = al.id_extra
            alis[al.alicuota_de_iva]["a"]["tipo_de_comprobante"] = al.tipo_de_comprobante
            alis[al.alicuota_de_iva]["a"]["punto_de_venta"] = al.punto_de_venta
            alis[al.alicuota_de_iva]["a"]["numero_de_comprobante"] = al.numero_de_comprobante
            alis[al.alicuota_de_iva]["a"]["importe_neto_gravado"] += int(al.importe_neto_gravado)
            alis[al.alicuota_de_iva]["a"]["alicuota_de_iva"] = al.alicuota_de_iva
            alis[al.alicuota_de_iva]["a"]["impuesto_liquidado"] += int(al.impuesto_liquidado)
            alis[al.alicuota_de_iva]["flag"] = True
            self.session.delete(al)
            self.session.flush()
        for ali in alis:
            if alis[ali]["flag"]:
                add_a = Alicuota(
                        id_extra = alis[ali]["a"]["id_extra"],
                        tipo_de_comprobante = alis[ali]["a"]["tipo_de_comprobante"],
                        punto_de_venta = alis[ali]["a"]["punto_de_venta"],
                        numero_de_comprobante = alis[ali]["a"]["numero_de_comprobante"],
                        importe_neto_gravado = str(alis[ali]["a"]["importe_neto_gravado"]).zfill(15),
                        alicuota_de_iva = alis[ali]["a"]["alicuota_de_iva"],
                        impuesto_liquidado = str(alis[ali]["a"]["impuesto_liquidado"]).zfill(15),
                    )
                self.session.add(add_a)
                self.session.flush()
        return

    def _merge_cbte(self,cbte):
        """Merge cbte that are duplicates"""
        add_cbte = self.cbte_template
        for c in cbte:
            add_cbte["id_extra"] = c.id_extra
            add_cbte["fecha_de_comprobante"] = c.fecha_de_comprobante
            add_cbte["tipo_de_comprobante"] = c.tipo_de_comprobante
            add_cbte["punto_de_venta"] = c.punto_de_venta
            add_cbte["numero_de_comprobante"] = c.numero_de_comprobante
            add_cbte["numero_de_comprobante_hasta"] = c.numero_de_comprobante_hasta
            add_cbte["codigo_de_documento_del_comprador"] = c.codigo_de_documento_del_comprador
            add_cbte["numero_de_identificacion_del_comprador"] = c.numero_de_identificacion_del_comprador
            add_cbte["apellido_y_nombre_o_denominacion_del_comprador"] = c.apellido_y_nombre_o_denominacion_del_comprador
            add_cbte["importe_total_de_la_operacion"] = int(c.importe_total_de_la_operacion)
            add_cbte["importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado"] = int(c.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado)
            add_cbte["percepcion_a_no_categorizados"] = int(c.percepcion_a_no_categorizados)
            add_cbte["importe_de_operaciones_exentas"] = int(c.importe_de_operaciones_exentas)
            add_cbte["importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales"] = int(c.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales)
            add_cbte["importe_de_percepciones_de_ingresos_brutos"] = int(c.importe_de_percepciones_de_ingresos_brutos)
            add_cbte["importe_de_percepciones_impuestos_municipales"] = int(c.importe_de_percepciones_impuestos_municipales)
            add_cbte["importe_impuestos_internos"] = int(c.importe_impuestos_internos)
            add_cbte["codigo_de_moneda"] = c.codigo_de_moneda
            add_cbte["tipo_de_cambio"] = c.tipo_de_cambio
            add_cbte["cantidad_de_alicuotas_de_iva"] = c.cantidad_de_alicuotas_de_iva
            add_cbte["codigo_de_operacion"] = c.codigo_de_operacion
            add_cbte["otros_tributos"] = c.otros_tributos
            add_cbte["fecha_de_vencimiento_de_pago"] = c.fecha_de_vencimiento_de_pago
            self.session.delete(c)
            self.session.flush()
        insert_cbte = Cbte (
                    id_extra = add_cbte["id_extra"],
                    fecha_de_comprobante = add_cbte["fecha_de_comprobante"],
                    tipo_de_comprobante = add_cbte["tipo_de_comprobante"],
                    punto_de_venta = add_cbte["punto_de_venta"],
                    numero_de_comprobante = add_cbte["numero_de_comprobante"],
                    numero_de_comprobante_hasta = add_cbte["numero_de_comprobante_hasta"],
                    codigo_de_documento_del_comprador = add_cbte["codigo_de_documento_del_comprador"],
                    numero_de_identificacion_del_comprador = add_cbte["numero_de_identificacion_del_comprador"],
                    apellido_y_nombre_o_denominacion_del_comprador = add_cbte["apellido_y_nombre_o_denominacion_del_comprador"],
                    importe_total_de_la_operacion = str(add_cbte["importe_total_de_la_operacion"]).zfill(15),
                    importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = str(add_cbte["importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado"]).zfill(15),
                    percepcion_a_no_categorizados = str(add_cbte["percepcion_a_no_categorizados"]).zfill(15),
                    importe_de_operaciones_exentas = str(add_cbte["importe_de_operaciones_exentas"]).zfill(15),
                    importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = str(add_cbte["importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales"]).zfill(15),
                    importe_de_percepciones_de_ingresos_brutos = str(add_cbte["importe_de_percepciones_de_ingresos_brutos"]).zfill(15),
                    importe_de_percepciones_impuestos_municipales = str(add_cbte["importe_de_percepciones_impuestos_municipales"]).zfill(15),
                    importe_impuestos_internos = str(add_cbte["importe_impuestos_internos"]).zfill(15),
                    codigo_de_moneda = add_cbte["codigo_de_moneda"],
                    tipo_de_cambio = add_cbte["tipo_de_cambio"],
                    cantidad_de_alicuotas_de_iva = add_cbte["cantidad_de_alicuotas_de_iva"],
                    codigo_de_operacion = add_cbte["codigo_de_operacion"],
                    otros_tributos = add_cbte["otros_tributos"],
                    fecha_de_vencimiento_de_pago = add_cbte["fecha_de_vencimiento_de_pago"],
                )
        self.session.add(insert_cbte)
        self.session.flush()
        return

    def _merge_duplicates_in_cbte_and_alicuotas(self):
        return_flag = True

        while return_flag:
            cbtes = self.session.query(Cbte).all()
            alicuotas = self.session.query(Alicuota).all()

            for cbte in cbtes:
                c = self.session.query(Cbte).filter(Cbte.id_extra == cbte.id_extra).all()
                if len(c) > 1:
                    # Merge the totals
                    self._merge_cbte(c)
                    return_flag = True
                else:
                    return_flag = False
            for alicuota in alicuotas:
                a = self.session.query(Alicuota).filter(Alicuota.id_extra == alicuota.id_extra).all()
                if len(a) > 1:
                    # Merge the totals
                    self._merge_alicuotas(a)
                    return_flag = True
                else:
                    return_flag = False
        self.session.commit()
        print("Se procesaron los documentos duplicados.")
        return

    def _audit_amount_alicuotas(self):
        cbtes = self.session.query(Cbte).all()
        for cbte in cbtes:
            alicuotas = self.session.query(Alicuota).filter(cbte.id_extra == Alicuota.id_extra).all()
            for alicuota in alicuotas:
                if alicuota.alicuota_de_iva == "0003":
                    cbte.codigo_de_operacion = "N"
            cbte.cantidad_de_alicuotas_de_iva = str(len(alicuotas))
            self.session.flush()
        self.session.commit()
        return

    def _check_amounts_in_cbte(self):
        cbtes = self.session.query(Cbte).all()
        for cbte in cbtes:
            alicuotas = self.session.query(Alicuota).filter(cbte.id_extra == Alicuota.id_extra).all()
            total_amount = 0
            for alicuota in alicuotas:
                total_amount += sum(
                    [
                        int(alicuota.importe_neto_gravado),
                        int(alicuota.impuesto_liquidado)
                    ]
                )
            total_amount += sum(
                [
                    int(cbte.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado),
                    int(cbte.percepcion_a_no_categorizados),
                    int(cbte.importe_de_operaciones_exentas),
                    int(cbte.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales),
                    int(cbte.importe_de_percepciones_de_ingresos_brutos),
                    int(cbte.importe_de_percepciones_impuestos_municipales),
                    int(cbte.importe_impuestos_internos)
                ]
            )
            cbte.importe_total_de_la_operacion = str(total_amount).zfill(15)
            self.session.flush()
        self.session.commit()
        return


    def run(self):
        """Execute all the functions necesary"""

        # Create and add data to database in memory
        self._process_cbte_and_alicuota()

        # Delete alicuotas
        self._delete_alicuotas_without_cbte()

        # Merge duplicates in cbte and alicuotas
        self._merge_duplicates_in_cbte_and_alicuotas()

        # Audit the amount of alicuotas
        self._audit_amount_alicuotas()

        # Check amounts in cbte
        self._check_amounts_in_cbte()

        # Write files
        self._write_file()

        print("Se limpio los datos del reporte y se grabaron los mismos.")
