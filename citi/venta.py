# -*- coding: latin-1 -*-
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
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

from sqlalchemy.sql.expression import null

Base = declarative_base()
from typing import Generator
from openpyxl import Workbook
import os
import sys

class Cbte(Base):
    """Cbte object for line_cbtebase"""

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
            id_extra:{self.id_extra!r},
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
            fecha_de_vencimiento_de_pago = {self.fecha_de_vencimiento_de_pago!r}
            )"""
        return message

class Alicuota(Base):
    """
    Alicuota object for line_cbtebase
    """
    __tablename__ = "ventas_alicuotas"

    id = Column(Integer,primary_key=True)
    id_extra = Column(String(28),nullable=False)
    id_alicuota = Column(String,nullable=False)
    tipo_de_comprobante = Column(String(3),nullable=False)
    punto_de_venta = Column(String(5),nullable=False)
    numero_de_comprobante = Column(String(20),nullable=False)
    importe_neto_gravado = Column(String(15),nullable=False)
    alicuota_de_iva = Column(String(4),nullable=False)
    impuesto_liquidado = Column(String(15),nullable=False)

    def __repr__(self):
        return f"""Alicuotas(
		id:{self.id!r},
		id_extra:{self.id_extra!r},
        id_alicuota: {self.id_alicuota!r},
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
    def __init__(self,cbte=None,alicuotas=None, ptv=-1, excel=False):
        try:
            self.engine = create_engine("sqlite+pysqlite:///:memory:")
            Base.metadata.create_all(self.engine)
            self.cbte_file = cbte
            self.alicuotas_file = alicuotas
            self.session = Session(self.engine)
            self.ptv = ptv
            self.excel = excel
        except Exception as e:
            print(e)
            raise e

    def _write_file(self):
        """Write a file in the current location"""
        try:
            data_c = self.session.query(Cbte).order_by(Cbte.id_extra).all()
            data_a = self.session.query(Alicuota).order_by(Alicuota.id_extra).all()
            if self.excel == False:
                with open("ventas_cbte.txt", mode="w", encoding="latin-1",newline="\r\n") as fc:
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

                with open("ventas_alicuotas.txt", "w", encoding="latin-1", newline="\r\n") as fa:
                    for a in data_a:
                        linea = a.tipo_de_comprobante + \
                            a.punto_de_venta + \
                            a.numero_de_comprobante + \
                            a.importe_neto_gravado + \
                            a.alicuota_de_iva + \
                            a.impuesto_liquidado + \
                            "\n"
                        fa.write(linea)
            else:
                wb = Workbook()
                dest_filename = "citi_ventas.xlsx"
                ws1 = wb.active
                ws1.title = "Cbte"
                ws1.append([
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
                    "fecha_de_vencimiento_de_pago"])
                for c in data_c:
                    ws1.append([
                        c.fecha_de_comprobante,
                        c.tipo_de_comprobante,
                        c.punto_de_venta,
                        c.numero_de_comprobante,
                        c.numero_de_comprobante_hasta,
                        c.codigo_de_documento_del_comprador,
                        c.numero_de_identificacion_del_comprador,
                        c.apellido_y_nombre_o_denominacion_del_comprador,
                        float(f"{int(c.importe_total_de_la_operacion[:-2])}.{c.importe_total_de_la_operacion[-2:]}"),
                        float(f"{int(c.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado[:-2])}.{c.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado[-2:]}"),
                        float(f"{int(c.percepcion_a_no_categorizados[:-2])}.{c.percepcion_a_no_categorizados[-2:]}"),
                        float(f"{int(c.importe_de_operaciones_exentas[:-2])}.{c.importe_de_operaciones_exentas[-2:]}"),
                        float(f"{int(c.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales[:-2])}.{c.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales[-2:]}"),
                        float(f"{int(c.importe_de_percepciones_de_ingresos_brutos[:-2])}.{c.importe_de_percepciones_de_ingresos_brutos[-2:]}"),
                        float(f"{int(c.importe_de_percepciones_impuestos_municipales[:-2])}.{c.importe_de_percepciones_impuestos_municipales[-2:]}"),
                        float(f"{int(c.importe_impuestos_internos[:-2])}.{c.importe_impuestos_internos[-2:]}"),
                        c.codigo_de_moneda,
                        c.tipo_de_cambio,
                        c.cantidad_de_alicuotas_de_iva,
                        c.codigo_de_operacion,
                        c.otros_tributos,
                        c.fecha_de_vencimiento_de_pago])
                ws2 = wb.create_sheet(title="Alicuotas")
                ws2.append([
                        "tipo_de_comprobante",
                        "punto_de_venta",
                        "numero_de_comprobante",
                        "importe_neto_gravado",
                        "alicuota_de_iva",
                        "impuesto_liquidado"])
                for a in data_a:
                    ws2.append([
                        a.tipo_de_comprobante,
                        a.punto_de_venta,
                        a.numero_de_comprobante,
                        float(f"{int(a.importe_neto_gravado[:-2])}.{a.importe_neto_gravado[-2:]}"),
                        a.alicuota_de_iva,
                        float(f"{int(a.impuesto_liquidado[:-2])}.{a.impuesto_liquidado[-2:]}")])
                wb.save(filename=dest_filename)
        except Exception as e:
            print(e)
            raise e

    def _process_cbte_and_alicuota(self):
        """Process cbte and alicuota
           This verified if the number of operation and until operation
        """
        try:
            with open(self.cbte_file,mode="r",encoding="latin-1") as f:
                for line_cbte in f.readlines():
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
                    self.session.add(cbte)
            with open(self.alicuotas_file,mode="r",encoding="latin-1") as f:
                for line_alicuota in f.readlines():
                    alicuota = Alicuota(
                        id_extra = line_alicuota[0:28],
                        id_alicuota = line_alicuota[0:28]+line_alicuota[43:47],
                        tipo_de_comprobante = line_alicuota[0:3],
                        punto_de_venta = line_alicuota[3:8],
                        numero_de_comprobante = line_alicuota[8:28],
                        importe_neto_gravado = line_alicuota[28:43],
                        alicuota_de_iva = line_alicuota[43:47],
                        impuesto_liquidado = line_alicuota[47:62],
                    )
                    self.session.add(alicuota)
            self.session.flush()
            self.session.commit()
        except FileNotFoundError:
           print("No se encontro algunos de los archivos")
           sys.exit(0)
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
        add_alicuota = alicuota[0]
        for a in range(1,len(alicuota)):
            al = alicuota[a]
            add_alicuota.importe_neto_gravado = str(sum(
                [
                    int(add_alicuota.importe_neto_gravado),
                    int(al.importe_neto_gravado)
                ]
            )
            ).zfill(15)
            add_alicuota.impuesto_liquidado = str(sum(
                [
                    int(add_alicuota.impuesto_liquidado),
                    int(al.impuesto_liquidado)
                ]
            )
            ).zfill(15)
            self.session.delete(alicuota[a])
        self.session.flush()

        return

    def _merge_cbte(self,cbte):
        """Merge cbte that are duplicates"""
        add_cbte = cbte[0]
        for i in range(1,len(cbte)):
            c = cbte[i]
            add_cbte.importe_total_de_la_operacion = str(
                sum(
                    [
                        int(add_cbte.importe_total_de_la_operacion),
                        int(c.importe_total_de_la_operacion)
                    ]
                )
            ).zfill(15)
            add_cbte.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado = str(
                sum(
                    [
                        int(add_cbte.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado),
                        int(c.importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado)
                    ]
                )
            ).zfill(15)
            add_cbte.percepcion_a_no_categorizados = str(
                sum(
                    [
                        int(add_cbte.percepcion_a_no_categorizados),
                        int(c.percepcion_a_no_categorizados)
                    ]
                )
            ).zfill(15)
            add_cbte.importe_de_operaciones_exentas = str(
                sum(
                    [
                        int(add_cbte.importe_de_operaciones_exentas),
                        int(c.importe_de_operaciones_exentas)
                    ]
                )
            ).zfill(15)
            add_cbte.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales = str(
                sum(
                    [
                        int(add_cbte.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales),
                        int(c.importe_de_percepciones_o_pagos_a_cuenta_de_impuestos_nacionales)
                    ]
                )
            ).zfill(15)
            add_cbte.importe_de_percepciones_de_ingresos_brutos = str(
                sum(
                    [
                        int(add_cbte.importe_de_percepciones_de_ingresos_brutos),
                        int(c.importe_de_percepciones_de_ingresos_brutos)
                    ]
                )
            ).zfill(15)
            add_cbte.importe_de_percepciones_impuestos_municipales = str(
                sum(
                    [
                        int(add_cbte.importe_de_percepciones_impuestos_municipales),
                        int(c.importe_de_percepciones_impuestos_municipales)
                    ]
                )
            ).zfill(15)
            add_cbte.importe_impuestos_internos = str(
                sum(
                    [
                        int(add_cbte.importe_impuestos_internos),
                        int(c.importe_impuestos_internos)
                    ]
                )
            ).zfill(15)
            self.session.delete(c)
        self.session.flush()
        return

    def _merge_duplicates_in_cbte_and_alicuotas(self):
        cbtes = self.session.query(Cbte.id_extra).all()
        alicuotas = self.session.query(Alicuota.id_alicuota).all()
        set_cbtes_id = set([c[0] for c in cbtes])
        set_alicuotas_id = set([a[0] for a in alicuotas])

        for id in set_cbtes_id:
            c = self.session.query(Cbte).filter(id == Cbte.id_extra).all()
            if len(c) > 1:
                self._merge_cbte(c)
        for id in set_alicuotas_id:
            a = self.session.query(Alicuota).filter(id == Alicuota.id_alicuota).all()
            if len(a) > 1:
                self._merge_alicuotas(a)
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

    def _delete_ptv(self):
        ptv = str(self.ptv).zfill(5)
        (self.session.query(Cbte).filter(Cbte.punto_de_venta == ptv)
         .delete(synchronize_session=False))
        (self.session.query(Alicuota).filter(Alicuota.punto_de_venta == ptv)
         .delete(synchronize_session=False))
        self.session.flush()
        self.session.commit()

        return


    def run(self):
        """Execute all the functions necesary"""

        # Create and add data to database in memory
        self._process_cbte_and_alicuota()

        if self.excel == True:
            self._write_file()
            print("Se grabaron los mismos en citi_ventas.xlsx.")
        else:
            # Delete alicuotas
            #self._delete_alicuotas_without_cbte()

            # Merge duplicates in cbte and alicuotas
            self._merge_duplicates_in_cbte_and_alicuotas()

            # Audit the amount of alicuotas
            self._audit_amount_alicuotas()

            # Check amounts in cbte
            self._check_amounts_in_cbte()

            # Delete PTV
            if self.ptv != -1:
                self._delete_ptv()

            print("Se limpio los datos del reporte.")
            # Write files
            self._write_file()
            print("Se grabaron en ventas_cbte.txt y ventas_alicuotas.txt")
        
        
