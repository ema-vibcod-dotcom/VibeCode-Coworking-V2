from models import RegistroAcceso, Usuario
from database import db
from sqlalchemy import and_

class LogService:
    @staticmethod
    def get_logs(user_id=None, start_date=None, end_date=None, status=None):
        query = RegistroAcceso.query.join(Usuario)
        
        if user_id:
            query = query.filter(RegistroAcceso.usuario_id == user_id)
        
        if start_date:
            query = query.filter(RegistroAcceso.fecha >= start_date)
            
        if end_date:
            query = query.filter(RegistroAcceso.fecha <= end_date)
            
        if status:
            query = query.filter(RegistroAcceso.estado == status)
            
        return query.order_by(RegistroAcceso.creado_en.desc()).all()
