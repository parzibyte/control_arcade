const RUTA_SERVIDOR = ".";
new Vue({
    el: "#app",
    data: () => ({
        minutos: 10,
        cargando: false,
    }),
    methods: {
        async recargar() {
            this.cargando = true;
            try {
                const response = await fetch(`${RUTA_SERVIDOR}/recargar?minutos=${this.minutos}`);
                this.$buefy.toast.open("Recargado con éxito")
            } catch (e) {
                this.$buefy.toast.open("Error recargando: " + e.message)
            } finally {
                this.cargando = false;
            }
        },
        reiniciarTiempo() {
            this.$buefy.dialog.confirm({
                title: "Reiniciar tiempo",
                message: "Esto colocará el tiempo en 0",
                confirmText: "Sí, reiniciar",
                cancelText: "Cancelar",
                type: 'is-danger',
                onConfirm: async () => {
                    this.cargando = true;
                    try {
                        const response = await fetch(`${RUTA_SERVIDOR}/reiniciar`);
                        this.$buefy.toast.open("Reiniciado con éxito")
                    } catch (e) {
                        this.$buefy.toast.open("Error reiniciando: " + e.message)
                    } finally {
                        this.cargando = false;
                    }
                }
            })
        }
    }
});
