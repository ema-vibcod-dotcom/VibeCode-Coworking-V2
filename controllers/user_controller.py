from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import AuthService
from services.user_service import UserService
import functools

user_bp = Blueprint('user', __name__, url_prefix='/usuario')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        user = AuthService.authenticate_user(nombre, password)
        if user:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('user.dashboard'))
        flash('Credenciales inválidas.', 'error')
    return render_template('login_user.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))

@user_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    status, registro, next_res = UserService.get_dashboard_data(user_id)
    return render_template('user_dashboard.html', status=status, registro=registro, next_res=next_res)

@user_bp.route('/checkin', methods=['POST'])
@login_required
def checkin():
    user_id = session['user_id']
    success, message = UserService.check_in(user_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('user.dashboard'))

@user_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    user_id = session['user_id']
    success, message = UserService.check_out(user_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('user.dashboard'))

@user_bp.route('/estado')
@login_required
def estado():
    user_id = session['user_id']
    return {'estado': UserService.get_user_status(user_id)}
