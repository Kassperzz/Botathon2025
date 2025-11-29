# app/__init__.py
from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager

def create_app(config_object: str = None):
    app = Flask(__name__, instance_relative_config=False)

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Registrar blueprints (imports absolutos)
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.dashboard import bp as dashboard_bp
    from app.blueprints.admin import bp as admin_bp
    from app.blueprints.users import bp as users_bp
    from app.blueprints.api import bp as api_bp
    from app.blueprints.items import bp as items_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='')      # raíz -> dashboard
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(items_bp)  # prefijo '' -> usa rutas tal cual (/items)


    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app
