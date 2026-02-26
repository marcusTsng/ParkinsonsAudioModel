// // // function processAudio(result){
// // //     // Later, change this so the audio is sent to the output

// // //     output = document.getElementById("finalResultOutput")
// // //     output.textContent = result
// // // }


// // async function processAudio() {
// //     const fileInput = document.getElementById("audioFile");
// //     if (!fileInput.files.length) {
// //         alert("Please choose an audio file first.");
// //         return;
// //     }

// //     const formData = new FormData();
// //     formData.append("audio", fileInput.files[0]);  // "audio" is the field name

// //     try {
// //         const response = await fetch("http://127.0.0.1:6767/process_audio", {
// //             method: "POST",
// //             body: formData
// //         });

// //         if (!response.ok) {
// //             throw new Error("Server error: " + response.status);
// //         }

// //         const data = await response.json();  // expecting { result: "..." }
// //         const output = document.getElementById("finalResultOutput");
// //         output.textContent = data.result;
// //     } catch (err) {
// //         console.error(err);
// //         document.getElementById("finalResultOutput").textContent = "Error processing audio." + err;
// //     }
// // }

// // async function processAudio() {
// //     const fileInput = document.getElementById("audioFile");
// //     if (!fileInput.files.length) {
// //         alert("Please choose an audio file first.");
// //         return;
// //     }

// //     const formData = new FormData();
// //     formData.append("audio", fileInput.files[0]);

// //     try {
// //         const response = await fetch("http://127.0.0.1:6767/process_audio", {  // ← 6767!
// //             method: "POST",
// //             body: formData
// //         });

// //         if (!response.ok) {
// //             throw new Error("Server error: " + response.status);
// //         }

// //         const data = await response.json();
// //         document.getElementById("finalResultOutput").textContent = data.result;
// //     } catch (err) {
// //         console.error(err);
// //         document.getElementById("finalResultOutput").textContent = "Error processing audio: " + err;
// //     }
// // }

// let mediaRecorder;
// let audioChunks = [];
// let audioBlob;
// let isRecording = false;

// async function processAudio(blob) {
//     const formData = new FormData();
//     formData.append("audio", blob, "recording.webm");

//     try {
//         const response = await fetch("http://127.0.0.1:6767/process_audio", {
//             method: "POST",
//             body: formData
//         });

//         if (!response.ok) {
//             throw new Error(`Server error: ${response.status}`);
//         }

//         const data = await response.json();
//         document.getElementById("finalResultOutput").textContent = data.result;
//         document.getElementById("recordingStatus").textContent = 
//             `Result: ${data.result} (${data.interpretation || (parseFloat(data.result) > 0.5 ? "Parkinson's" : "Healthy")})`;
//     } catch (err) {
//         console.error(err);
//         document.getElementById("finalResultOutput").textContent = "Error processing audio: " + err;
//     }
// }

// async function startRecording() {
//     try {
//         // Get microphone access
//         const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//         mediaRecorder = new MediaRecorder(stream);
//         audioChunks = [];

//         mediaRecorder.ondataavailable = (event) => {
//             audioChunks.push(event.data);
//         };

//         mediaRecorder.onstop = () => {
//             audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
//             stream.getTracks().forEach(track => track.stop()); // Stop mic
            
//             // Enable submit button
//             document.getElementById("submitRecording").disabled = false;
//             document.getElementById("recordingStatus").textContent = "Recording complete! Click Submit.";
//         };

//         mediaRecorder.start();
//         isRecording = true;
        
//         // UI updates
//         document.getElementById("startRecord").disabled = true;
//         document.getElementById("stopRecord").disabled = false;
//         document.getElementById("recordingStatus").textContent = "🎤 Recording... Speak now!";
        
//     } catch (err) {
//         console.error("Microphone access denied:", err);
//         document.getElementById("finalResultOutput").textContent = "Microphone access denied. Please allow microphone.";
//     }
// }

// function stopRecording() {
//     if (mediaRecorder && isRecording) {
//         mediaRecorder.stop();
//         isRecording = false;
        
//         document.getElementById("startRecord").disabled = false;
//         document.getElementById("stopRecord").disabled = true;
//     }
// }

// function submitRecording() {
//     if (audioBlob) {
//         document.getElementById("recordingStatus").textContent = "Analyzing...";
//         processAudio(audioBlob);
//     }
// }

// // File upload (your existing function - unchanged)
// async function processFileUpload() {
//     const fileInput = document.getElementById("audioFile");
//     if (!fileInput.files.length) {
//         alert("Please choose a file first.");
//         return;
//     }
//     processAudio(fileInput.files[0]);
// }

// // Event listeners
// document.getElementById("startRecord").onclick = startRecording;
// document.getElementById("stopRecord").onclick = stopRecording;
// document.getElementById("submitRecording").onclick = submitRecording;
// document.getElementById("audioFile").onchange = processFileUpload;

// // Auto-submit on file select (optional convenience)

// let recordedAudioBlob = null;  // Global for playback

// // ... your existing processAudio(blob) function ...

// function playRecording() {
//     if (recordedAudioBlob) {
//         const audioPlayer = document.getElementById("audioPlayer");
//         audioPlayer.src = URL.createObjectURL(recordedAudioBlob);
//         audioPlayer.play();
//         document.getElementById("playAudio").textContent = "⏸️ Pause";
//     }
// }

