# -*- coding: latin-1 -*-
# Con esta clase se procesara los archivos de exportación del citi compras


# Compras comprobantes

class Comprobante:

    def __init__(self):

        return

    def diccionario_comprobante(self,dato):
        self.dato = dato
        self.d = {
            "fecha_de_comprobante_o_fecha_de_oficializacion": self.dato[0:8],
            "tipo_de_comprobante": self.dato[8:11],
            "punto_de_venta": self.dato[11:16],
            "numero_de_comprobante": self.dato[16:36],
            "despacho_de_importacion": self.dato[36:52],
            "codigo_de_documento_del_vendedor": self.dato[52:54],
            "numero_de_identificacion_del_vendedor": self.dato[54:74],
            "apellido_y_nombre_o_denominacion_del_vendedor": self.dato[74:104],
            "importe_total_de_la_operacion": self.dato[104:119],
            "importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado": self.dato[119:134],
            "importe_de_operaciones_exentas": self.dato[134:149],
            "importe_de_percepciones_o_pagos_a_cuenta_del_impuesto_al_valor_agregado":self.dato[149:164],
            "importe_de_percepciones_o_pagos_a_cuenta_de_otros_impuestos_nacionales": self.dato[164:179],
            "importe_de_percepciones_de_ingresos_brutos": self.dato[179:194],
            "importe_de_percepciones_de_impuestos_municipales": self.dato[194:209],
            "importe_de_impuestos_internos": self.dato[209:224],
            "codigo_de_moneda": self.dato[224:227],
            "tipo_de_cambio": self.dato[227:237],
            "cantidad_de_alicuotas_de_iva": self.dato[237:238],
            "codigo_de_operacion": self.dato[238:239],
            "credito_fiscal_computable": self.dato[239:254],
            "otros_tributos": self.dato[254:269],
            "cuit_emisor_corredor": self.dato[269:280],
            "denominacion_del_emisor_corredor": self.dato[280:310],
            "iva_comision": self.dato[310:325]}
        return self.d

    def construir_linea_comprobante(self,dato):
        linea = (
            dato["fecha_de_comprobante_o_fecha_de_oficializacion"]+
            dato["tipo_de_comprobante"]+
            dato["punto_de_venta"]+
            dato["numero_de_comprobante"]+
            dato["despacho_de_importacion"]+
            dato["codigo_de_documento_del_vendedor"]+
            dato["numero_de_identificacion_del_vendedor"]+
            dato["apellido_y_nombre_o_denominacion_del_vendedor"]+
            dato["importe_total_de_la_operacion"]+
            dato["importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado"]+
            dato["importe_de_operaciones_exentas"]+
            dato["importe_de_percepciones_o_pagos_a_cuenta_del_impuesto_al_valor_agregado"]+
            dato["importe_de_percepciones_o_pagos_a_cuenta_de_otros_impuestos_nacionales"]+
            dato["importe_de_percepciones_de_ingresos_brutos"]+
            dato["importe_de_percepciones_de_impuestos_municipales"]+
            dato["importe_de_impuestos_internos"]+
            dato["codigo_de_moneda"]+
            dato["tipo_de_cambio"]+
            dato["cantidad_de_alicuotas_de_iva"]+
            dato["codigo_de_operacion"]+
            dato["credito_fiscal_computable"]+
            dato["otros_tributos"]+
            dato["cuit_emisor_corredor"]+
            dato["denominacion_del_emisor_corredor"]+
            dato["iva_comision"])
        return linea

    def pdv_nro_factura_cbte(self,linea):
        linea = linea
        if linea["punto_de_venta"] == "00000":
            linea["punto_de_venta"] = "00001"
        if linea["numero_de_comprobante"] == "00000000000000000000":
            linea["numero_de_comprobante"] = "00000000000000000001"
        return linea

    def tipo_de_comprobante(self,linea):

        if linea["tipo_de_comprobante"] == "006":
            linea["cantidad_de_alicuotas_de_iva"] = "0"
            return linea
        elif linea["tipo_de_comprobante"] == "011":
            linea["cantidad_de_alicuotas_de_iva"] = "0"
            return linea
        else:
            return linea

    def quitar_otros_proveedores_cbte(self,linea):

            if linea["apellido_y_nombre_o_denominacion_del_vendedor"] == "OTROS PROVEEDORES             ":
                return None
            else:
                return linea
            return

    def procesar_comprobante(self,archivo):
        self.archivo = archivo
        self.lista = []

        with open(self.archivo, encoding="latin-1", mode="r") as file:
            for linea in file:
                linea = self.diccionario_comprobante(linea)
                linea = self.quitar_otros_proveedores_cbte(linea)
                if linea == None:
                    continue
                else:
                    linea = self.pdv_nro_factura_cbte(linea)
                    linea = self.tipo_de_comprobante(linea)
                self.lista.append(self.construir_linea_comprobante(linea))
            return self.lista

# Compras alicuotas

# TODO Revisar toda la clase de alicuotas

