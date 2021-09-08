import sys

from zipfile import ZipFile
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
        #   -vd o --ventas-duplicados
        self.argv = args[0]

    def run(self):

        try:

            if self.argv[1] == '-c' or self.argv[1] == '--compras':
                self.run_compras(cbte=self.argv[2], ali=self.argv[3])
            elif self.argv[1] == '-v' or self.argv[1] == '--ventas':
                self.run_ventas(cbte=self.argv[2], ali=self.argv[3])
            elif self.argv[1] == '-cjoin' or self.argv[1] == "--compras-join":
                self.join_files(files="compras", args=self.argv[2:])
            elif self.argv[1] == '-vjoin' or self.argv[1] == "--ventas-join":
                self.join_files(files="ventas", args=self.argv[2:])
            else:
                self._help(args=self.argv)
        except IndexError:
            self._help()
        except Exception as e:
            raise e

    def _help(self, args=None):
        msg = """
            -v o --ventas [CBTE] [ALICUOTAS]
            -vjoin o --ventas-join [Archivos Zip]
            -c o --compras [CBTE] [ALICUOTAS]
            -cjoin o --compras-join [Archivos Zip]
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

    def join_files(self,args, files):
        """ Reviza los zip en busca de los archivos txt de las exportaciones y los une en uno solo"""
        if files == "compras":
            cbte = "REGINFO_CV_COMPRAS_CBTE.txt"
            exp_cbte = "compras_cbte.txt"
            ali = "REGINFO_CV_COMPRAS_ALICUOTAS.txt"
            exp_ali = "compras_alicuotas.txt"
        if files == "ventas":
            cbte = "REGINFO_CV_VENTAS_CBTE.txt"
            exp_cbte = "ventas_cbte.txt"
            ali = "REGINFO_CV_VENTAS_ALICUOTAS.txt"
            exp_ali = "ventas_alicuotas.txt"
        for z in args:
            try:
                with ZipFile(z) as myzipfile:
                    with myzipfile.open(cbte) as txt:
                        with open(exp_cbte, mode="a", newline="\r\n") as exp:
                            text = str(txt.readlines()).replace("'","").replace("[","").replace("]","").replace("b","").replace(",","").split('\\r\\n')[1:]
                            for l in text:
                                if l != "":
                                    l = l[1:] + "\n"
                                    exp.write(l)
                    with myzipfile.open(ali) as txt:
                        with open(exp_ali, mode="a", newline="\r\n") as exp:
                            text = str(txt.readlines()).replace("'","").replace("[","").replace("]","").replace("b","").replace(",","").split('\\r\\n')[1:]
                            for l in text:
                                if l != "":
                                    l = l[1:] + "\n"
                                    exp.write(l)
            except Exception as e:
                raise e

    def run_ventas(self, cbte, ali):
        citi_venta = venta.Venta(cbte, ali)
        citi_venta.run()

    #def remove_ptv(self, ptv, cbte, ali):
    #    citi_venta = venta.Venta(cbte, ali)
    #    citi_venta.process_cbte_and_alicuota(ptv=ptv)
    #    citi_venta.write_file(filename="ventas_cbte.txt",data_to_use="cbte")
    #    citi_venta.write_file(filename="ventas_alicuotas.txt")

    def _write_file(self, data , filename):
        with open(filename,"w", encoding="latin-1", newline="\r\n") as f:
            for l in data:
                f.write(l + "\n")

if __name__ == '__main__':
    Citi(sys.argv)
