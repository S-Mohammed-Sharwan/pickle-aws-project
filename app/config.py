"""
Application Configuration
Contains all configuration settings for the Flask app.
Includes AWS DynamoDB placeholders for cloud deployment.
"""

import os


class Config:
    """Base configuration class."""

    # ── Flask Core ─────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "homemade-pickles-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", True)

    # ── Session Configuration ──────────────────────────────────────────
    SESSION_TYPE = "filesystem"  # Use 'filesystem' for local, 'dynamodb' for AWS
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flask_session")

    # ── AWS Configuration (for DynamoDB integration) ───────────────────
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")

    # ── DynamoDB Table Names ───────────────────────────────────────────
    DYNAMODB_PRODUCTS_TABLE = os.environ.get("DYNAMODB_PRODUCTS_TABLE", "HomemadePickles_Products")
    DYNAMODB_USERS_TABLE = os.environ.get("DYNAMODB_USERS_TABLE", "HomemadePickles_Users")
    DYNAMODB_ORDERS_TABLE = os.environ.get("DYNAMODB_ORDERS_TABLE", "HomemadePickles_Orders")

    # ── Feature Flags ──────────────────────────────────────────────────
    USE_DYNAMODB = os.environ.get("USE_DYNAMODB", "false").lower() == "true"
