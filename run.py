from app import create_app

# Crea la aplicación
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)