"""
HomeMade Pickles & Snacks - Application Factory
Creates and configures the Flask application using the factory pattern.
"""

from flask import Flask
from .config import Config


def create_app(config_class=Config):
    """
    Application factory function.
    Creates a Flask app instance, loads configuration, and registers all blueprints.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Initialize Extensions ──────────────────────────────────────────
    from .extensions import init_extensions
    init_extensions(app)

    # ── Register Blueprints ────────────────────────────────────────────
    from .routes.auth_routes import auth_bp
    from .routes.product_routes import product_bp
    from .routes.cart_routes import cart_bp
    from .routes.order_routes import order_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)

    return app
