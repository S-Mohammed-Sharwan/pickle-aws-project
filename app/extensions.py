"""
Extensions Module
Initializes Flask extensions and optional AWS DynamoDB connections.
"""

# Global DynamoDB resource placeholder (initialized when USE_DYNAMODB is True)
dynamodb = None
dynamodb_tables = {}


def init_extensions(app):
    """
    Initialize all extensions for the Flask application.
    Sets up session management and optional DynamoDB connection.
    """
    global dynamodb, dynamodb_tables

    # ── Session Management ─────────────────────────────────────────────
    from flask_session import Session
    Session(app)

    # ── DynamoDB Integration (Optional) ────────────────────────────────
    if app.config.get("USE_DYNAMODB", False):
        try:
            import boto3

            dynamodb = boto3.resource(
                "dynamodb",
                region_name=app.config["AWS_REGION"],
                aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
            )

            # Initialize table references
            dynamodb_tables["products"] = dynamodb.Table(app.config["DYNAMODB_PRODUCTS_TABLE"])
            dynamodb_tables["users"] = dynamodb.Table(app.config["DYNAMODB_USERS_TABLE"])
            dynamodb_tables["orders"] = dynamodb.Table(app.config["DYNAMODB_ORDERS_TABLE"])

            app.logger.info("✅ Connected to AWS DynamoDB successfully.")
        except Exception as e:
            app.logger.error(f"❌ Failed to connect to DynamoDB: {e}")
            dynamodb = None
    else:
        app.logger.info("📦 Using local dictionary storage (DynamoDB disabled).")
