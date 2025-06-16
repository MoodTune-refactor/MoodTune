import numpy as np
import time
from deep_translator import GoogleTranslator
from langdetect import detect
from src.models.model_loader import model_data  # Usa el modelo, índice y dataframe cargados

def translate_to_english(text):
    try:
        if text and isinstance(text, str) and text.strip():
            if detect(text) != 'en':
                return GoogleTranslator(source='auto', target='en').translate(text)
        return text
    except Exception as e:
        print(f"❌ Error detectando idioma: {e}")
        return text

def translate_to_spanish(text):
    try:
        if text and isinstance(text, str) and text.strip():
            return GoogleTranslator(source='en', target='es').translate(text[:499])
        return "Traducción no disponible"
    except Exception as e:
        print(f"❌ Error traduciendo texto: {e}")
        return "Traducción no disponible"

def search_songs(user_query, top_n=1):
    start_time = time.time()
    
    # Traducir la consulta a inglés si es necesario.
    translated_query = translate_to_english(user_query)
    
    # Generar el embedding de la consulta usando el modelo cargado.
    model = model_data["model"]
    query_embedding = model.encode(translated_query, convert_to_tensor=True).cpu().numpy().astype('float32')
    
    # Realizar la búsqueda en el índice FAISS.
    index = model_data["index"]
    distances, indices = index.search(np.array([query_embedding]), top_n)
    
    # Si no se obtuvieron resultados, devolver un valor por defecto.
    if not indices.any():
        print("❌ No se encontraron resultados, devolviendo valor por defecto.")
        return [{
            "artist_name": "Error",
            "song_name": "No se encontraron canciones",
            "spotify_url": "",
            "processed_lyrics": "No hay letra disponible",
            "translated_lyrics": "Traducción no disponible",
            "similarity": 0
        }]
    
    # Obtener las canciones más similares del DataFrame.
    df = model_data["df"]
    top_songs = df.iloc[indices[0]].copy()
    top_songs['similarity'] = 1 - distances[0]  # Ajuste de similitud, según la métrica de FAISS
    
    # Procesar las letras (recortar a 499 caracteres y traducir si es posible).
    if "processed_lyrics" in top_songs.columns:
        top_songs['processed_lyrics'] = top_songs['processed_lyrics'].apply(
            lambda x: (x[:499] + "...") if isinstance(x, str) and x.strip() else "No hay letra disponible"
        )
        top_songs['translated_lyrics'] = top_songs['processed_lyrics'].apply(
            lambda x: translate_to_spanish(x) if x != "No hay letra disponible" else "Traducción no disponible"
        )
    else:
        top_songs['processed_lyrics'] = "No hay letra disponible"
        top_songs['translated_lyrics'] = "Traducción no disponible"
    
    print(f"⏱ Búsqueda completada en {time.time() - start_time:.4f} segundos.")
    return top_songs[['artist_name', 'song_name', 'spotify_url', 'processed_lyrics', 'translated_lyrics', 'similarity']].to_dict(orient="records")
