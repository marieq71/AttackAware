from models import db, User
from flask import flash

class Admin:
    @staticmethod
    def promote_to_admin(user_id):
        user = User.query.get(user_id)
        if user:
            user.is_admin = True
            db.session.commit()
            return f"{user.firstName} {user.lastName} has been granted admin privileges."
        else:
            return "User not found."