// function clearRecording() {
//     recordedAudioBlob = null;
//     document.getElementById("audioPlayer").src = "";
//     document.getElementById("playAudio").disabled = true;
//     document.getElementById("clearAudio").disabled = true;
//     document.getElementById("submitRecording").disabled = true;
//     document.getElementById("recordingStatus").textContent = "Recording cleared.";
// }

// // **UPDATE your existing recording functions:**

// // In startRecording() - add after mediaRecorder.start():
// mediaRecorder.start(1000);  // Record in 1s chunks for smoother playback

// // In mediaRecorder.onstop = () => { ... } - UPDATE:
// mediaRecorder.onstop = () => {
//     recordedAudioBlob = new Blob(audioChunks, { type: 'audio/webm' });
//     stream.getTracks().forEach(track => track.stop());
    
//     // Enable playback buttons
//     document.getElementById("playAudio").disabled = false;
//     document.getElementById("clearAudio").disabled = false;
//     document.getElementById("submitRecording").disabled = false;
//     document.getElementById("recordingStatus").textContent = "Ready! 🎵 Click Play or Submit.";
// };

// // **File upload - also enable playback:**
// async function processFileUpload() {
//     const fileInput = document.getElementById("audioFile");
//     if (!fileInput.files.length) return;
    
//     recordedAudioBlob = fileInput.files[0];  // Enable playback for uploaded files
//     document.getElementById("playAudio").disabled = false;
//     document.getElementById("clearAudio").disabled = false;
    
//     processAudio(recordedAudioBlob);
// }

// // **ADD EVENT LISTENERS** (at bottom of main.js)
// document.getElementById("playAudio").onclick = function() {
//     if (this.textContent.includes("Pause")) {
//         document.getElementById("audioPlayer").pause();
//         this.textContent = "▶️ Play Recording";
//     } else {
//         playRecording();
//     }
// };

// document.getElementById("clearAudio").onclick = clearRecording;

let mediaRecorder, audioChunks = [], recordedAudioBlob = null, isRecording = false;

async function processAudio(blob) {
    const formData = new FormData();
    formData.append("audio", blob, "recording.webm");

    try {
        const response = await fetch("http://127.0.0.1:6767/process_audio", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        
        const data = await response.json();
        document.getElementById("finalResultOutput").textContent = data.result;
        document.getElementById("recordingStatus").textContent = 
            `Result: ${data.result} (${data.interpretation || (parseFloat(data.result) > 0.5 ? "Parkinson's" : "Healthy")})`;
    } catch (err) {
        console.error(err);
        document.getElementById("finalResultOutput").textContent = "Error: " + err;
    }
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
        
        mediaRecorder.onstop = () => {
            recordedAudioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            stream.getTracks().forEach(track => track.stop());
            
            // Enable ALL buttons
            document.getElementById("playAudio").disabled = false;
            document.getElementById("clearAudio").disabled = false;
            document.getElementById("submitRecording").disabled = false;
            document.getElementById("recordingStatus").textContent = "✅ Ready! Click Play or Submit.";
        };

        mediaRecorder.start(1000);  // 1s chunks
        isRecording = true;
        
        document.getElementById("startRecord").disabled = true;
        document.getElementById("stopRecord").disabled = false;
        document.getElementById("recordingStatus").textContent = "🎤 Recording... Speak now!";
        
    } catch (err) {
        console.error("Mic error:", err);
        document.getElementById("finalResultOutput").textContent = "Microphone access denied.";
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        document.getElementById("startRecord").disabled = false;
        document.getElementById("stopRecord").disabled = true;
    }
}

function submitRecording() {
    if (recordedAudioBlob) {
        document.getElementById("recordingStatus").textContent = "🔬 Analyzing...";
        processAudio(recordedAudioBlob);
    }
}

function playRecording() {
    if (recordedAudioBlob) {
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = URL.createObjectURL(recordedAudioBlob);
        audioPlayer.play();
        document.getElementById("playAudio").textContent = "⏸️ Pause";
    }
}

function clearRecording() {
    recordedAudioBlob = null;
    document.getElementById("audioPlayer").src = "";
    document.getElementById("playAudio").disabled = true;
    document.getElementById("clearAudio").disabled = true;
    document.getElementById("submitRecording").disabled = true;
    document.getElementById("recordingStatus").textContent = "🗑️ Cleared. Start new recording.";
}

// File upload
async function processFileUpload() {
    const fileInput = document.getElementById("audioFile");
    if (!fileInput.files.length) return;
    
    recordedAudioBlob = fileInput.files[0];
    document.getElementById("playAudio").disabled = false;
    document.getElementById("clearAudio").disabled = false;
    processAudio(recordedAudioBlob);
}

// 🎛️ EVENT LISTENERS (CRITICAL)
document.getElementById("startRecord").onclick = startRecording;
document.getElementById("stopRecord").onclick = stopRecording;
document.getElementById("submitRecording").onclick = submitRecording;
document.getElementById("audioFile").onchange = processFileUpload;
document.getElementById("playAudio").onclick = function() {
    if (this.textContent.includes("Pause")) {
        document.getElementById("audioPlayer").pause();
        this.textContent = "▶️ Play Recording";
    } else {
        playRecording();
    }
};
document.getElementById("clearAudio").onclick = clearRecording;
