from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.reservation_service import ReservationService
import functools

reservation_bp = Blueprint('reservation', __name__, url_prefix='/reserva')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view

@reservation_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        espacio_id = request.form['espacio_id']
        fecha = request.form['fecha']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']
        
        success, msg = ReservationService.create_reservation(
            session['user_id'], espacio_id, fecha, hora_inicio, hora_fin
        )
        if success:
            flash(msg, 'success')
            return redirect(url_for('reservation.mis_reservas'))
        else:
            flash(msg, 'error')
    
    espacios = ReservationService.get_active_spaces()
    return render_template('reservar.html', espacios=espacios)

@reservation_bp.route('/mis_reservas')
@login_required
def mis_reservas():
    reservas = ReservationService.get_user_reservations(session['user_id'])
    return render_template('mis_reservas.html', reservas=reservas)

@reservation_bp.route('/cancelar', methods=['POST'])
@login_required
def cancelar():
    reserva_id = request.form['reserva_id']
    success, msg = ReservationService.cancel_reservation(reserva_id, user_id=session['user_id'])
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
    return redirect(url_for('reservation.mis_reservas'))
