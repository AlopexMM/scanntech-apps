#!/usr/bin/env bash

cd $HOME/.scanntech-apps/

git clone https://github.com/AlopexMM/scanntech-apps.git

cp -r $HOME/.scanntech-apps/scanntech-apps/app/* $HOME/.scanntech-apps/app/

rm -rf $HOME/.scanntech-apps/scanntech-apps
