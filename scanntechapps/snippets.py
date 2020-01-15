# Esta clase contiene funciones que tienen en comun los reportes de ARBA y ATER

def grabar(datos,nombre):
        with open(nombre,"w",encoding="latin-1") as file:
                file.writelines(datos)
        return
    
def valores_genericos(rango, valor):
    # Rango es el tamaño de la lista y valor es el dato que va a contener
    .lista = []
    for x in range(rango):
        .lista.append(valor)
    return .lista

def arreglo_fecha(fechas):
    .lista = []
    for x in fechas:
        .lista.append(x.strftime("%d/%m/%Y"))
    return .lista

def pasar_string(datos,fill=None,decimal=None):
    lista = []
    if decimal:
        for x in datos:
            x = format(x,".2f")
            lista.append(str(x).zfill(fill))
    elif decimal == False:
        for x in datos:
            x = str(x).split(".")
            lista.append(x[0].zfill(fill))
    else:
        for x in range(len(datos)):
            lista.append(str(datos[x].zfill(fill)))
    return lista

def escribir_reporte(datos,ater=False,arba=False):
    if ater:
        return grabar(datos,"~/scanntech-apps/docs/ater.txt")
    if arba:
        return grabar(datos,"~/scanntech-apps/docs/arba.txt")
    return