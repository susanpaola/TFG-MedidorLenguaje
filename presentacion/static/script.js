function subirArchivo() {
    let fileInput = document.getElementById("videoFile").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    let mensaje = document.getElementById("mensaje");
    let descargarBtn = document.getElementById("descargarBtn");
    let progressContainer = document.getElementById("progressContainer");
    let progressBar = document.getElementById("progressBar");

    // Mostrar barra de progreso con animación infinita
    progressContainer.style.display = "block";
    progressBar.style.animation = "loading 2s infinite linear";
    mensaje.innerText = "Transcribiendo audio... Esto puede tardar varios minutos.";
    descargarBtn.style.display = "none";

    fetch("/transcribir", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            mensaje.innerText = "Error en la transcripción.";
        } else {
            mensaje.innerText = "Transcripción completada con éxito.";
            descargarBtn.style.display = "block";
            descargarBtn.setAttribute("data-file", data.archivo);
        }

        // Detener animación y llenar la barra
        progressBar.style.animation = "none";
        progressBar.style.background = "#28a745"; // Verde de éxito
    })
    .catch(error => {
        mensaje.innerText = "Hubo un problema con la transcripción.";
        console.error("Error:", error);

        // Ocultar barra si hay error
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
