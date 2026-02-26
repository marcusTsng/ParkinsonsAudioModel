# """SETUP"""
# # Flask - js/py bridge imports and setup
# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)

# # Other imports
# from data_extraction import get_training_data, get_testing_data, set_training_ratio
# from machine_learning import Model
# # Variables/Constants
# PERCENTAGE_TRAINING_RATIO = 70

# # Fetching data
# set_training_ratio(PERCENTAGE_TRAINING_RATIO)
# X_train, y_train = get_training_data()
# X_test, y_test = get_testing_data()

# # Loading ai model
# model = Model()
# model.train(X_train, y_train)

# """FUNCTIONS"""
# # Audio processing
# def get_data_from_audio(file):
#     data = file.read()
#     out = model.process_data(data)
#     return out 

# """FLASK CONNECTION (JS/PY BRIDGE)"""
# @app.route("/process_audio", methods=["POST"])
# def process_audio_route():
#     if "audio" not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     audio_file = request.files["audio"]
#     if audio_file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     filename = secure_filename(audio_file.filename)
#     # Optional: save file if you want
#     # audio_file.save(f"./uploads/{filename}")

#     result = get_data_from_audio(audio_file)
#     return jsonify({"result": result})

# """TESTS AND DEBUGGING"""
# if __name__ == "__main__":
#     app.run(debug=True)

#     # Interface
#     print("\n\n}---{MODEL TRAINING INTERFACE}---{")
#     selection = input("Run test training for model? (y/n): ")
#     if selection.lower() == "y":
#         percentage_training_data = float(input("Percentage used as training data /% (0-100): "))

#         # Data extraction 
#         set_training_ratio(percentage_training_data)
#         X_train, y_train = get_training_data()
#         X_test, y_test = get_testing_data()

#         # Model training
#         model = Model()
#         model.train(X_train, y_train)
#         print("\n\n}---{STATISTICS}---{")
#         model.test(X_test, y_test, 0.8)

"""SETUP"""
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Imports
from data_extraction import get_training_data, get_testing_data, set_training_ratio, extract_features_from_audio
from machine_learning import Model

# Constants
PERCENTAGE_TRAINING_RATIO = 0.8

# Load model
print("🔄 Loading Parkinson's model...")
set_training_ratio(PERCENTAGE_TRAINING_RATIO * 100)
X_train, y_train = get_training_data()
X_test, y_test = get_testing_data()

model = Model()
model.train(X_train, y_train)
print("✅ Model trained! Accuracy:", model.test(X_test, y_test, 0.8))


"""FUNCTIONS"""
def get_data_from_audio(file):
    """Audio bytes → Parkinson's probability"""
    try:
        audio_bytes = file.read()
        print(f"🎤 Processing audio: {len(audio_bytes)} bytes")
        
        features = extract_features_from_audio(audio_bytes)
        print(f"📊 Features shape: {features.shape}")
        
        probability = model.process_data(features)
        return probability
    except Exception as e:
        print(f"❌ Error: {e}")
        return "0.50"

"""FLASK API"""
@app.route("/process_audio", methods=["POST"])
def process_audio_route():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    result = get_data_from_audio(audio_file)
    return jsonify({"result": result, "interpretation": "Parkinson's" if float(result) > 0.5 else "Healthy"})

@app.route("/")
def home():
    return "Parkinson's Audio Detector API - POST to /process_audio"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6767)
