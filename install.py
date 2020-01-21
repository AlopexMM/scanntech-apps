#!/usr/bin/env python3

import os
import subprocess
import shutil

dir_instalacion = os.path.join(os.environ["HOME"],".scanntech-apps")

lista_programas = ["git","virtualenv"]

alias = os.path.join(os.environ["HOME"],".bash_aliases")

# Verifico que en el sistema se encuentren los programas necesarios instalados
for programa in lista_programas:
    if subprocess.call(["which",programa]):
        subprocess.call(["sudo","apt","install",programa])

# Descargamos el repositorio
subprocess.call(
    ["git", "clone", "https://github.com/AlopexMM/scanntech-apps.git"])

scanntech_apps = os.path.abspath("scanntech-apps")
src = os.path.join(scanntech_apps,"src")
requirements = os.path.join(scanntech_apps,"requirements.txt")
requirements_sh = os.path.join(scanntech_apps, "requirements.sh")
# Copiamos los archivos al directorio de instalación
if os.path.isdir(dir_instalacion):
    shutil.copytree(src,dir_instalacion)
    shutil.copy(requirements,dir_instalacion)
else:
    os.mkdir(dir_instalacion)
    shutil.copytree(src, dir_instalacion)
    shutil.copy(requirements, dir_instalacion)

# Nos paramos en el directorio de la app
os.chdir(dir_instalacion)

# Creamos el entorno virtual
subprocess.call(["virtualenv","venv","--python=python3"])
subprocess.call(["sh", "requirements.sh"])

# Por ultimo agregamos en bash_aliases la linea
virtualenv = os.path.join(dir_instalacion,"venv/bin/activate")
program = os.path.join(dir_instalacion,"src/cli.py")
linea = "source {0};python  {1}".format(virtualenv,program)

archivo = []
with open(alias,mode="r") as file:
    for line in file:
        if line.find("alias citi="):
            line = linea
            archivo.append(line)            
        elif line != "":
            archivo.append(line)

with open(alias,mode="w") as file:
    file.writelines(archivo)            
