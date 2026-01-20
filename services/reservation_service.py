from models import Reserva, Espacio, Usuario
from database import db
from datetime import datetime, date, time
from sqlalchemy import and_, or_

class ReservationService:
    @staticmethod
    def _update_finished_reservations():
        now = datetime.now()
        Reserva.query.filter(
            Reserva.estado == 'activa',
            or_(
                Reserva.fecha < now.date(),
                and_(Reserva.fecha == now.date(), Reserva.hora_fin <= now.time())
            )
        ).update({"estado": "finalizada"})
        db.session.commit()

    @staticmethod
    def get_active_spaces():
        return Espacio.query.filter_by(activo=True).all()

    @staticmethod
    def get_user_reservations(user_id):
        ReservationService._update_finished_reservations()
        return Reserva.query.filter_by(usuario_id=user_id).order_by(Reserva.fecha.desc(), Reserva.hora_inicio.desc()).all()

    @staticmethod
    def get_all_reservations(user_id=None, espacio_id=None, start_date=None, end_date=None):
        ReservationService._update_finished_reservations()
        query = Reserva.query
        
        if user_id:
            query = query.filter(Reserva.usuario_id == user_id)
        if espacio_id:
            query = query.filter(Reserva.espacio_id == espacio_id)
        if start_date:
            query = query.filter(Reserva.fecha >= start_date)
        if end_date:
            query = query.filter(Reserva.fecha <= end_date)
            
        return query.order_by(Reserva.fecha.desc(), Reserva.hora_inicio.desc()).all()

    @staticmethod
    def check_overlap(user_id, espacio_id, fecha, start_time, end_time):
        # 1. Check user overlap (any space)
        user_overlap = Reserva.query.filter(
            Reserva.usuario_id == user_id,
            Reserva.fecha == fecha,
            Reserva.estado == 'activa',
            # Overlap logic: (StartA < EndB) and (EndA > StartB)
            Reserva.hora_inicio < end_time,
            Reserva.hora_fin > start_time
        ).first()
        
        if user_overlap:
            return True, "Ya tienes una reserva en ese horario."

        # 2. Check space overlap (same space, any user)
        space_overlap = Reserva.query.filter(
            Reserva.espacio_id == espacio_id,
            Reserva.fecha == fecha,
            Reserva.estado == 'activa',
            Reserva.hora_inicio < end_time,
            Reserva.hora_fin > start_time
        ).first()

        if space_overlap:
            return True, "El espacio ya está reservado en ese horario."
            
        return False, None

    @staticmethod
    def create_reservation(user_id, espacio_id, fecha_str, start_time_str, end_time_str):
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            
            # Validation: Future date/time
            now = datetime.now()
            if fecha < now.date() or (fecha == now.date() and start_time < now.time()):
                 return False, "La reserva debe ser futura."
            
            if start_time >= end_time:
                return False, "La hora de fin debe ser posterior a la de inicio."

            # Overlap check
            overlap, msg = ReservationService.check_overlap(user_id, espacio_id, fecha, start_time, end_time)
            if overlap:
                return False, msg

            reserva = Reserva(
                usuario_id=user_id,
                espacio_id=espacio_id,
                fecha=fecha,
                hora_inicio=start_time,
                hora_fin=end_time
            )
            db.session.add(reserva)
            db.session.commit()
            return True, "Reserva creada exitosamente."
            
        except ValueError:
            return False, "Formato de fecha u hora inválido."

    @staticmethod
    def cancel_reservation(reserva_id, user_id=None, is_admin=False):
        reserva = Reserva.query.get(reserva_id)
        if not reserva:
            return False, "Reserva no encontrada."
            
        if not is_admin and reserva.usuario_id != user_id:
            return False, "No tienes permiso para cancelar esta reserva."
            
        if reserva.estado != 'activa':
            return False, "Solo se pueden cancelar reservas activas."
            
        reserva.estado = 'cancelada'
        db.session.commit()
        return True, "Reserva cancelada."
