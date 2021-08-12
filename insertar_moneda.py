import urllib.request
import argparse
from constantes import URL_SERVIDOR
MINUTOS_POR_DEFECTO = 10
parser = argparse.ArgumentParser()
parser.add_argument("--minutos", help="Cantidad de minutos a recargar")
argumentos = parser.parse_args()
minutos = MINUTOS_POR_DEFECTO
if argumentos.minutos:
    minutos = argumentos.minutos
print(f"Recargando {minutos} minutos...")
urllib.request.urlopen(f"{URL_SERVIDOR}/recargar?minutos={minutos}")
