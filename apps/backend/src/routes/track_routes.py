from flask import Blueprint, jsonify, request
from src.models.models import FavoriteTrack

bp = Blueprint('track_routes', __name__, url_prefix='/tracks')

@bp.route('/favorites/<user_id>', methods=['GET'])
def get_favorites(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    favorites = FavoriteTrack.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)

    return jsonify({
        'total': favorites.total,
        'pages': favorites.pages,
        'results': [
            {
                'track_id': track.track_id,
                'track_name': track.track_name,
                'artist_name': track.artist_name,
                'album_name': track.album_name,
                'added_at': track.added_at
            } for track in favorites.items
        ]
    })
