from sys import argv
from datetime import date
from time import strftime

class Padron(object):
    """
    Process padron files and export one file with the format for sysadmin
    """
    def __init__(self, *args) -> None:
        self.argv = args[0]
        today = date.today()
        t = today.strftime("%d-%m-%Y")
        self.file = f"padron_sysadmin_{t}.txt"

    def _export(self,line) -> None:
        with open(self.file,mode="a",encoding="latin-1",newline="\r\n") as f:
        		f.write(line)
        return

    def run(self):
        for file in self.argv[1:]:
            print(f"Procesando {file}")
            with open(file,mode="r",encoding="latin-1") as f:
                for line in f.readlines():
                    line = line.replace("\n","")
                    if len(line) == 52:
                        l = line.split(";")
                        lf = f"P;{l[1]};{l[2]};{l[3]};{l[4]};{l[5]};{l[6]};{l[7]};{l[8]};;1\n"
                        self._export(lf)
                    if len(line) == 55:
                        l = line.split(";")
                        lf = f"P;{l[1]};{l[2]};{l[3]};{l[4]};{l[5]};{l[6]};{l[7]};{l[8]};{l[9]};6\n"
                        self._export(lf)
        print("Se procesaron los padrones se va a exportar el reporte final")
        print(f"Se gravo el archivo {self.file}")

if __name__ == "__main__":
	result = Padron(argv[1:])
	result.run()
