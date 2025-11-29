from flask_login import UserMixin
from app.extensions import db, login_manager
from app.utils import NOMBRES_REGIONES

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(256))

class Voluntario(db.Model):
    __tablename__ = 'voluntarios'
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(150))
    apellido_paterno = db.Column(db.String(100))
    ocupacion = db.Column(db.String(255))
    region_id = db.Column(db.Integer)
    sexo_id = db.Column(db.Integer)
    
    def to_json(self):
        nombre_region = NOMBRES_REGIONES.get(self.region_id, f"Región {self.region_id}")
        return {
            'id': self.id,
            'nombre_completo': f"{self.nombres} {self.apellido_paterno}",
            'ocupacion': self.ocupacion,
            'region': nombre_region
        }

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))