class Alicuota:
    def __init__(self):
        return

    def diccionario_alicuota(self,dato):

        d = {
            "tipo_de_comprobante": dato[0:3],
            "punto_de_venta": dato[3:8],
            "numero_de_comprobante": dato[8:28],
            "codigo_de_documento_del_vendedor": dato[28:30],
            "numero_de_identificacion_del_vendedor": dato[30:50],
            "importe_neto_gravado": dato[50:65],
            "alicuota_de_iva": dato[65:69],
            "impuesto_liquidado": dato[69:84]}
        return d

    def construir_linea_alicuota(self,linea):
        l = (linea["tipo_de_comprobante"] +
             linea["punto_de_venta"] +
             linea["numero_de_comprobante"] +
             linea["codigo_de_documento_del_vendedor"] +
             linea["numero_de_identificacion_del_vendedor"] +
             linea["importe_neto_gravado"] +
             linea["alicuota_de_iva"] +
             linea["impuesto_liquidado"])
        return l

    # Debido a que en facturas B y C no se deben informar alicuotas se quitaran esas lineas del archivo
    def borrar_alicuota(self,linea):

        if linea["tipo_de_comprobante"] == "006":
            return None
        elif linea["tipo_de_comprobante"] == "011":
            return None
        else:
            return linea

    def quitar_otros_proveedores_ali(self,linea):

        if linea["numero_de_identificacion_del_vendedor"] == "00000000000000000001":
            return None
        else:
            return linea

    def pdv_nro_factura_ali(self,linea):

        if linea["punto_de_venta"] == "00000":
            linea["punto_de_venta"] = "00001"
        if linea["numero_de_comprobante"] == "00000000000000000000":
            linea["numero_de_comprobante"] = "00000000000000000001"
        return linea

    def correccion_impuesto_liquidado(self,linea):

        # Crear el calculo segun el codigo de IVA
        if int(linea["alicuota_de_iva"]) == 3:
            return linea
        elif int(linea["alicuota_de_iva"]) == 4:
            impuesto_liquidado = int(int(linea["importe_neto_gravado"]) * 0.105)
            linea["impuesto_liquidado"] = str(impuesto_liquidado).zfill(15)
            return linea
        elif int(linea["alicuota_de_iva"]) == 5:
            impuesto_liquidado = int(
                int(linea["importe_neto_gravado"]) * 0.21)
            linea["impuesto_liquidado"] = str(impuesto_liquidado).zfill(15)
            return linea
        elif int(linea["alicuota_de_iva"]) == 6:
            impuesto_liquidado = int(
                int(linea["importe_neto_gravado"]) * 0.27)
            linea["impuesto_liquidado"] = str(impuesto_liquidado).zfill(15)
            return linea
        elif int(linea["alicuota_de_iva"]) == 9:
            impuesto_liquidado = int(
                int(linea["importe_neto_gravado"]) * 0.025)
            linea["impuesto_liquidado"] = str(impuesto_liquidado).zfill(15)
            return linea
            
    def procesar_alicuota(self, archivo):

        self.archivo = archivo
        self.lista = []

        with open (self.archivo, mode="r", encoding="latin-1") as f:
            for linea in f:
                linea = self.diccionario_alicuota(linea)
                linea = self.borrar_alicuota(linea)
                linea = self.correccion_impuesto_liquidado(linea)
                if linea == None:
                    continue
                else:
                    linea = self.quitar_otros_proveedores_ali(linea)
                    if linea == None:
                        continue
                    else:
                        linea = self.pdv_nro_factura_ali(linea)
                
                self.lista.append(self.construir_linea_alicuota(linea))
        return self.lista

class Verificacion(Comprobante,Alicuota):

    def __init__(self):

        return

    # Funciones de la clase

    def comprobacion(self, lista_cbte, lista_alicuota):
        self.lista_cbte = lista_cbte
        self.lista_alicuota = lista_alicuota
        nueva_lista_cbte = []

        for linea_c in self.lista_cbte:
            linea_cbte = self.diccionario_comprobante(linea_c)
            comprobante = (
                linea_cbte["tipo_de_comprobante"] +
                linea_cbte["punto_de_venta"] +
                linea_cbte["numero_de_comprobante"])
            docproveedor = linea_cbte["numero_de_identificacion_del_vendedor"]

            # Contenedores de suma
            suma_importe_total = 0
            suma_credito_fiscal_computable = 0

            for linea_a in lista_alicuota:
                
                linea_alicuota = self.diccionario_alicuota(linea_a)
                _comprobante = (linea_alicuota["tipo_de_comprobante"] +
                                linea_alicuota["punto_de_venta"] +
                                linea_alicuota["numero_de_comprobante"])
                _docproveedor = linea_alicuota["numero_de_identificacion_del_vendedor"]

                if comprobante == _comprobante and docproveedor == _docproveedor:
                    suma_credito_fiscal_computable += int(
                        linea_alicuota["impuesto_liquidado"])
                    suma_importe_total += int(
                        linea_alicuota["importe_neto_gravado"]) + int(linea_alicuota["impuesto_liquidado"])

            suma_importe_total = (
                suma_importe_total +
                int(linea_cbte["importe_total_de_conceptos_que_no_integran_el_precio_neto_gravado"]) +
                int(linea_cbte["importe_de_operaciones_exentas"]) +
                int(linea_cbte["importe_de_percepciones_o_pagos_a_cuenta_del_impuesto_al_valor_agregado"]) +
                int(linea_cbte["importe_de_percepciones_o_pagos_a_cuenta_de_otros_impuestos_nacionales"]) +
                int(linea_cbte["importe_de_percepciones_de_ingresos_brutos"]) +
                int(linea_cbte["importe_de_percepciones_de_impuestos_municipales"]) +
                int(linea_cbte["importe_de_impuestos_internos"])
            )
            suma_importe_total = str(suma_importe_total)
            suma_credito_fiscal_computable = str(suma_credito_fiscal_computable)

            cred_fiscal_computable = suma_credito_fiscal_computable.rjust(15,"0")
            linea_cbte["credito_fiscal_computable"] = cred_fiscal_computable

            importe_total = suma_importe_total.rjust(15,"0")

            linea_cbte["importe_total_de_la_operacion"] = importe_total

            nueva_lista_cbte.append(self.construir_linea_comprobante(linea_cbte))

        return nueva_lista_cbte

