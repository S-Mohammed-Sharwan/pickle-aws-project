"""
WSGI Entry Point for Production Deployment
Use with gunicorn on AWS EC2:
    gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4
"""

from app import create_app

app = create_app()
