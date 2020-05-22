#!/usr/bin/env bash

cd $HOME/.scanntech-apps/

git clone https://github.com/AlopexMM/scanntech-apps.git

cp -r $HOME/.scanntech-apps/scanntech-apps/module_cli/* $HOME/.scanntech-apps/module_cli/

rm -rf $HOME/.scanntech-apps/scanntech-apps