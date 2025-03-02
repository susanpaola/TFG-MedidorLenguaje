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
    })
    .catch(error => console.error("Error:", error));
}
