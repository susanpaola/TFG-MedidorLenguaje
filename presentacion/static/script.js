function subirArchivo() {
    let fileInput = document.getElementById("videoFile").files[0];
    if (!fileInput) {
        alert("Selecciona un archivo primero.");
        return;
    }
    let formData = new FormData();
    formData.append("file", fileInput);

    let mensaje = document.getElementById("mensaje");
    let descargarTxt = document.getElementById("descargarTxt");
    let descargarPdf = document.getElementById("descargarPdf");
    let progressContainer = document.getElementById("progressContainer");
    let progressBar = document.getElementById("progressBar");

    progressContainer.style.display = "block";
    progressBar.style.animation = "loading 2s infinite linear";
    mensaje.innerText = "Transcribiendo audio... Esto puede tardar varios minutos.";
    descargarTxt.style.display = "none";
    descargarPdf.style.display = "none";

    fetch("/transcribir", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                mensaje.innerText = "Error en la transcripción: " + (data.error || "");
            } else {
                mensaje.innerText = "Transcripción completada con éxito.";
                // Guardamos rutas devueltas en atributos
                descargarTxt.style.display = "inline-block";
                descargarTxt.setAttribute("data-file", data.txt);
                descargarPdf.style.display = "inline-block";
                descargarPdf.setAttribute("data-file", data.pdf);
            }
            progressBar.style.animation = "none";
            progressBar.value = 100;
        })
        .catch(error => {
            mensaje.innerText = "Hubo un problema con la transcripción.";
            console.error("Error:", error);
            progressContainer.style.display = "none";
        });
}

function descargarTranscripcion(tipo) {
    let btn = tipo === 'txt' ? document.getElementById("descargarTxt") : document.getElementById("descargarPdf");
    let archivo = btn.getAttribute("data-file");
    if (archivo) {
        window.location.href = "/descargar?file=" + encodeURIComponent(archivo);
    }
}

// Modo oscuro simple
document.getElementById("toggleDarkMode").addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
});
