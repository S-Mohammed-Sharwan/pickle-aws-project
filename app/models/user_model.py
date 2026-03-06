"""
User Model
Manages user accounts using local Python dictionaries.
Includes comments showing how to switch to DynamoDB.
"""

import hashlib
import uuid

# ══════════════════════════════════════════════════════════════════════════
# LOCAL DICTIONARY STORAGE (Development)
# Replace with DynamoDB calls when deploying to AWS (see comments below).
# ══════════════════════════════════════════════════════════════════════════

USERS = {}

# Pre-seed an admin user (password: admin123)
_admin_password_hash = hashlib.sha256("admin123".encode()).hexdigest()
USERS["admin"] = {
    "id": "admin",
    "username": "admin",
    "email": "admin@homemadepickles.com",
    "password": _admin_password_hash,
    "full_name": "Admin User",
    "is_admin": True,
}


def _hash_password(password):
    """Hash a password using SHA-256. In production, use bcrypt or argon2."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, email, password, full_name=""):
    """
    Register a new user.
    Returns the user dict on success, or None if username already exists.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # try:
    #     dynamodb_tables['users'].put_item(
    #         Item={...},
    #         ConditionExpression='attribute_not_exists(username)'
    #     )
    # except ClientError as e:
    #     if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
    #         return None
    """
    if username in USERS:
        return None

    user_id = str(uuid.uuid4())[:8]
    user = {
        "id": user_id,
        "username": username,
        "email": email,
        "password": _hash_password(password),
        "full_name": full_name,
        "is_admin": False,
    }
    USERS[username] = user
    # Return user without password hash
    return {k: v for k, v in user.items() if k != "password"}


def authenticate_user(username, password):
    """
    Authenticate a user by username and password.
    Returns the user dict (without password) on success, or None on failure.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['users'].get_item(Key={'username': username})
    # user = response.get('Item')
    # if user and user['password'] == _hash_password(password):
    #     return {k: v for k, v in user.items() if k != 'password'}
    # return None
    """
    user = USERS.get(username)
    if not user:
        return None
    if user["password"] != _hash_password(password):
        return None
    # Return user without password hash
    return {k: v for k, v in user.items() if k != "password"}


def get_user(username):
    """
    Retrieve a user by username (without the password hash).
    Returns the user dict or None if not found.

    # DynamoDB equivalent:
    # from app.extensions import dynamodb_tables
    # response = dynamodb_tables['users'].get_item(Key={'username': username})
    # user = response.get('Item')
    # if user:
    #     return {k: v for k, v in user.items() if k != 'password'}
    # return None
    """
    user = USERS.get(username)
    if user:
        return {k: v for k, v in user.items() if k != "password"}
    return None


def is_admin(username):
    """Check if a user is an admin."""
    user = USERS.get(username)
    return user.get("is_admin", False) if user else False
