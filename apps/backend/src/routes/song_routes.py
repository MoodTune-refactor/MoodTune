from flask import Blueprint, jsonify, request
from src.functions.song_search import search_songs
from src.models.model_loader import model_data  # Se obtiene el DataFrame, índice y modelo
import pandas as pd

bp = Blueprint("song_routes", __name__, url_prefix="/songs")

# Utilizamos el DataFrame cargado en model_data en lugar de leer el CSV de nuevo.
df = model_data["df"]

# Función para filtrar el dataset según los géneros seleccionados
def filtrar_por_genero(df, generos):
    if not generos:  # Si `generos` está vacío, devolvemos todo el dataset
        return df
    df_filtrado = df[df["combined_genres"].apply(lambda x: any(gen in str(x).lower() for gen in generos))]
    return df_filtrado if not df_filtrado.empty else df  # Si el filtrado queda vacío, devolvemos el dataset original

# Función para calcular la tasa de diferencia entre las canciones de referencia
def calcular_tasa_diferencia_referencias(referencias, columnas_parametros):
    diferencias = []
    canciones_referencia = []
    promedio_diferencias = {}

    # Extraer la información de cada canción de referencia
    for referencia in referencias:
        cancion_data = referencia["dataset_data"]
        canciones_referencia.append(referencia)  # Guardamos la referencia completa
        promedio_diferencias[cancion_data["song_name"]] = 0

    # Comparar todas las canciones de referencia entre sí
    for i in range(len(canciones_referencia)):
        for j in range(i + 1, len(canciones_referencia)):
            song_1 = canciones_referencia[i]["dataset_data"]
            song_2 = canciones_referencia[j]["dataset_data"]
            diferencia_total = 0

            for columna in columnas_parametros:
                valor_1 = song_1[columna] * 10
                valor_2 = song_2[columna] * 10
                diferencia_total += (abs(valor_1 - valor_2)) ** 2

            diferencias.append({
                "song_1": song_1["song_name"],
                "artist_1": song_1["artist_name"],
                "song_2": song_2["song_name"],
                "artist_2": song_2["artist_name"],
                "tasa_diferencia": diferencia_total
            })

            # Acumular diferencias para el promedio
            promedio_diferencias[song_1["song_name"]] += diferencia_total
            promedio_diferencias[song_2["song_name"]] += diferencia_total

    # Calcular el promedio de diferencia para cada canción
    for cancion in promedio_diferencias:
        promedio_diferencias[cancion] /= (len(canciones_referencia) - 1)

    # Convertir a DataFrame y ordenar
    diferencias_df = pd.DataFrame(diferencias)
    diferencias_df.sort_values(by="tasa_diferencia", ascending=True, inplace=True)

    # Crear DataFrame con promedios y ordenarlo
    promedio_df = pd.DataFrame(list(promedio_diferencias.items()), columns=["song_name", "promedio_diferencia"])
    promedio_df.sort_values(by="promedio_diferencia", ascending=True, inplace=True)

    # Obtener la lista ordenada de canciones con su estructura completa
    canciones_ordenadas = []
    for _, row in promedio_df.iterrows():
        song_name = row["song_name"]
        cancion_completa = next(ref for ref in canciones_referencia if ref["dataset_data"]["song_name"] == song_name)
        canciones_ordenadas.append(cancion_completa)

    return diferencias_df, canciones_ordenadas

# Endpoint para obtener canción basada en el estado de ánimo
@bp.route("/mood", methods=["POST"])
def get_songs_by_mood():
    """
    Endpoint para buscar canciones basadas en el estado de ánimo del usuario.
    Recibe un JSON con la clave 'moodText'.
    """
    data = request.get_json()
    if not data or "moodText" not in data:
        return jsonify({"error": "Falta el parámetro 'moodText'"}), 400

    mood_text = data["moodText"]
    songs = search_songs(mood_text, top_n=10)
    return jsonify(songs)

# Endpoint para obtener canción más cercana a las demás (ranking central)
@bp.route("/rank-central-songs", methods=["POST"])
def rank_central_songs():
    try:
        data = request.get_json()
        if not data or "references" not in data or "importances" not in data:
            return jsonify({"error": "Invalid input format"}), 400

        referencias = data["references"]
        importancias = data["importances"]
        if not referencias or not isinstance(importancias, dict):
            return jsonify({"error": "Invalid references or importances format"}), 400

        # Obtener columnas de parámetros a partir del diccionario de importancias
        columnas_parametros = list(importancias.keys())
        # Calcular la centralidad de las canciones
        _, canciones_ordenadas = calcular_tasa_diferencia_referencias(referencias, columnas_parametros)
        return jsonify({"ordered_tracks": canciones_ordenadas}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Función para calcular la disonancia ponderada
def calcular_disonancia(row, referencia, importancias):
    disonancia_total = 0
    for columna, valor_referencia in referencia.items():
        importancia = importancias.get(columna, 1)  # Si no hay importancia definida, se usa 1
        diferencia = abs(row[columna] - valor_referencia)
        disonancia_total += diferencia * importancia
    return disonancia_total

# Función para obtener rankings de disonancia
def obtener_ranking(df, referencia, importancias, nombre_columna_ranking):
    df[nombre_columna_ranking] = df.apply(lambda row: calcular_disonancia(row, referencia, importancias), axis=1)
    df.sort_values(by=nombre_columna_ranking, ascending=True, inplace=True)
    df[nombre_columna_ranking + '_rank'] = range(1, len(df) + 1)
    return df

# Función para obtener el top 10 de canciones menos disonantes basado en las preferencias del usuario
def obtener_top_10_por_preferencias(df, preferencias_usuario, importancias):
    # Convertir las preferencias en un diccionario de referencia (normalizando a 0-1)
    referencia = {k: v / 100 for k, v in preferencias_usuario.items()}
    df_ranking = obtener_ranking(df.copy(), referencia, importancias, "disonancia_usuario")
    top_10 = df_ranking.head(10)
    top_10_json = top_10[[ 
        "artist_name", "song_name", "recording_id", "danceable", "instrumental", "male", "mood_acoustic",
        "mood_aggressive", "mood_electronic", "mood_happy", "mood_party", "mood_relaxed", "mood_sad",
        "timbre_bright", "tonal", "spotify_url", "album_name", "duration_ms", "combined_genres"
    ]].rename(columns={
        "album_name": "album",
        "artist_name": "artist"
    }).to_dict(orient="records")
    return top_10_json

# Endpoint para obtener recomendaciones de canciones según las preferencias del usuario
@bp.route("/recommendations", methods=["POST"])
def get_song_recommendations():
    try:
        data = request.get_json()
        if not data or "preferences" not in data or "importances" not in data:
            return jsonify({"error": "Invalid input format. Expected 'preferences' and 'importances'."}), 400

        preferencias_usuario = data["preferences"]
        importancias = data["importances"]

        if not isinstance(preferencias_usuario, dict) or not isinstance(importancias, dict):
            return jsonify({"error": "Invalid format. 'preferences' and 'importances' should be dictionaries."}), 400

        top_10_canciones_json = obtener_top_10_por_preferencias(df, preferencias_usuario, importancias)
        return jsonify({"recommended_tracks": top_10_canciones_json}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
