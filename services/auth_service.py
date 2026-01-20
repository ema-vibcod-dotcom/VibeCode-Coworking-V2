from werkzeug.security import generate_password_hash, check_password_hash
from models import Administrador, Usuario
from database import db

class AuthService:
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)

    @staticmethod
    def create_initial_admin(name, password):
        if not Administrador.query.first():
            hashed = AuthService.hash_password(password)
            admin = Administrador(nombre=name, contraseña_hashed=hashed)
            db.session.add(admin)
            db.session.commit()
            return admin
        return None

    @staticmethod
    def authenticate_admin(name, password):
        admin = Administrador.query.filter_by(nombre=name).first()
        if admin and AuthService.verify_password(admin.contraseña_hashed, password) and admin.activo:
            return admin
        return None

    @staticmethod
    def authenticate_user(name, password):
        user = Usuario.query.filter_by(nombre=name).first()
        if user and AuthService.verify_password(user.contraseña_hashed, password) and user.activo:
            return user
        return None
