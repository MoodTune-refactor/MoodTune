import os
import pandas as pd
import torch
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Definir rutas basadas en el directorio actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_FILE = os.path.join(BASE_DIR, "lyrics_embeddings_roberta3.pkl")
FAISS_INDEX_FILE = os.path.join(BASE_DIR, "lyrics_embeddings_faiss_IP.index")

# Verificar que el archivo de embeddings exista
if not os.path.exists(EMBEDDINGS_FILE):
    raise FileNotFoundError(f"❌ No se encontró el archivo de embeddings: {EMBEDDINGS_FILE}")

# Cargar el objeto desde el archivo pickle
try:
    loaded_obj = pd.read_pickle(EMBEDDINGS_FILE)
    print("✅ Archivo de embeddings cargado correctamente.")
except Exception as e:
    raise RuntimeError(f"❌ Error al cargar el archivo Pickle: {e}")

# Si el objeto cargado no es un DataFrame, asumimos que es una lista o array
if not isinstance(loaded_obj, pd.DataFrame):
    # Cargar metadata desde el CSV para construir el DataFrame
    METADATA_FILE = os.path.join(os.getcwd(), "src/data/final_df.csv")
    df_metadata = pd.read_csv(METADATA_FILE)
    if len(df_metadata) != len(loaded_obj):
        raise ValueError("El número de embeddings no coincide con el número de filas en el metadata.")
    df = df_metadata.copy()
    # Convertir el array 2D a una lista de arrays 1D
    df['embedding'] = list(loaded_obj)
else:
    df = loaded_obj

# Convertir la columna 'embedding' a arrays NumPy de tipo float32
df['embedding'] = df['embedding'].apply(lambda x: np.array(x, dtype=np.float32))
embeddings = np.stack(df["embedding"].values)

# Cargar o crear el índice FAISS
if os.path.exists(FAISS_INDEX_FILE):
    index = faiss.read_index(FAISS_INDEX_FILE)
    print("✅ FAISS index cargado correctamente.")
else:
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)
    faiss.write_index(index, FAISS_INDEX_FILE)
    print("✅ FAISS index creado y guardado correctamente.")

# Cargar el modelo SentenceTransformer (RoBERTa)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer('sentence-transformers/all-roberta-large-v1', device=device)

# Almacenar los recursos en un diccionario para facilitar el acceso en otros módulos
model_data = {
    "df": df,
    "index": index,
    "model": model
}
