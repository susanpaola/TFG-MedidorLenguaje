function subirArchivo() {
    let fileInput = document.getElementById("videoFile").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    let mensaje = document.getElementById("mensaje");
    let descargarBtn = document.getElementById("descargarBtn");
    let progressBar = document.getElementById("progressBar");
    let progressContainer = document.getElementById("progressContainer");

    // Mostrar barra de progreso
    progressContainer.style.display = "block";
    progressBar.value = 0;
    mensaje.innerText = "Transcribiendo audio... Esto puede tardar varios minutos.";
    descargarBtn.style.display = "none";

    fetch("/transcribir", {
        method: "POST",
        body: formData
    })
    .then(response => {
        let totalSteps = 3; // Simulación de progreso (dividir, transcribir, guardar)
        let step = 0;
        let interval = setInterval(() => {
            if (step < totalSteps) {
                progressBar.value = (step + 1) * (100 / totalSteps);
                step++;
            } else {
                clearInterval(interval);
            }
        }, 2000); // Simulación de progreso cada 2 segundos

        return response.json();
    })
    .then(data => {
        if (data.error) {
            mensaje.innerText = "Error en la transcripción.";
        } else {
            mensaje.innerText = "Transcripción completada con éxito.";
            descargarBtn.style.display = "block";
            descargarBtn.setAttribute("data-file", data.archivo);
        }
        progressContainer.style.display = "none";
    })
    .catch(error => {
        mensaje.innerText = "Hubo un problema con la transcripción.";
        console.error("Error:", error);
        progressContainer.style.display = "none";
    });
}

function descargarTranscripcion() {
    let archivo = document.getElementById("descargarBtn").getAttribute("data-file");
    if (archivo) {
        window.location.href = "/descargar?file=" + encodeURIComponent(archivo);
    }
}

// Modo oscuro
document.getElementById("toggleDarkMode").addEventListener("click", function() {
    document.body.classList.toggle("dark-mode");
});
