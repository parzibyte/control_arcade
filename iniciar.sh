#!/bin/sh
# Recuerda que antes debes compilar el programa
# /usr/local/go/bin/go build servidor.go
./servidor
/usr/bin/python3 contador_tiempo.py 2>1 &
/usr/bin/lxterminal -e /usr/bin/emulationstation