from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy import text

# Configuración mínima para conectar a la BD
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Enaxxion13!@127.0.0.1:5432/botathon2025'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definimos la tabla de admins
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

def inicializar_admin():
    with app.app_context():
        # 1. Crear la tabla si no existe
        db.create_all()
        print("✅ Tabla 'admins' verificada.")

        # 2. Crear un usuario admin (si no existe)
        if not Admin.query.filter_by(username='admin').first():
            # ENCRIPTAMOS la contraseña '1234'
            pass_encriptada = generate_password_hash('1234')
            
            nuevo_admin = Admin(username='admin', password_hash=pass_encriptada)
            db.session.add(nuevo_admin)
            db.session.commit()
            print("✅ Usuario 'admin' creado con contraseña '1234'.")
        else:
            print("ℹ️ El usuario 'admin' ya existe.")

if __name__ == '__main__':
    inicializar_admin()