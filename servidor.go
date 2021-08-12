package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
)

var fechaTerminacion time.Time

const MinutosRecargaPorMoneda = 10

func obtenerSegundosRestantes() int64 {
	return int64(fechaTerminacion.Sub(time.Now()).Seconds())
}

func agregarCeroSiEsNecesario(valor int) string {
	return fmt.Sprintf("%02d", valor)
}

func segundosASegundosMinutosYHoras(segundos float64) string {
	horas := int(segundos / 60 / 60)
	segundos -= float64(horas * 60 * 60)
	minutos := int(segundos / 60)
	segundos -= float64(minutos * 60)
	return fmt.Sprintf("%02d:%02d:%02d", horas, minutos, int(segundos))
}

func main() {
	fechaTerminacion = time.Now()
	http.HandleFunc("/", func(w http.ResponseWriter, peticion *http.Request) {
		json.NewEncoder(w).Encode(obtenerSegundosRestantes())
	})

	http.HandleFunc("/segundos_restantes", func(w http.ResponseWriter, peticion *http.Request) {
		json.NewEncoder(w).Encode(obtenerSegundosRestantes())
	})

	http.HandleFunc("/reiniciar", func(w http.ResponseWriter, peticion *http.Request) {
		fechaTerminacion = time.Now()
		json.NewEncoder(w).Encode(true)
	})

	http.HandleFunc("/recargar", func(w http.ResponseWriter, r *http.Request) {
		minutosArray, ok := r.URL.Query()["minutos"]
		minutos := MinutosRecargaPorMoneda

		if ok && len(minutosArray) >= 1 {
			var err error
			minutos, err = strconv.Atoi(minutosArray[0])
			if err != nil {
				log.Printf("error convirtiendo minutos: %s", err.Error())
			}
		}
		log.Printf("recargar %d minutos", minutos)
		duracionAgregar := time.Minute * time.Duration(minutos)
		if obtenerSegundosRestantes() <= 0 {
			fechaTerminacion = time.Now().Add(duracionAgregar)
		} else {
			fechaTerminacion = fechaTerminacion.Add(duracionAgregar)
		}
		json.NewEncoder(w).Encode(true)
	})
	direccion := ":8000"
	fmt.Println("Servidor listo escuchando en " + direccion)
	log.Fatal(http.ListenAndServe(direccion, nil))
}