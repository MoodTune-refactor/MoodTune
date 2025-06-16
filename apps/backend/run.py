from src import create_app

app = create_app()

# Imprimir todas las rutas registradas
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule}")

if __name__ == "__main__":
    app.run(debug=True)
