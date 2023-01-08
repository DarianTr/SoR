from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, Flask, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
import os
import threading
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from flask import abort
from werkzeug.utils import secure_filename
from . import app, database, engine
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
import util
from config import path
import structure
from werkzeug.security import generate_password_hash
import sqlalchemy.orm
from website import database
from algorithmus.algorithmus_glpk import assign_students
from sqlalchemy.orm import joinedload
from datetime import datetime


ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
def assign_students_finished(job_id, result):
    with sqlalchemy.orm.Session(engine) as sess:
        try:
            for student_id, projekt_id in result.items(): 
                student = sess.get(structure.Person, student_id)
                student._projekt_id = projekt_id
            sess.commit()

            job = sess.get(structure.Job, job_id)
            job.finish = datetime.now()
            job.status = 'success'
            
            sess.commit()
        except Exception as e:
            job = sess.get(structure.Job, job_id)
            job.finish = datetime.now()
            job.status = 'error'
            job.messsage = str(e)
            sess.commit()
        return True
        
def algorithm_in_new_thread(list_of_students, list_of_projects):
    with sqlalchemy.orm.Session(engine) as sess:
        starter = sess.get(structure.Person, current_user.id)
        new_job  = structure.Job(starter=starter, status='waiting')
        sess.add(new_job)
        sess.commit()
        new_thread = threading.Thread(target=assign_students, args=(new_job.id, list_of_students, list_of_projects, 100, 75, 50, assign_students_finished))
        new_thread.start()
        new_job.status = 'running'
        sess.merge(new_job)
        sess.commit()
    return new_job.id          
           
def write_to_csv(filename):
    with sqlalchemy.orm.Session(engine) as sess:
        list_of_students = sess.query(structure.Person).where(structure.Person.position == "Schueler").all()
        file = pd.DataFrame({'Name':[s.vorname + s.nachname for s in list_of_students],
                             'Klasse':[s.klassenstufe for s in list_of_students],
                             'Projekt':[s.projekt.name for s in list_of_students]})
        file.to_csv(filename, index=False)
        
            
lehrer = Blueprint('lehrer', __name__)

def lehrer_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.pos() == 'Lehrer':
            return func(*args, **kwargs)
        else:
            flash("no permission", category="error")
            return redirect(url_for('schueler.list'))
            
    return decorated_view

@lehrer.route('/schueler_projekt_download', methods=['GET'])
@login_required
@lehrer_role_required
def schueler_projekt_download(): 
    with sqlalchemy.orm.Session(engine) as sess:
        last_successful_job = sess.query(structure.Job).options(joinedload('*')).filter(structure.Job.status == 'success').order_by(structure.Job.start.desc()).first()
        if not last_successful_job:
            return 'Der Algorithmus läuft noch. Bitte haben sie Gedult.'
        
        write_to_csv('SchuelerlisteMitProjekten.csv')
        return send_file(os.path.join(path, f'SchuelerlisteMitProjekten.csv'),  as_attachment=True, download_name='SchuelerlisteMitProjekten.csv')

@lehrer.route('/lehrerview', methods=['GET', 'POST'])
@login_required
@lehrer_role_required
def lehrerview(): 
    with sqlalchemy.orm.Session(engine) as sess:
        count_students_voted = sess.query(structure.Person).filter(structure.Person.wunsch1 != None).where(structure.Person.position == 'Schueler').count()
        count_students = sess.query(structure.Person).where(structure.Person.position == 'Schueler').count()
        jobs = sess.query(structure.Job).order_by(structure.Job.start.desc()).limit(10).options(joinedload('*')).all()
        jobs_running = [j for j in jobs if j.status == 'Running' or j.status == 'Waiting'] != []
        if request.method == 'POST':
            #set algorithm bool to True
            
                s = sess.query(structure.Person).filter(structure.Person.wunsch1 != None).where(structure.Person.position == 'Schueler').options(joinedload('*'))
                list_of_students = s.all()


                s = sess.query(structure.Workshop)
                list_of_projects = s.all()
                
                id = algorithm_in_new_thread(list_of_students, list_of_projects)
                jobs = sess.query(structure.Job).all()
        last_successful_job = sess.query(structure.Job).options(joinedload('*')).filter(structure.Job.status == 'success').order_by(structure.Job.start.desc()).first()

    return render_template('lehrer.html', user=current_user, count_students_voted=count_students_voted, count_students=count_students, jobs=jobs, jobs_running=jobs_running, last_successful_job=last_successful_job)


   
def create_schueler(csv_file):
    data = pd.read_csv(csv_file, sep=',', encoding='utf-8')
    for row in data.itertuples():
        print(row[1], row[2], row[3], row[4])
        new_user = structure.Person(vorname=row[1], nachname=row[2], position='Schueler', username=row[3],  password=generate_password_hash(row[4], method='sha256'))
        database.session.add(new_user)
        database.session.commit()

class FileForm(FlaskForm):
    schueler_file = FileField('File', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Bitte nur .txt oder .csv files')])
    projekt_file = FileField('File', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Bitte nur .txt oder .csv files')])


@lehrer.route('/import', methods=['GET', 'POST'])
@lehrer_role_required
def schuelerliste():
    form = FileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            f = form.schueler_file.data
            if f:
                content = f.read().decode('utf-8')
                datei = util.username_password_csv_erweiterung(content, 'csv', 7, 'schuelerlist_mit_passwort_und_username.csv')
                try:
                    d = database.session.query(structure.Person).where(structure.Person.position == 'Schueler').all()
                    for person in d:
                        database.session.delete(person)
                    create_schueler(datei)
                    return send_file(os.path.join(path, 'output.csv'),  as_attachment=True, download_name='SchuelerlisteMitZugangsdaten.csv')
                except Exception as e:
                    return "Error: " + str(e)
            p = form.projekt_file.data
            if p:
                content = p.read().decode('utf-8')
                util.projekt_csv(content, 'csv')
            
            
        else:
            flash('Bitte nur .txt oder .csv files', category='error')
    return render_template('upload.html', form=form, user=current_user)
    
 
# @choose.route('/select-file', methods=['POST', 'GET'])
# def select_file():
#     # Create a Tkinter root window
#     root = Tk()
#     root.withdraw()

#     # Ask the user to select a file
#     filepath = askopenfilename()

#     # Sendet das file -> client kann speichern
#     return send_file(filepath, as_attachment=True)

# @choose.route('/download_file')
# def download_file():
#     try:
#         return send_file('test.txt',  as_attachment=True, download_name='file.txt')
#     except Exception as e:
#         return "Error: " + str(e)
    
    
# @choose.route('/upload-file', methods=['POST', 'GET'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # file.save(file.filename)
            
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''

# choose.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)