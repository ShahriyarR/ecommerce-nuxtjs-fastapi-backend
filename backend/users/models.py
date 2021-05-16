from backend.app.main import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True)
    username = db.Column(db.Unicode(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean(), nullable=True, server_default="True")
    salt = db.Column(db.Unicode(), nullable=False)
    password = db.Column(db.Unicode(), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, server_default="True")
    is_superuser = db.Column(db.Boolean(), nullable=False, server_default="False")
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False)
