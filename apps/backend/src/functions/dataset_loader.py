import pandas as pd
import re
from rapidfuzz import fuzz, process

DATASET_PATH = "C:/Users/USUARIO/Desktop/Projects/mood_tune_back/src/data/final_df.csv"
df_dataset = None

def load_dataset():
    global df_dataset
    if df_dataset is None:
        df_dataset = pd.read_csv(
            DATASET_PATH,
            usecols=["song_name", "artist_name", "recording_id", "danceable", "male", "timbre_bright", 
                     "tonal", "instrumental", "mood_acoustic", "mood_aggressive", "mood_electronic", 
                     "mood_happy", "mood_party", "mood_relaxed", "mood_sad", "combined_genres"],
            dtype={
                "danceable": float,
                "male": float,
                "timbre_bright": float,
                "tonal": float,
                "instrumental": float,
                "mood_acoustic": float,
                "mood_aggressive": float,
                "mood_electronic": float,
                "mood_happy": float,
                "mood_party": float,
                "mood_relaxed": float,
                "mood_sad": float
            }
        )
        df_dataset = df_dataset.dropna(subset=["song_name", "artist_name"])
        df_dataset["song_name"] = df_dataset["song_name"].apply(normalize_string)
        df_dataset["artist_name"] = df_dataset["artist_name"].apply(normalize_string)
    return df_dataset

def normalize_string(text):
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text

def check_songs_in_dataset(user_songs, threshold=85):
    df_dataset = load_dataset()

    dataset_dict = {
        (row['song_name'], row['artist_name']): row.to_dict()
        for _, row in df_dataset.iterrows()
    }

    dataset_song_artist = list(dataset_dict.keys())

    matching_songs = []
    for song in user_songs:
        if "name" not in song or "artists" not in song:
            continue

        song_name = normalize_string(song["name"])
        artist_name = normalize_string(song["artists"][0]["name"])
        song_query = (song_name, artist_name)

        match = process.extractOne(song_query, dataset_song_artist, scorer=fuzz.ratio)
        if match:
            best_match, score = match[:2]

            if best_match and score >= threshold:
                dataset_data = dataset_dict.get(best_match, {})

                matching_songs.append({
                    "spotify_data": {
                        "original_name": song["name"],
                        "artist": song["artists"][0]["name"],
                        "album": song["album"]["name"],
                        "duration_ms": song["duration_ms"],
                        "popularity": song["popularity"],
                        "spotify_url": song["external_urls"]["spotify"],
                        "picture": song["album"]["images"][0]["url"]
                    },
                    "dataset_data": dataset_data
                })

    return matching_songs


def check_artists_in_dataset(user_artists, threshold=85):
    df_dataset = load_dataset()

    dataset_artists = df_dataset["artist_name"].tolist()

    matching_artists = []
    for artist in user_artists:
        artist_name = normalize_string(artist.get("name", ""))

        match = process.extractOne(artist_name, dataset_artists, scorer=fuzz.ratio)
        if match:
            best_match, score = match[:2]

            if score >= threshold:
                matching_artists.append(artist)

    return matching_artists
