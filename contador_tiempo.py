import tkinter as tk
import urllib.request
import json
import subprocess
from constantes import URL_SERVIDOR


INTERVALO_CONSULTAS_EN_MILISEGUNDOS = 300
TIEMPO_CERO = "00:00:00"
TAMANIO_FUENTE = 30
FUENTE = "Consolas"
gpio_encendido = False


def apagar_gpio():
    global gpio_encendido
    print("Apagando GPIO...")
    try:
        subprocess.Popen(["bash","/usr/bin/gpionext", "stop"])
        print("GPIO apagado")
    except:
        print("Error apagando GPIO")
    gpio_encendido = False


def encender_gpio():
    global gpio_encendido
    print("Encendiendo GPIO...")
    try:
        subprocess.Popen(["bash","/usr/bin/gpionext", "start"])
        print("GPIO encendido")
    except:
        print("Error encendiendo GPIO")
    gpio_encendido = True


def init():
    apagar_gpio()


def agregar_cero_si_es_necesario(valor):
    if valor >= 10:
        return str(valor)
    else:
        return "0"+str(valor)


def segundos_a_segundos_minutos_y_horas(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    cadena = f"{agregar_cero_si_es_necesario(horas)}:{agregar_cero_si_es_necesario(minutos)}:{agregar_cero_si_es_necesario(segundos)}"
    return cadena


def obtener_tiempo_restante():
    return json.loads(urllib.request.urlopen(URL_SERVIDOR+"/segundos_restantes").read())


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.crear_widgets()

    def crear_widgets(self):
        variable_tiempo_restante.set(TIEMPO_CERO)
        self.etiqueta_tiempo_restante = tk.Label(
            self, font=f"{FUENTE} {TAMANIO_FUENTE} bold", bg="black", fg="white", textvariable=variable_tiempo_restante)
        self.etiqueta_tiempo_restante.pack(side="top")


def verificar_tiempo():
    segundos_restantes = obtener_tiempo_restante()
    restante_legible = TIEMPO_CERO
    if segundos_restantes <= 0:
        if gpio_encendido:
            apagar_gpio()
    else:
        if not gpio_encendido:
            encender_gpio()
        restante_legible = segundos_a_segundos_minutos_y_horas(
            segundos_restantes)

    variable_tiempo_restante.set(restante_legible)
    root.after(INTERVALO_CONSULTAS_EN_MILISEGUNDOS, verificar_tiempo)


def alinear_esquina_superior_izquierda(r):
    r.geometry("+0+0")


def alinear_esquina_inferior_derecha(r):
    r.geometry("-0-0")


def alinear_esquina_inferior_izquierda(r):
    r.geometry("+0-0")


def alinear_esquina_superior_derecha(r):
    r.geometry("-0+0")


init()

variable_tiempo_restante = None
root = tk.Tk()
variable_tiempo_restante = tk.StringVar(root)
root.attributes('-alpha', 1)
root.attributes('-topmost', True)
alinear_esquina_superior_derecha(root)
root.overrideredirect(True)
root.lift()
verificar_tiempo()
app = Application(master=root)
app.mainloop()
