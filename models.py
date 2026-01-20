from datetime import datetime
from database import db

class Administrador(db.Model):
    __tablename__ = 'administradores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    contraseña_hashed = db.Column(db.String(200), nullable=False)
    fecha_creación = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    contraseña_hashed = db.Column(db.String(200), nullable=False)
    estado_actual = db.Column(db.String(20), default='fuera') # 'dentro' or 'fuera'
    fecha_creación = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    registros = db.relationship('RegistroAcceso', backref='usuario', lazy=True)
    reservas = db.relationship('Reserva', backref='usuario', lazy=True)

class RegistroAcceso(db.Model):
    __tablename__ = 'registros_acceso'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    hora_ingreso = db.Column(db.Time, default=datetime.utcnow().time, nullable=False)
    hora_salida = db.Column(db.Time, nullable=True)
    estado = db.Column(db.String(20), default='abierto') # 'abierto' or 'cerrado'
    reserva_id = db.Column(db.Integer, db.ForeignKey('reservas.id'), nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

class Espacio(db.Model):
    __tablename__ = 'espacios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    tipo = db.Column(db.String(20), nullable=False) # 'sala' or 'puesto'
    activo = db.Column(db.Boolean, default=True)
    reservas = db.relationship('Reserva', backref='espacio', lazy=True)

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String(20), default='activa') # 'activa', 'cancelada', 'finalizada'
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
