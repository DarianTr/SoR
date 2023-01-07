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
def show_projects():
    with sqlalchemy.orm.Session(engine) as session:
        s = session.query(structure.Workshop
                          ).where(structure.Workshop.minKlasse >= current_user.klassenstufe
                          ).where(structure.Workshop.maxKlasse <= current_user.klassenstufe)
        list_of_projects = s.all()
    if request.method == 'POST':
        return redirect(url_for('schueler.wahl'))

    return render_template('projectlist.html', user=current_user, projektliste = list_of_projects) 

@schueler.route('/list/<int:id>', methods=['GET', 'POST'])
def show_one_project(id):
    session = sqlalchemy.orm.Session(engine)
    s = session.query(structure.Workshop).where(structure.Workshop.id == id)
    access = s.first()
    if access:
        if access.minKlasse <= current_user.klassenstufe and access.maxKlasse >= current_user.klassenstufe:
            pass
        else:
            return f"Dieses Projekt ist wird nicht für deine Klassenstufe angeboten"
    else: 
        return f"Diesen Kurs gibt es nicht"
    return render_template('projectlist.html', user=current_user, project = access) 

@schueler.route('/wahl', methods=['GET', 'POST'])
def wahl():
    with sqlalchemy.orm.Session(engine) as session:
        s = session.query(structure.Workshop
                          ).where(structure.Workshop.minKlasse >= current_user.klassenstufe
                          ).where(structure.Workshop.maxKlasse <= current_user.klassenstufe)
        list_of_projects = s.all()
    if request.method == 'POST':
        current_user.wunsch1 = request.form.get('wunsch1')
        current_user.wunsch2 = request.form.get('wunsch2')
        current_user.wunsch3 = request.form.get('wunsch3')
    return render_template('projectlist.html', user=current_user, list_of_projects=list_of_projects)