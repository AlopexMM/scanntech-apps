import sys

from citi import Venta
from citi import Compra
from citi import Verificaciones

class Citi(object):
    """ Process citi files and write new ones with corrections"""

    def __init__(self, *args):
        """ Init with arguments from console and process the files"""
        #Las opciones que maneja son:
        #   -c o --compras para citi compras
        #   -v o --ventas para citi ventas
        #Estas tienen que ir acompañada de dos archivos:
        #   comprobantes
        self.argv = args[0]

    def run(self):

        if self.argv[1] == '-c' or self.argv[1] == '--compras':
            try:
                self.run_compras(cbte=self.argv[2], ali=self.argv[3])
            except Exception:
                self._help(args=self.argv)
        elif self.argv[1] == '-v' or self.argv[1] == '--ventas':
            try:
                self.run_ventas(cbte=self.argv[2], ali=self.argv[3])
            except Exception:
                self._help(args=self.argv)
        else:
            self._help(self.argv)

    def _help(self, args=None):
        msg = """
            -v o --ventas [archivo comprobantes] [archivo alicuotas]
            -c o --compras [archivo comprobantes] archivo alicuotas]
            """
        print(msg)
        if args is not None:
            print("\tRevise los argumentos pasados {}".format(args[1:]))

    def run_compras(self, cbte, ali):
        comprobante = Compra.Comprobante()
        alicuota = Compra.Alicuota()
        lista_cbte = comprobante.procesar_comprobante(cbte)
        lista_alicuota = alicuota.procesar_alicuota(ali)
        comprobar = Compra.Verificacion()
        lista_cbte = comprobar.comprobacion(lista_cbte, lista_alicuota)
        self._write_file(lista_cbte, 'compras_cbte.txt')
        self._write_file(lista_alicuota, 'compras_alicuotas.txt')


    def run_ventas(self, cbte, ali):
        comprobante = Venta.comprobante()
        alicuota = Venta.alicuota()
        lista_cbte = comprobante.procesamiento_comprobantes(cbte)
        lista_alicuotas = alicuota.procesamiento_alicuotas(ali)
        comprobar = Venta.verificaciones()
        lista_cbte = comprobar.verificar_nro_alicuotas(
            lista_cbte, lista_alicuotas)
        lista_cbte = comprobar.verificar_monto_final(
            lista_cbte, lista_alicuotas)
        lista_cbte, lista_alicuotas = comprobar.verificar_comprobantes_cero(
    lista_cbte, lista_alicuotas)

        self._write_file(lista_cbte,'ventas_cbte.txt')
        self._write_file(lista_alicuotas, 'ventas_alicuotas.txt')

    def _write_file(self, data, file_name):
        with open(file_name, 'w') as f:
            for line in data:
                f.write(line + '\n\r')

if __name__ == '__main__':
    Citi(sys.argv)
