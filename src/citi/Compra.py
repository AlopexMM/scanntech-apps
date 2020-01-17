# -*- coding: utf-8 -*-

# Con esta clase se procesara los archivos de exportación del citi compras

# Compras comprobantes
""" "Fecha de comprobante o fecha de oficialización":[0:8]
    "Tipo de comprobante":[8:11]
    "Punto de venta":[11:16]
    "Número de comprobante":[16:36]
    "Despacho de importación":[36:52]
    "Código de documento del vendedor":[52:54]
    "Número de identificación del vendedor":[54:74]
    "Apellido y nombre o denominación del vendedor":[74:104]
    "Importe total de la operación":[104:119]
    "Importe total de conceptos que no integran el precio neto gravado":[119:134]
    "Importe de operaciones exentas":[134:149]
    "Importe de percepciones o pagos a cuenta del Impuesto al Valor Agregado":[149:164]
    "Importe de percepciones o pagos a cuenta de otros impuestos nacionales":[164:179]
    "Importe de percepciones de Ingresos Brutos":[179:194]
    "Importe de percepciones de Impuestos Municipales":[194:209]
    "Importe de Impuestos Internos":[209:224]
    "Código de moneda":[224:227]
    "Tipo de cambio":[227:237]
    "Cantidad de alícuotas de IVA":[237:238]
    "Código de operación":[238:239]
    "Crédito Fiscal Computable":[239:254]
    "Otros Tributos":[254:269]
    "CUIT emisor/corredor":[269:280]
    "Denominación del emisor/corredor":[280:310]
    "IVA comisión":[310:325]
"""

class comprobante:
    
    def __init__(self):
        return
    
    @staticmethod
    def _pdvnrofacturacbte(linea):
        inicio = linea[0:11]
        puntodeventa = linea[11:16]
        nrofactura = linea[16:36]
        final = linea[36:325]
        try:
           if puntodeventa == "00000":
              puntodeventa = "00001"
           if nrofactura == "00000000000000000000":
               nrofactura = "00000000000000000001"
           linea = inicio + puntodeventa + nrofactura + final
           return linea
        except Exception as e:
            #TODO: log de errores
            return


    @staticmethod
    def _tipodecomprobante(linea):
        inicio = linea[0:8]
        tipocomprobante = linea[8:11]
        cuerpo = linea[11:237]
        cantidadalicuotas = linea[237:238]
        final = linea[238:325]
        if tipocomprobante == "006":
            cantidadalicuotas = "0"
            linea = inicio + tipocomprobante + cuerpo + cantidadalicuotas + final
            return linea
        elif tipocomprobante == "011":
            cantidadalicuotas = "0"
            linea = inicio + tipocomprobante + cuerpo + cantidadalicuotas + final
            return linea
        else:
            return linea


    @staticmethod
    def _quitarotrosproveedorescbte(linea):
        otrosproveedores = linea[74:104]
        try:
            if otrosproveedores == "OTROS PROVEEDORES             ":
                return None
            else:
                return linea
        except Exception as e:
            #TODO: log de errores
            return

    def procesar_comprobante(self, archivo):
        self.archivo = archivo
        self.lista = []

        with open(self.archivo, encoding="latin-1", mode="r") as file:
            for linea in file:
                linea = comprobante._quitarotrosproveedorescbte(linea)
                if linea == None:
                    continue
                else:
                    linea = comprobante._pdvnrofacturacbte(linea)
                    linea = comprobante._tipodecomprobante(linea)
                self.lista.append(linea + '\n')
            return self.lista

# Compras alicuotas
""" "Tipo de comprobante":[0:3]
    "Punto de venta":[3:8]
    "Número de comprobante":[8:28]
    "Código de documento del vendedor":[28:30]
    "Número de identificación del vendedor":[30:50]
    "Importe neto gravado":[50:65]
    "Alícuota de IVA":[65:69]
    "Impuesto liquidado":[69:84]
"""

