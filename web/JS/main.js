let mediaRecorder, audioChunks = [], recordedAudioBlob = null, isRecording = false;

async function processAudio(blob) {
    const formData = new FormData();
    formData.append("audio", blob, "recording.webm");

    try {
        document.getElementById("recordingStatus").textContent = "🔬 Analyzing...";
        const response = await fetch("http://127.0.0.1:6767/process_audio", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        
        const data = await response.json();
        document.getElementById("finalResultOutput").textContent = data.result;
        document.getElementById("recordingStatus").textContent = 
            `✅ ${data.result} (${data.interpretation || (parseFloat(data.result) > 0.5 ? "Parkinson's" : "Healthy")})`;
    } catch (err) {
        console.error(err);
        document.getElementById("finalResultOutput").textContent = "❌ Error: " + err.message;
        document.getElementById("recordingStatus").textContent = "Analysis failed.";
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
            
            document.getElementById("playAudio").disabled = false;
            document.getElementById("clearAudio").disabled = false;
            document.getElementById("submitRecording").disabled = false;
            document.getElementById("recordingStatus").textContent = "✅ Ready! 🎵 Click Play or Submit.";
        };

        mediaRecorder.start(1000);
        isRecording = true;
        
        document.getElementById("startRecord").disabled = true;
        document.getElementById("stopRecord").disabled = false;
        document.getElementById("recordingStatus").textContent = "🎤 Recording... Speak now!";
        
    } catch (err) {
        console.error("Mic error:", err);
        document.getElementById("finalResultOutput").textContent = "❌ Microphone access denied.";
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
    if (recordedAudioBlob) processAudio(recordedAudioBlob);
}

function togglePlay() {
    const btn = document.getElementById("playAudio");
    const player = document.getElementById("audioPlayer");
    
    if (btn.textContent.includes("Pause")) {
        player.pause();
        btn.textContent = "🔊 Play Recording";
    } else {
        player.src = URL.createObjectURL(recordedAudioBlob);
        player.play();
        btn.textContent = "⏸️ Pause";
    }
}

function clearRecording() {
    recordedAudioBlob = null;
    document.getElementById("audioPlayer").src = "";
    document.getElementById("playAudio").disabled = true;
    document.getElementById("playAudio").textContent = "🔊 Play Recording";
    document.getElementById("clearAudio").disabled = true;
    document.getElementById("submitRecording").disabled = true;
    document.getElementById("recordingStatus").textContent = "🗑️ Cleared. Start new recording.";
}

async function processFileUpload() {
    const fileInput = document.getElementById("audioFile");
    if (!fileInput.files.length) return;
    
    recordedAudioBlob = fileInput.files[0];
    document.getElementById("playAudio").disabled = false;
    document.getElementById("clearAudio").disabled = false;
    processAudio(recordedAudioBlob);
}

// Event listeners
document.getElementById("startRecord").onclick = startRecording;
document.getElementById("stopRecord").onclick = stopRecording;
document.getElementById("submitRecording").onclick = submitRecording;
document.getElementById("playAudio").onclick = togglePlay;
document.getElementById("clearAudio").onclick = clearRecording;
document.getElementById("audioFile").onchange = processFileUpload;
