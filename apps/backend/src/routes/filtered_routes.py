from flask import Blueprint, jsonify, request, session
from flask_cors import CORS
from src.functions.dataset_loader import check_songs_in_dataset, check_artists_in_dataset

filtered_bp = Blueprint("filtered", __name__, url_prefix="/filter")

CORS(filtered_bp, supports_credentials=True, origins=["http://localhost:5173"])

def almacenar_canciones_en_sesion(nuevas_canciones):
    if "filtered_tracks" not in session:
        session["filtered_tracks"] = []

    session["filtered_tracks"].extend(nuevas_canciones)
    session.modified = True

@filtered_bp.route("/filtered-top-tracks", methods=["POST"])
def filtered_top_tracks():
    try:
        data = request.get_json()

        if not data or "tracks" not in data:
            return jsonify({"error": "No data provided"}), 400

        user_tracks = data.get("tracks", [])
        filtered_tracks = check_songs_in_dataset(user_tracks)

        almacenar_canciones_en_sesion(filtered_tracks)

        return jsonify({"filtered_tracks": filtered_tracks}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@filtered_bp.route("/filtered-favourite-tracks", methods=["POST"])
def filtered_favourite_tracks():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_tracks = data.get("tracks", [])
    filtered_tracks = check_songs_in_dataset(user_tracks)

    almacenar_canciones_en_sesion(filtered_tracks)

    return jsonify({"filtered_tracks": filtered_tracks}), 200

@filtered_bp.route("/filtered-followed-artists", methods=["POST"])
def filtered_followed_artists():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_artists = data.get("artists", [])
    filtered_artists = check_artists_in_dataset(user_artists)

    return jsonify({"filtered_artists": filtered_artists}), 200

@filtered_bp.route("/get-filtered-tracks", methods=["GET"])
def get_filtered_tracks():
    print("📢 Recuperando de sesión:", session.get("filtered_tracks", "No session data"))
    return jsonify({"filtered_tracks": session.get("filtered_tracks", [])}), 200


@filtered_bp.route('/filter/debug-session', methods=['GET'])
def debug_session():
    return jsonify(session.get("filtered_tracks", "No session data"))
