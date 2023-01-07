from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, Flask, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from config import path
import structure
from werkzeug.security import generate_password_hash
import sqlalchemy.orm
from website import database, engine
import structure
from flask import session




schueler = Blueprint('schueler', __name__)


@schueler.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    with sqlalchemy.orm.Session(engine) as session:
        s = session.query(structure.Workshop
                          ).where(structure.Workshop.minKlasse <= current_user.klassenstufe
                          ).where(structure.Workshop.maxKlasse >= current_user.klassenstufe)
        list_of_projects = s.all()
    if request.method == 'POST':
        return redirect(url_for('schueler.wahl'))

    return render_template('projectlist.html', user=current_user, projektliste = list_of_projects) 



@schueler.route('/list/<int:id>', methods=['GET', 'POST'])
@login_required
def show_one_project(id):
    session = sqlalchemy.orm.Session(engine)
    s = session.query(structure.Workshop).where(structure.Workshop.id == id)
    access = s.first()
    if access:
        if access.minKlasse <= current_user.klassenstufe and access.maxKlasse >= current_user.klassenstufe:
            return render_template('one_project.html', user=current_user, project = access) 
        else:
            return f"Dieses Projekt ist wird nicht für deine Klassenstufe angeboten"
    else: 
        return f"Diesen Kurs gibt es nicht"


@schueler.route('/wahl', methods=['GET', 'POST'])
@login_required
def wahl():
    with sqlalchemy.orm.Session(engine) as session:
        if request.method == 'POST':
            user = session.get(structure.Person, current_user.id)
            user._wunsch1_id = int(request.form.get('wunsch1')) if request.form.get('wunsch1') else None
            user._wunsch2_id = int(request.form.get('wunsch2')) if request.form.get('wunsch2') else None
            user._wunsch3_id = int(request.form.get('wunsch3')) if request.form.get('wunsch3') else None 
            # current_user.wunsch2 = request.form.get('wunsch2')
            # current_user.wunsch3 = request.form.get('wunsch3')
            
            session.commit()
        s = session.query(structure.Workshop
                        ).where(structure.Workshop.minKlasse <= current_user.klassenstufe
                        ).where(structure.Workshop.maxKlasse >= current_user.klassenstufe)
        list_of_projects = s.all()
       
    return render_template('wahl.html', user=current_user, projektliste=list_of_projects)