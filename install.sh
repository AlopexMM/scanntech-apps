#!/bin/bash
# Instalador del aplicativo en la carpeta home de los sistemas GNU/Linux
# License: MIT
# Dependecies: None
# Libreries: None

diraplicativo="$HOME/.scanntech/appciti"
directorioshome=`ls -a $HOME/.scanntech/ | grep appciti`
src="./src" 

if [[ $directorioshome = "appciti" ]]; then
    echo `rm -r $diraplicativo/*`
    echo `cp -r $src/* $diraplicativo`
else
    echo `mkdir -p $diraplicativo`
    echo `cp -r $src/* $diraplocativo`
    echo "alias citi='python3 $HOME/.scanntech/appciti/cli.py'" >> "$HOME/.bash_aliases"
fi

echo "-------------------------------------------------"
echo "Finalizo la instalación, cierre y vuelva a       "
echo " ingresar a la terminal                          "
echo "-------------------------------------------------"