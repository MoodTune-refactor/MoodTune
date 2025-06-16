from src.models.models import db, User, FavoriteTrack
from datetime import datetime

def save_user_and_tracks(user_data, tracks_data):
    user = User(
        id=user_data['id'],
        display_name=user_data.get('display_name'),
        email=user_data.get('email')
    )
    db.session.merge(user)

    for track in tracks_data:
        favorite_track = FavoriteTrack(
            user_id=user_data['id'],
            track_id=track['id'],
            track_name=track['name'],
            artist_name=', '.join(artist['name'] for artist in track['artists']),
            album_name=track['album']['name'],
            added_at=datetime.now()
        )
        db.session.add(favorite_track)

    db.session.commit()
