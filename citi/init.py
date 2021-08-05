import sys
import sqlite3

from citi import venta
from citi import Compra

class Citi(object):
    """ Process citi files and write new ones with corrections"""

    def __init__(self, *args):
        """ Init with arguments from console and process the files"""
        #Las opciones que maneja son:
        #   -c o --compras para citi compras
        #   -v o --ventas para citi ventas
        #   -rmp o --remove-ptv para citi ventas
        #   -dbv o --database-ventas para citi ventas
        # TODO quitar comprobantes con valor cero de compras
        #Estas tienen que ir acompañada de dos archivos:
        #   comprobantes
        self.argv = args[0]

    def run(self):

        if self.argv[1] == '-c' or self.argv[1] == '--compras':
            self.run_compras(cbte=self.argv[2], ali=self.argv[3])
        elif self.argv[1] == '-v' or self.argv[1] == '--ventas':
            self.run_ventas(cbte=self.argv[2], ali=self.argv[3])
        elif self.argv[1] == '-rmp' or self.argv[1] == '--remove-ptv':
            ptv = self.argv[2].zfill(5)
            self.remove_ptv(ptv=ptv, cbte=self.argv[3], ali=self.argv[4])
        elif self.argv[1] == '-dbv' or self.argv[1] == '--database-ventas':
            self.create_database_ventas(cbte=self.argv[2], ali=self.argv[3])
        else:
            self._help(args=self.argv)

    def _help(self, args=None):
        msg = """
            -v o --ventas [CBTE] [ALICUOTAS]
            -rmp o --remove-ptv [PTV] [CBTE] [ALICUOTAS]
            -dbv o --database-ventas [CBTE] [ALICUOTAS]
            -c o --compras [CBTE] [ALICUOTAS]
            """
        print(msg)
        if args is not None:
            print("\tRevise los argumentos pasados {}".format(args[1:]))

    def run_compras(self, cbte, ali):
        """ Remueve lineas segun la lista de puntos de venta """
        comprobante = Compra.Comprobante()
        alicuota = Compra.Alicuota()
        lista_cbte = comprobante.procesar_comprobante(cbte)
        lista_alicuota = alicuota.procesar_alicuota(ali)
        comprobar = Compra.Verificacion()
        lista_cbte = comprobar.comprobacion(lista_cbte, lista_alicuota)
        self._write_file(lista_cbte, 'compras_cbte.txt')
        self._write_file(lista_alicuota, 'compras_alicuotas.txt')


    def run_ventas(self, cbte, ali):
        citi_venta = venta.Venta(cbte, ali)
        citi_venta.process_cbte_and_alicuota()
        citi_venta.write_file(filename="ventas_cbte.txt",data_to_use="cbte")
        citi_venta.write_file(filename="ventas_alicuotas.txt")

    # def remove_ptv(self, ptv, cbte, ali):
        # comprobante = Venta.comprobante()
        # alicuota = Venta.alicuota()
        # lista_cbte = comprobante.remove_ptv(ptv,cbte)
        # lista_alicuotas = alicuota.remove_ptv(ptv,ali)
# 
        # self._write_file(lista_cbte,'ventas_cbte.txt')
        # self._write_file(lista_alicuotas, 'ventas_alicuotas.txt')

    def create_database_ventas(self, cbte, ali):
        citi_venta = venta.Venta(cbte,ali)
        citi_venta.process_cbte_and_alicuota()
        citi_venta.create_database()
    
    def _write_file(self, data , filename):
        with open(filename,"w", encoding="latin-1", newline="\r\n") as f:
            for l in data:
                f.write(l + "\n")

if __name__ == '__main__':
    Citi(sys.argv)