class alicuota:
    def __init__(self):
        return
    
    # Debido a que en facturas B y C no se deben informar alicuotas se quitaran esas lineas del archivo

    @staticmethod
    def _borraralicuota(linea):
        tipofac = linea[0:3]
        if tipofac == "006":
            return None
        elif tipofac == "011":
            return None
        else:
            return linea

    @staticmethod
    def _quitarotrosproveedoresali(linea):
        docproveedor = linea[30:50]
        if docproveedor == "00000000000000000001":
            return None
        else:
            return linea

    @staticmethod
    def _pdvnrofacturaali(linea):
        inicio = linea[0:3]
        puntodeventa = linea[3:8]
        nrofactura = linea[8:28]
        final = linea[28:84]
        if puntodeventa == "00000":
            puntodeventa = "00001"
        if nrofactura == "00000000000000000000":
            nrofactura = "00000000000000000001"
        linea = inicio + puntodeventa + nrofactura + final
        return linea

    def procesar_alicuota(self, archivo):
        self.archivo = archivo
        self.lista = []

        with open (self.archivo, mode="r", encoding="latin-1") as f:
            for linea in f:
                linea = alicuota._borraralicuota(linea)
                if linea == None:
                    continue
                else:
                    linea = alicuota._quitarotrosproveedoresali(linea)
                    if linea == None:
                        continue
                    else:
                        linea = alicuota._pdvnrofacturaali(linea)    
                self.lista.append(linea + '\n')
        return self.lista

class verificacion:
    
    def __init__(self):
        return

    # Funciones de la clase

    def comprobacion(self, lista_cbte, lista_alicuota):
        self.lista_cbte = lista_cbte
        self.lista_alicuota = lista_alicuota
        nueva_listacbte = []


        for linea in self.lista_cbte:
            inicio = linea[0:8]
            comprobante = linea[8:36]
            importaciontipodoc = linea[36:54]
            docproveedor = linea[54:74]
            nombreprov = linea[74:104]
            importetotal = linea[104:119]
            totalnetonogravado = linea[119:134]
            operacionesexentas = linea[134:149]
            importeimpvaloragregado = linea[149:164]
            impuestosnacionales = linea[164:179]
            percepcionesiibb = linea[179:194]
            impmunicipales = linea[194:209]
            impint = linea[209:224]
            codmoneda = linea[224:227]
            tipodecambio = linea[227:237]
            cantaliiva = linea[237:238]
            codoperacion = linea[238:239]
            credfiscalcomputable = linea[239:254]
            final = linea[254:325]
            suma_importetotal = 0
            suma_creditofiscalcomputable = 0
            
            for linea1 in lista_alicuota:
                _comprobante = linea1[0:28]
                _tipodoc = linea1[28:30]
                _docproveedor = linea1[30:50]
                _importenetogavado = linea1[50:65]
                _alicuotaiva = linea1[65:69]
                _impuestoliquidado = linea1[69:84]
                if comprobante == _comprobante and docproveedor == _docproveedor:
                    suma_creditofiscalcomputable = suma_creditofiscalcomputable + int(_impuestoliquidado)
                    suma_importetotal = suma_importetotal + int(_importenetogavado) + int(_impuestoliquidado)
            
            suma_importetotal = (
                suma_importetotal +
                int(totalnetonogravado) +
                int(operacionesexentas) +
                int(importeimpvaloragregado) +
                int(impuestosnacionales) +
                int(percepcionesiibb) +
                int(impmunicipales) +
                int(impint)
            )
            suma_importetotal = str(suma_importetotal)
            suma_creditofiscalcomputable = str(suma_creditofiscalcomputable)
            credfiscalcomputable = suma_creditofiscalcomputable.rjust(15,"0")
            importetotal = suma_importetotal.rjust(15,"0")

            nueva_listacbte.append(
                inicio +
                comprobante +
                importaciontipodoc +
                docproveedor +
                nombreprov +
                importetotal +
                totalnetonogravado +
                operacionesexentas +
                importeimpvaloragregado +
                impuestosnacionales +
                percepcionesiibb +
                impmunicipales +
                impint +
                codmoneda +
                tipodecambio +
                cantaliiva +
                codoperacion +
                credfiscalcomputable +
                final +
                "\n"
            )

        return nueva_listacbte

