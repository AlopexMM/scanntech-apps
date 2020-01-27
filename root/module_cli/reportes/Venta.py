# -*- coding: latin-1 -*-

''' En esta clase se puede encontrar las funciones que modifican el archivo de 
comprobantes'''




# Verificadores

def verificador_cuit(cuit):

    # Cortamos la cadena de 20 caracteres para que me queden los ultimos 11
    # y poder verificar el CUIT
    
    cuit = cuit[9:20]
    
    # Base para la multiplicacion
    
    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    aux = 0
    for i in range(10):
        aux += int(cuit[i]) * base[i]
    aux = 11 - (aux % 11)
    if aux == 11:
        aux = 0
    elif aux == 10:
        aux = 9
    if int(cuit[10]) == aux:
        return True
    else:
        return False

# Funciones propias de la clase
# Funciones que pueden ser utilizadas por ambas clases
        
def remplazo_tipo_operacion(data, comprobantes=False, alicuotas=False):
    if comprobantes:

        # Remplazo el tipo de comprobante en los datos

        if (data.get('tipo de comprobante') == '006'):
            data['tipo de comprobante']='082'
        elif (data.get('tipo de comprobante') == '001'):
            data['tipo de comprobante']= '081'
        elif (data.get('tipo de comprobante') == '008'):
            data['tipo de comprobante']='113'
        elif (data.get('tipo de comprobante') == '003'):
            data['tipo de comprobante']='112'
        return data

    elif alicuotas:
        
        # Remplazo el tipo de comprobante en los datos incorrectos

        if (data.get('tipo de comprobante') == '006'):
            data['tipo de comprobante'] = '082'
        elif (data.get('tipo de comprobante') == '001'):
            data['tipo de comprobante'] = '081'
        elif (data.get('tipo de comprobante') == '008'):
            data['tipo de comprobante'] = '113'
        elif (data.get('tipo de comprobante') == '003'):
            data['tipo de comprobante'] = '112'
        
        return data
    else:
        return data

# Funciones que pertenecen solo a comprobantes

def desde_hasta(data):
        
    if (data.get('numero de comprobante') != data.get('numero de comprobante hasta')):
        data['numero de comprobante hasta'] = data['numero de comprobante']
        return data
    else:
        return data

def verificar_comprador(data):

    # Se verifica que el cuit y los datos del cliente cargados
    # en la venta esten bien
    # -----------------------------------------------------------------
    # Se verifica el CUIT y si el monto es mayor o menor que 1000 pesos

    resultado_cuit = verificador_cuit(
        data.get('numero de identificacion del comprador')
        )
    
    # El nro de comprador si aparece no es valido por lo que se lo cambia por 
    # 80 que es para facturas

    if (data.get('codigo de documento del comprador') == '87'):
        data['codigo de documento del comprador'] = '80'
    
    # Verificamos que este bien para para las NOTAS DE CREDITO y DEBITO

    if (data.get('tipo de comprobante') == '113'):
        data['codigo de documento del comprador'] = '99'


    # Si el nro de comprador es 99 se analiza si el monto es mayor o menor de 1000 pesos
    
    if (data.get('codigo de documento del comprador') == '99'):
        if (int(data.get('importe total de la operacion')) < 1000):
            data['numero de identificacion del comprador'] = '00000000000000000000'
            data['apellido y nombre o denominacion del comprador'] = 'CONSUMIDOR FINAL              '
        elif (int(data.get('importe total de la operacion')) >= 1000):
            data['numero de identificacion del comprador'] = '00000000000000000000'
            data['apellido y nombre o denominacion del comprador'] = 'VENTA GLOBAL DIARIA           '
    elif (resultado_cuit == False):
        if (int(data.get('importe total de la operacion')) < 1000):
            data['codigo de documento del comprador'] = '99'
            data['numero de identificacion del comprador'] = '00000000000000000000'
            data['apellido y nombre o denominacion del comprador'] = 'CONSUMIDOR FINAL              '
        elif (int(data.get('importe total de la operacion')) >= 1000):
            data['codigo de documento del comprador'] = '99'
            data['numero de identificacion del comprador'] = '00000000000000000000'
            data['apellido y nombre o denominacion del comprador'] = 'VENTA GLOBAL DIARIA           '
    
    return data

def revision_alicuotasAlicuotas(data):
    
    # Se verifica que el codigo de alicuota no sea el de No gavado de ser asi
    # se cambia por el de 0%

    if data.get('alicuota de iva') == '0001':
        data['alicuota de iva'] = '0003'
    
    return data

