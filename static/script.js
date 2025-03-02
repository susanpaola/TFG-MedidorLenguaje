let archivoTranscripcion = "";

function subirVideo() {
    let fileInput = document.getElementById("videoFile").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    fetch("/transcribir", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("resultado").innerText = data.transcripcion;
        archivoTranscripcion = data.archivo;  // Guarda el nombre del archivo para descargar

        // Mostrar botón de descarga
        document.getElementById("descargarBtn").style.display = "block";
    })
    .catch(error => console.error("Error:", error));
}

function descargarTranscripcion() {
    window.location.href = `/descargar/${archivoTranscripcion}`;
}
