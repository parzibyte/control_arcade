#!/bin/sh
# Recuerda que antes debes compilar el programa
# /usr/local/go/bin/go build servidor.go
~/control_arcade/servidor >> ~/control_arcade/servidor.log 2>&1 &
/usr/bin/python3 ~/control_arcade/contador_tiempo.py >> ~/control_arcade/contador.log 2>&1 &
/usr/bin/lxterminal -e /usr/bin/emulationstation