import sys
from os.path import abspath, dirname

# Añade la raíz del proyecto al PYTHONPATH
project_root = dirname(abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Imprime el PYTHONPATH para verificar
print("PYTHONPATH:", sys.path)

# Importa las funciones y variables necesarias desde src
from src import db, create_app

# Crear la aplicación Flask
app = create_app()

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()
    print("Tablas creadas correctamente.")
