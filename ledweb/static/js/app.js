document.addEventListener('DOMContentLoaded', () => {
    console.log("Sistema de monitoreo cargado...");

    // Humedad
    const sliderH = document.getElementById('slider-humedad');
    const displayH = document.getElementById('val-humedad');
    const ledH = document.getElementById('led-humedad');

    // Temperatura
    const sliderT = document.getElementById('slider-temp');
    const displayT = document.getElementById('val-temp');
    const ledT = document.getElementById('led-temp');

    // Listener Humedad
    sliderH.addEventListener('input', function() {
        let v = this.value;
        displayH.innerHTML = v + "%";
        
        let color, estado;
        if (v < 33) { color = "green"; estado = "OK"; }
        else if (v <= 66) { color = "yellow"; estado = "ADVERTENCIA"; }
        else { color = "red"; estado = "ALERTA"; }

        ledH.className = `led led-${color} mx-auto my-4`;
        enviarComando("HUMEDAD", estado);
    });

    // Listener Temperatura
    sliderT.addEventListener('input', function() {
        let v = this.value;
        displayT.innerHTML = v + "°C";
         
        let color, estado;
        // 16-22 Verde | 23-28 Amarillo | 29 > Rojo
        if (v >= 16 && v <= 22) { color = "green"; estado = "NORMAL"; }
        else if (v >= 23 && v <= 28) { color = "yellow"; estado = "ELEVADA"; }
        else { color = "red"; estado = "ALERTA"; }

        ledT.className = `led led-${color} mx-auto my-4`;
        enviarComando("TEMP", estado);
    });

    async function enviarComando(tipo, estado) {
        try {
            await fetch('/update_sensor', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ type: tipo, status: estado })
            });
        } catch (e) {
            console.error("Error enviando datos a Flask");
        }
    }
});
