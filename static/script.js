function subirVideo() {
    let fileInput = document.getElementById("videoFile").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    let mensaje = document.getElementById("mensaje");
    let resultado = document.getElementById("resultado");
    let descargarBtn = document.getElementById("descargarBtn");

    // Mensaje de estado para el usuario
    mensaje.innerText = "Transcribiendo audio... Esto puede tardar varios minutos.";
    resultado.innerText = "";
    descargarBtn.style.display = "none";

    fetch("/transcribir", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            mensaje.innerText = "Error en la transcripción.";
            resultado.innerText = "Error: " + data.error;
        } else {
            mensaje.innerText = "Transcripción completada con éxito.";
            resultado.innerText = data.transcripcion;
            descargarBtn.style.display = "block";
        }
    })
    .catch(error => {
        mensaje.innerText = "Hubo un problema con la transcripción.";
        console.error("Error:", error);
    });
}

function descargarTranscripcion() {
    let texto = document.getElementById("resultado").innerText;
    let blob = new Blob([texto], { type: "text/plain" });
    let enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = "transcripcion.txt";
    enlace.click();
}
