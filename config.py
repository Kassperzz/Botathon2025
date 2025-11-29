import os
from urllib.parse import quote_plus

class Config:
    # 1. Credenciales (Ajusta esto si cambia tu configuración local)
    DB_USER = 'postgres'
    DB_PASS = 'root'      # ¿Estás seguro de que lleva '!'? A veces es solo 'root'
    DB_HOST = '127.0.0.1'
    DB_PORT = '5432'
    DB_NAME = 'botathon'   # Asegúrate de que esta DB exista en pgAdmin

    # 2. Codificamos la contraseña para evitar errores con caracteres especiales
    encoded_password = quote_plus(DB_PASS)

    # 3. Construimos la URI
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_clave_secreta_super_segura'