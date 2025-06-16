from flask import Blueprint, redirect, request, jsonify
from src.functions.auth import (
    build_auth_url,
    exchange_code_for_token,
    refresh_access_token,
    is_code_used,
    mark_code_as_used,
)

# Create Blueprint for routes
login_bp = Blueprint("login", __name__)

# Endpoint for redirect usert to auth
@login_bp.route("/login", methods=["GET"])
def login():
    try:
        # Make the auth Spotify URL
        auth_url = build_auth_url()
        return redirect(auth_url)
    except Exception as e:
        return jsonify({"error": "Failed to build authentication URL", "details": str(e)}), 500

# Callback for receiving the autorization token from Spotify
@login_bp.route("/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No authorization code provided"}), 400

    if is_code_used(code):
        return jsonify({"error": "Authorization code already used"}), 400

    # Set code as used
    mark_code_as_used(code)

    # Exchange tokens
    try:
        token_info = exchange_code_for_token(code)
    except Exception as e:
        return jsonify({"error": "Failed to fetch access token", "details": str(e)}), 500

    # Verify errors on Spotify request
    if "error" in token_info:
        return jsonify({"error": "Failed to fetch access token", "details": token_info}), 400

    return jsonify({
        "access_token": token_info.get("access_token"),
        "refresh_token": token_info.get("refresh_token"),
        "expires_in": token_info.get("expires_in"),
        "scope": token_info.get("scope"),
    })

# Endpoint for refresh access token
@login_bp.route("/refresh", methods=["POST"])
def refresh_token():
    refresh_token = request.json.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "No refresh token provided"}), 400

    # Refresh access token
    try:
        new_tokens = refresh_access_token(refresh_token)
    except Exception as e:
        return jsonify({"error": "Failed to refresh token", "details": str(e)}), 500

    # Verificar si hay errores en la respuesta de Spotify
    if "error" in new_tokens:
        return jsonify({"error": "Failed to refresh token", "details": new_tokens}), 400

    # Devolver los nuevos tokens al cliente
    return jsonify({
        "access_token": new_tokens.get("access_token"),
        "expires_in": new_tokens.get("expires_in"),
        "scope": new_tokens.get("scope"),
    })
