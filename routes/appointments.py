from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Patient, Examination
from forms import ExaminationForm
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page
    pagination = Examination.query.filter_by(status='pending').order_by(Examination.created_at.desc()).paginate(page=page, per_page=per_page)
    return render_template('appointments/index.html', 
                         appointments=pagination.items,
                         pagination=pagination,
                         page=page)

@appointments_bp.route('/appointments/new', methods=['GET', 'POST'])
@login_required
def new():
    form = ExaminationForm()
    if form.validate_on_submit():
        examination = Examination(
            patient_id=form.patient_id.data,
            examination_type=form.examination_type.data,
            status='pending',
            created_at=datetime.now(),
            performed_by=current_user.id
        )
        db.session.add(examination)
        db.session.commit()
        flash('تم إنشاء الموعد بنجاح', 'success')
        return redirect(url_for('appointments.index'))
    return render_template('appointments/form.html', form=form, title='موعد جديد')

@appointments_bp.route('/appointments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    appointment = Examination.query.get_or_404(id)
    form = ExaminationForm(obj=appointment)
    if form.validate_on_submit():
        appointment.patient_id = form.patient_id.data
        appointment.examination_type = form.examination_type.data
        db.session.commit()
        flash('تم تحديث الموعد بنجاح', 'success')
        return redirect(url_for('appointments.index'))
    return render_template('appointments/form.html', form=form, title='تعديل موعد')

@appointments_bp.route('/appointments/<int:id>/cancel')
@login_required
def cancel(id):
    appointment = Examination.query.get_or_404(id)
    appointment.status = 'cancelled'
    db.session.commit()
    flash('تم إلغاء الموعد بنجاح', 'success')
    return redirect(url_for('appointments.index'))
