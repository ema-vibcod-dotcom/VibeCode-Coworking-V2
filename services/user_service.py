from models import Usuario, RegistroAcceso
from database import db
from services.auth_service import AuthService
from datetime import datetime, date
from sqlalchemy import and_, or_

class UserService:
    @staticmethod
    def create_user(name, password):
        if Usuario.query.filter_by(nombre=name).first():
            return None # User exists
        hashed = AuthService.hash_password(password)
        user = Usuario(nombre=name, contraseña_hashed=hashed)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_users():
        return Usuario.query.all()

    @staticmethod
    def check_in(user_id):
        user = Usuario.query.get(user_id)
        if not user or user.estado_actual == 'dentro':
            return False, "Usuario no existe o ya está dentro"
        
        from models import Reserva, RegistroAcceso
        from datetime import timedelta
        now = datetime.now()
        
        # Look for an active reservation today that is active or starts soon (within 30 mins)
        # OR is already ongoing.
        reserva_activa = Reserva.query.filter(
            Reserva.usuario_id == user_id,
            Reserva.fecha == now.date(),
            Reserva.estado == 'activa'
        ).all()
        
        linked_reserva = None
        for r in reserva_activa:
            start_dt = datetime.combine(now.date(), r.hora_inicio)
            end_dt = datetime.combine(now.date(), r.hora_fin)
            # Link if within 30 mins before start OR during the reservation OR within 15 mins after end (grace)
            if (now >= start_dt - timedelta(minutes=30)) and (now <= end_dt + timedelta(minutes=15)):
                linked_reserva = r
                break

        # Create open record
        registro = RegistroAcceso(
            usuario_id=user.id,
            fecha=now.date(),
            hora_ingreso=now.time(),
            estado='abierto',
            reserva_id=linked_reserva.id if linked_reserva else None
        )
        user.estado_actual = 'dentro'
        
        db.session.add(registro)
        db.session.commit()
        msg = f"Check-in exitoso a las {now.strftime('%H:%M:%S')}"
        if linked_reserva:
            msg += f" (Asociado a tu reserva en {linked_reserva.espacio.nombre})"
        return True, msg

    @staticmethod
    def get_dashboard_data(user_id):
        user = Usuario.query.get(user_id)
        if not user:
            return None, None, None
            
        from services.reservation_service import ReservationService
        ReservationService._update_finished_reservations()
        
        # Get last open record
        registro = RegistroAcceso.query.filter_by(usuario_id=user_id, estado='abierto').first()
        
        from models import Reserva
        # Get next active reservation
        next_res = Reserva.query.filter(
            Reserva.usuario_id == user_id,
            Reserva.estado == 'activa',
            or_(
                Reserva.fecha > date.today(),
                and_(Reserva.fecha == date.today(), Reserva.hora_fin > datetime.now().time())
            )
        ).order_by(Reserva.fecha.asc(), Reserva.hora_inicio.asc()).first()
        
        return user.estado_actual, registro, next_res

    @staticmethod
    def check_out(user_id):
        user = Usuario.query.get(user_id)
        if not user or user.estado_actual == 'fuera':
            return False, "Usuario no existe o ya está fuera"

        # Find open record
        registro = RegistroAcceso.query.filter_by(usuario_id=user.id, estado='abierto').first()
        now = datetime.now()
        
        if registro:
            registro.hora_salida = now.time()
            registro.estado = 'cerrado'
        
        user.estado_actual = 'fuera'
        db.session.commit()
        return True, f"Check-out exitoso a las {now.strftime('%H:%M:%S')}"

    @staticmethod
    def get_user_status(user_id):
        user = Usuario.query.get(user_id)
        return user.estado_actual if user else None
