// function processAudio(result){
//     // Later, change this so the audio is sent to the output

//     output = document.getElementById("finalResultOutput")
//     output.textContent = result
// }


async function processAudio() {
    const fileInput = document.getElementById("audioFile");
    if (!fileInput.files.length) {
        alert("Please choose an audio file first.");
        return;
    }

    const formData = new FormData();
    formData.append("audio", fileInput.files[0]);  // "audio" is the field name

    try {
        const response = await fetch("http://127.0.0.1:5000/process_audio", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();  // expecting { result: "..." }
        const output = document.getElementById("finalResultOutput");
        output.textContent = data.result;
    } catch (err) {
        console.error(err);
        document.getElementById("finalResultOutput").textContent = "Error processing audio." + err;
    }
}