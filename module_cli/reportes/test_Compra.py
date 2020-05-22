from .Compra import Alicuota
from .Compra import Verificacion


# Test de alicuotas
LINEA_ALICUOTA = ["001000060000000000060000581280000000000307153085640000000021506770004000000000225821"]
LINEA_ALI_CORREGIDA = "001000060000000000060000581280000000000307153085640000000021506770004000000000225821"

def test_correccion_impuesto_liquidado():
    # Solo maneja una alicuota faltan ejemplos para todas las alicuotas
    alicuota = Alicuota()
    linea_ali = alicuota.diccionario_alicuota(LINEA_ALICUOTA[0])
    linea_ali = alicuota.correccion_impuesto_liquidado(linea_ali)
    linea_ali = alicuota.construir_linea_alicuota(linea_ali)
    assert linea_ali == LINEA_ALI_CORREGIDA

# Test de Verificacion
LINEA_COMPROBANTE = ["""202001040010000600000000000600005812                8000000000030715308564SABORES SALUDABLES S.A        000000002376498000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000PES00010000001N00000000215067700000000000000000000000000                              000000000000000"""]
LINEA_CBTE_CORREGIDA = ["""202001040010000600000000000600005812                8000000000030715308564SABORES SALUDABLES S.A        000000002376498000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000PES00010000001N00000000022582100000000000000000000000000                              000000000000000"""]

def test_comprobancion():
    comprobar = Verificacion()
    lista_cbte = comprobar.comprobacion(LINEA_COMPROBANTE, LINEA_ALICUOTA)

    assert lista_cbte == LINEA_CBTE_CORREGIDA
