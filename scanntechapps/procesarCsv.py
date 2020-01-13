from sys import argv

def cuitMod(texto):
    cabeza = texto[0:2]
    cuerpo = texto[2:10]
    cola = texto[10:]
    texto = cabeza + "-" + cuerpo + "-" + cola
    return texto

def numeroSucursalMod(texto):
    texto = texto.zfill(4)
    return texto

def numeroEmisionMod(texto):
    texto = texto.zfill(8)
    return texto

def decimalesMod(texto):
    if len(texto) > 2:
        texto = texto[0:2]
        return texto
    elif len(texto) == 1:
        texto = texto.ljust(1,'0')
        return texto
    return texto
def corregirMontoImponible(texto):
    quitar = len(texto) - 12
    texto = texto[quitar:]
    return texto

def montoImponibleMod(texto):
    if len(texto) > 1:
        try:
            monto = texto.split(",")
            monto[1] = decimalesMod(monto[1])
            texto = monto[0] + "." + monto[1]
            texto = texto.zfill(12)
        except:
            texto = texto + ".00"
            texto = texto.zfill(12)
    if len(texto) > 12:
        texto = corregirMontoImponible(texto)    
    return texto

def importePercepcionMod(texto):
    if len(texto) > 1:
        monto = texto.split(",")
        monto[1] = decimalesMod(monto[1])
        texto = monto[0] + "." + monto[1]
        texto = texto.zfill(11)
    else:
        texto = texto + ".00"
        texto = texto.zfill(11)
    return texto


with open(argv[1], mode='r') as csv:
    newCsv = []
    
    for line in csv:
        x = line.split(";")
        cuit = x[0]
        fecha = x[1]
        tipoComprobante = x[2]
        letraComprobante = x[3]
        numeroSucursal = x[4]
        numeroEmision = x[5]
        montoImponible = x[6]
        importePercepcion = x[7]
        tipoOperacion = x[8]

        # Modifico cada una de las partes que se encuentran mal
        cuit = cuitMod(cuit)
        numeroSucursal = numeroSucursalMod(numeroSucursal)
        numeroEmision = numeroEmisionMod(numeroEmision)
        montoImponible = montoImponibleMod(montoImponible)
        importePercepcion = importePercepcionMod(importePercepcion)

        # Volvemos a formar la linea
        newCsv.append(
            cuit +
            fecha +
            tipoComprobante +
            letraComprobante +
            numeroSucursal +
            numeroEmision +
            montoImponible +
            importePercepcion +
            tipoOperacion)

with open("nuevoPercepciones.txt", mode="w", encoding="latin-1") as file:
    file.writelines(newCsv)