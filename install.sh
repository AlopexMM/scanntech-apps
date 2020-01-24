#!/bin/bash

aliases=`cat .bash_aliases | cut -d"=" -f1`

if [[x in $aliases -eq "alias scanntech"]]; then
    echo "Funciona"
fi
echo $aliases