# Funciones que pertenecen solo a Alicuotas

# Clases

class comprobante:

    def __init__(self):
        return
    
    def campos_comprobante(self, linea):

        # Formato de comprobantes segun AFIP
        # Tomamos la linea y devolvemos un diccionario con todas las partes para una
        # facil revisión de los datos

        campos_cbte = {
            'fecha de comprobante': linea[0:8],
            'tipo de comprobante': linea[8:11],
            'punto de venta': linea[11:16],
            'numero de comprobante': linea[16:36],
            'numero de comprobante hasta': linea[36:56],
            'codigo de documento del comprador': linea[56:58],
            'numero de identificacion del comprador': linea[58:78],
            'apellido y nombre o denominacion del comprador': linea[78:108],
            'importe total de la operacion': linea[108:123],
            'importe total de conceptos que no integran el precio neto gravado': linea[123:138],
            'percepcion a no categorizados': linea[138:153],
            'importe de operaciones exentas': linea[153:168],
            'importe de percepciones o pagos a cuenta de impuestos nacionales': linea[168:183],
            'importe de percepciones de ingresos brutos': linea[183:198],
            'importe de percepciones impuestos municipales': linea[198:213],
            'importe impuestos internos': linea[213:228],
            'codigo de moneda': linea[228:231],
            'tipo de cambio': linea[231:241],
            'cantidad de alicuotas de iva': linea[241:242],
            'codigo de operacion': linea[242:243],
            'otros tributos': linea[243:258],
            'fecha de vencimiento de pago': linea[258:266]
        }

        return campos_cbte

    # Construimos la linea en el orden correcto para evitar errores en otras partes del programa
    
    def construir_linea_comprobante(self, data):
        linea = data['fecha de comprobante'] + \
        data['tipo de comprobante'] + \
        data['punto de venta'] + \
        data['numero de comprobante'] + \
        data['numero de comprobante hasta'] + \
        data['codigo de documento del comprador'] + \
        data['numero de identificacion del comprador'] + \
        data['apellido y nombre o denominacion del comprador'] + \
        data['importe total de la operacion'] + \
        data['importe total de conceptos que no integran el precio neto gravado'] + \
        data['percepcion a no categorizados'] + \
        data['importe de operaciones exentas'] + \
        data['importe de percepciones o pagos a cuenta de impuestos nacionales'] + \
        data['importe de percepciones de ingresos brutos'] + \
        data['importe de percepciones impuestos municipales'] + \
        data['importe impuestos internos'] + \
        data['codigo de moneda'] + \
        data['tipo de cambio'] + \
        data['cantidad de alicuotas de iva'] + \
        data['codigo de operacion'] + \
        data['otros tributos'] + \
        data['fecha de vencimiento de pago']

        return linea

    def procesamiento_comprobantes(self, archivo):
        nueva_lista = []
        try:
            with open(archivo, mode='r', encoding='latin-1') as lista:

                for linea in lista:
                    data = self.campos_comprobante(linea)
                    data = remplazo_tipo_operacion(data,comprobantes=True)
                    data = desde_hasta(data)
                    data = verificar_comprador(data)
                    nueva_lista.append(self.construir_linea_comprobante(data))

                return nueva_lista
        except Exception as error:
            print(error)
            return 

class alicuota:

    def __init__(self):
        return

    def campos_alicuotas(self, linea):

        # Formato que tienen las lineas de alicuotas
        campos_ali = {
            'tipo de comprobante': linea[0:3],
            'punto de venta': linea[3:8],
            'numero de comprobante': linea[8:28],
            'importe neto gravado': linea[28:43],
            'alicuota de iva': linea[43:47],
            'impuesto liquidado': linea[47:62]
        }

        return campos_ali
    
    def construir_linea_alicuota(self, data):
        linea = data['tipo de comprobante'] + \
        data['punto de venta'] + \
        data['numero de comprobante'] + \
        data['importe neto gravado'] + \
        data['alicuota de iva'] + \
        data['impuesto liquidado']

        return linea

    def procesamiento_alicuotas(self, archivo):
        nueva_lista = []
        try:    
            with open(archivo, mode='r', encoding='latin-1') as lista:

                for linea in lista:
                    data = self.campos_alicuotas(linea)
                    data = remplazo_tipo_operacion(data, alicuotas=True)
                    data = revision_alicuotasAlicuotas(data)
                    nueva_lista.append(self.construir_linea_alicuota(data))
                return nueva_lista
        except Exception as error:
            print(error)
            return 
