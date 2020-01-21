from reportes import Venta

# Funcion que devuelve un nro unico formado por valores que se encuentran
# en ambos reportes
def codigo_unico_cbte_alicuota(data):
    codigo_unico = data['tipo de comprobante'] + \
        data['punto de venta'] + \
        data['numero de comprobante']
    return codigo_unico

class verificaciones:
    def __init__(self):
        self.comprobantes = Venta.comprobante()
        self.alicuotas = Venta.alicuota()
        return
    
    def verificar_nro_alicuotas(self, cbte, alicuota):

        resultado = []
        
        
        for x in cbte:
            
            # Contador de lineas de alicuotas que se encuentran en alicuotas
            count_al = 0

            # Obtenemos un diccionario de los campos
            cbte_linea = self.comprobantes.campos_comprobante(x)

            # Creamos un valor unico para contar las cantidad de alicuotas que hay
            tmp_cbte = codigo_unico_cbte_alicuota(cbte_linea)

            for y in alicuota:
                
                # Obtenemos un diccionario de los campos
                alicuota_linea = self.alicuotas.campos_alicuotas(y)

                # Creamos un valor unico para contar las cantidad de alicuotas que hay
                tmp_alicuota = codigo_unico_cbte_alicuota(alicuota_linea)

                # Verificamos con los valores unicos obtenidos,
                # de tener igualdad se suma uno al contador
                if tmp_cbte == tmp_alicuota:
                    count_al = count_al + 1
                
                # Revisamos si hay IVA 0
                if alicuota_linea['alicuota de iva'] == '0003':
                    cbte_linea['codigo de operacion'] = 'N'

            # Terminamos de recorrer la lista y reemplazamos la cantidad de alicuotas por el monto de la cuenta
            cbte_linea['cantidad de alicuotas de iva'] = str(count_al)
            resultado.append(self.comprobantes.construir_linea_comprobante(cbte_linea))
        return resultado


    def verificar_monto_final(self, cbte, alicuota):
        lista = []
        
        # Revisamos cada linea de comprobantes
        for x in cbte:

            # Obtenemos el diccionario de los comprobantes para trabajarlo
            cbte_linea = self.comprobantes.campos_comprobante(x)

            # Armamos un codigo unico de operacion en comprobantes
            x_operacion = codigo_unico_cbte_alicuota(cbte_linea)

            # Declaramos la variable donde se van a acumular el IVA y el neto
            # que encontremos en alicuotas y coincidan los codigos unicos
            # de la linea de comprobante y la linea de alicuota
            y_monto_x = 0

            for y in alicuota:

                # Obtenemos el diccionario de las alicuotas para trabajarlo
                alicuota_linea = self.alicuotas.campos_alicuotas(y)

                # Armamos un codigo unico 
                y_operation = codigo_unico_cbte_alicuota(alicuota_linea)

                # Importes que se necesitan obtener
                y_monto_sin_impuesto = alicuota_linea['importe neto gravado']
                y_iva = alicuota_linea['impuesto liquidado']

                # Si los codigos unicos coinciden sumarizamos los montos del IVA y el neto
                if x_operacion == y_operation:
                    y_monto_x = (y_monto_x + int(y_monto_sin_impuesto) + int(y_iva))

            # Obtenemos el monto real en y_mas_x
            y_mas_x = (
                y_monto_x +
                int(cbte_linea['importe total de conceptos que no integran el precio neto gravado']) +
                int(cbte_linea['percepcion a no categorizados']) +
                int(cbte_linea['importe de operaciones exentas']) +
                int(cbte_linea['importe de percepciones o pagos a cuenta de impuestos nacionales']) +
                int(cbte_linea['importe de percepciones de ingresos brutos']) +
                int(cbte_linea['importe de percepciones impuestos municipales']) +
                int(cbte_linea['importe impuestos internos'])
                )

            # Modificamos el monto total de la operacion para que coincida con lo reportado
            y_mas_x = str(y_mas_x).rjust(15, "0")
            
            if cbte_linea['importe total de la operacion'] != y_mas_x:
                cbte_linea['importe total de la operacion'] = y_mas_x

            # Se forma la linea final
            lista.append(self.comprobantes.construir_linea_comprobante(cbte_linea))

        return lista

    def verificar_comprobantes_cero(self, cbte, alicuotas):

        lista_cbte = []
        alicuotas_a_quitar = []
        self.lista_alicuotas = alicuotas

        for x in cbte:

            cbte_linea = self.comprobantes.campos_comprobante(x)

            if int(cbte_linea['importe total de la operacion']) == 0:
                operacion = cbte_linea['tipo de comprobante'] + \
                    cbte_linea['punto de venta'] + \
                    cbte_linea['numero de comprobante']
                alicuotas_a_quitar.append(operacion)
            else:
                lista_cbte.append(self.comprobantes.construir_linea_comprobante(cbte_linea))

        for x in alicuotas:            
            alicuota_linea = self.alicuotas.campos_alicuotas(x)

            operacion_alicuota = alicuota_linea['tipo de comprobante'] + \
                alicuota_linea['punto de venta'] + \
                alicuota_linea['numero de comprobante']

            for y in alicuotas_a_quitar:
                if operacion_alicuota == y:
                    #print("{0} encontro este y se debe remover {1}".format(y,x))
                    self.lista_alicuotas.remove(x)


        return [lista_cbte, self.lista_alicuotas]
