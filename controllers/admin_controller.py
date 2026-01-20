from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from services.user_service import UserService
from services.log_service import LogService
from services.reservation_service import ReservationService
import functools

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.login'))
        return view(**kwargs)
    return wrapped_view

@admin_bp.route('/registro_inicial', methods=['GET', 'POST'])
def registro_inicial():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        if AuthService.create_initial_admin(nombre, password):
            flash('Administrador creado. Por favor inicie sesión.', 'success')
            return redirect(url_for('admin.login'))
        else:
            flash('Ya existe un administrador.', 'error')
    return render_template('registro_inicial.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        admin = AuthService.authenticate_admin(nombre, password)
        if admin:
            session.clear()
            session['admin_id'] = admin.id
            return redirect(url_for('admin.dashboard'))
        flash('Credenciales inválidas.', 'error')
    return render_template('login_admin.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        if UserService.create_user(nombre, password):
            flash('Usuario creado exitosamente.', 'success')
        else:
            flash('El usuario ya existe.', 'error')
        return redirect(url_for('admin.usuarios'))
    
    users = UserService.get_all_users()
    return render_template('admin_dashboard.html', users=users, active_tab='users')

@admin_bp.route('/registros')
@login_required
def registros():
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    logs = LogService.get_logs(user_id=user_id, status=status, start_date=start_date, end_date=end_date)
    users = UserService.get_all_users()
    return render_template('admin_registros.html', logs=logs, users=users, active_tab='logs')

@admin_bp.route('/reservas')
@login_required
def reservas():
    user_id = request.args.get('user_id')
    espacio_id = request.args.get('espacio_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    reservas = ReservationService.get_all_reservations(user_id=user_id, espacio_id=espacio_id, start_date=start_date, end_date=end_date)
    users = UserService.get_all_users()
    espacios = ReservationService.get_active_spaces()
    
    return render_template('admin_reservas.html', reservas=reservas, users=users, espacios=espacios, active_tab='reservas')

@admin_bp.route('/reserva/cancelar', methods=['POST'])
@login_required
def cancelar_reserva():
    reserva_id = request.form['reserva_id']
    success, msg = ReservationService.cancel_reservation(reserva_id, is_admin=True)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
    return redirect(url_for('admin.reservas'))
