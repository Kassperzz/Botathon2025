# run.py
import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db, login_manager
from app.models import User
import click

# Crear la app (usa la configuración por defecto definida en create_app)
app = create_app()


if __name__ == "__main__":
    # Puerto configurable vía env PORT, por defecto 5000
    port = int(os.getenv("PORT", 5000))
    debug = app.config.get("DEBUG", False)
    app.run(host="0.0.0.0", port=port, debug=debug)
