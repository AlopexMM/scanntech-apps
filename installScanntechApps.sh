#!/usr/bin/bash

sudo apt-get -y install git python-virtualenv python3-pip virtualenv

mkdir $HOME/.scanntech-apps

cd $HOME/.scanntech-apps

git clone https://github.com/AlopexMM/scanntech-apps.git

cp -r $HOME/.scanntech-apps/scanntech-apps/module_cli $HOME/.scanntech-apps/

virtualenv venv --python=python3

echo "alias scanntech=\"source $HOME/.scanntech-apps/venv/bin/activate;python3 $HOME/.scanntech-apps/module_cli/cli.py\"" > $HOME/.bash_aliases

source $HOME/.scanntech-apps/venv/bin/activate; pip install -r $HOME/.scanntech-apps/scanntech-apps/requirements.txt

rm -rf $HOME/.scanntech-apps/scanntech-apps

