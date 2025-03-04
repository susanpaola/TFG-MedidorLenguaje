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
        if (data.error) {
            document.getElementById("resultado").innerText = "Error: " + data.error;
        } else {
            document.getElementById("resultado").innerText = data.transcripcion;
            document.getElementById("descargarBtn").style.display = "block";
        }
    })
    .catch(error => console.error("Error:", error));
}

function descargarTranscripcion() {
    let texto = document.getElementById("resultado").innerText;
    let blob = new Blob([texto], { type: "text/plain" });
    let enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = "transcripcion.txt";
    enlace.click();
}
