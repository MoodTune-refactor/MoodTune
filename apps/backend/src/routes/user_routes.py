from flask import Blueprint, request, jsonify, session
import numpy as np

bp = Blueprint('user_routes', __name__, url_prefix='/user')

PARAMS = [
    "danceable", "instrumental", "male", "mood_acoustic", "mood_aggressive",
    "mood_electronic", "mood_happy", "mood_party", "mood_relaxed", "mood_sad",
    "timbre_bright", "tonal"
]

@bp.route('/store-tracks', methods=['POST'])
def store_tracks():
    data = request.get_json()

    if not data or "tracks" not in data:
        return jsonify({"error": "No se enviaron tracks"}), 400

    if "filtered_tracks" not in session:
        session["filtered_tracks"] = []

    session["filtered_tracks"].extend(data["tracks"])
    session.modified = True

    return jsonify({"message": "Tracks almacenados en la sesión"}), 200

@bp.route('/user/preferences', methods=['GET'])
def get_user_preferences():
    if "filtered_tracks" not in session or not session["filtered_tracks"]:
        return jsonify({"error": "No hay tracks almacenados en la sesión"}), 400

    tracks = session["filtered_tracks"]

    param_values = {param: [] for param in PARAMS}

    for track in tracks:
        dataset_data = track.get("dataset_data", {})
        for param in PARAMS:
            value = dataset_data.get(param)
            if value is not None:
                param_values[param].append(float(value))

    user_preferences = {}
    for param, values in param_values.items():
        if values:
            max_val = np.max(values)
            min_val = np.min(values)
            user_preferences[param] = (((1 - (max_val - min_val)) ** 2) * 100)
        else:
            user_preferences[param] = 0

    return jsonify({"user_preferences": user_preferences}), 200

@bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to MoodTune"}), 200

