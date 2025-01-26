from models import db, User
from werkzeug.security import generate_password_hash
import os

admin_email = os.getenv('ADMIN_EMAIL', 'admin@admin.com')
admin_password = os.getenv('ADMIN_PASSWORD', 'admin')


def create_initial_admin():
    # Check if an admin already exists
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        return

    # If no admin exists, create one
    admin_user = User(
        firstName='Admin',
        lastName='User',
        email=admin_email,
        password=generate_password_hash(admin_password),
        is_admin=True
    )
    db.session.add(admin_user)
    db.session.commit()
