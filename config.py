import os
from dotenv import load_dotenv

load_dotenv()  # carga .env automáticamente

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # URL de conexión a PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/mydatabase"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Opcional: SSL para producción (Heroku, Railway, Render)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            # activar sólo si tu proveedor lo requiere
            # "sslmode": "require"
        }
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
