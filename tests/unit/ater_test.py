from ater.init import OldAter, NewAter
def test_old_ater_line():
    cbte = OldAter(
        tipo_de_agente="1",
        motivo_movimiento="061",
        cuit_cliente="20263325347",
        fecha_percepcion="01/08/2021",
        tipo_de_comprobante="TF    ",
        letra_comprobante="A",
        numero_de_comprobante="002300017873",
        importe_base="000000004817.52",
        alicuota="003.00",
        importe_percibido="14.45",
        anulacion="0",
        contribuyente_conv_multi="0"
    )
    text = "10612026332534701/08/2021TF    A002300017873000000004817.52003.0014.4500\n"
    assert text == cbte.line()

def test_new_ater_line():
    cbte = NewAter(
        id = 1,
        tipo_de_comprobante="1",
        letra_comprobante="A",
        numero_de_comprobante="002300017873",
        cuit_cliente="20263325347",
        fecha_percepcion="01/08/2021",
        monto_sujeto_a_percepcion="000000004817.52",
        alicuota="003.00",
        monto_percibido="14.45",
        tipo_de_regimen_de_percepcion="004",
        jurisdiccion="908"
    )
    text = """00001,1,A,002300017873,20263325347,01/08/2021,000000004817.52,003.00,14.45,004,908\n"""

    assert text == cbte.line()
