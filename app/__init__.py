from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=False)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(Config)

    # 1. Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
   

    # Configuración de Login (Redirección si no está logueado)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Inicia sesión para continuar.'

    # 2. Registrar Blueprints (Importaciones corregidas)
    # Usamos los nombres reales definidos en cada __init__.py (auth_bp, dashboard_bp, etc.)
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.users import users_bp
    from app.blueprints.api import api_bp
    from app.blueprints.items import items_bp

    # 3. Registrar con prefijos
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')      # Raíz -> Dashboard
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(items_bp, url_prefix='/items')

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app