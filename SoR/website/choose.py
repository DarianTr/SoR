from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, Flask, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
import os
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
import sqlalchemy
import sqlalchemy.orm
from website import database


ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
choose = Blueprint('choose', __name__)

def lehrer_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.pos() == 'Lehrer':
            return func(*args, **kwargs)
        else:
            flash("no permission")
            return redirect(url_for('choose.select'))
            
    return decorated_view

@choose.route('/choose', methods=['GET', 'POST'])
#@login_required(current_user.position == 'Schueler')
def select():
    return render_template('select_project.html', user=current_user) 

@choose.route('/lehrer', methods=['GET', 'POST'])
@lehrer_role_required
@login_required
def lehrer(): 
    
    return render_template('lehrer.html', user=current_user)



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



class FileForm(FlaskForm):
    file = FileField('File', validators=[DataRequired(), FileAllowed(ALLOWED_EXTENSIONS, 'Bitte nur .txt oder .csv files')])
    
@lehrer_role_required
@choose.route('/schuelerliste', methods=['GET', 'POST'])
def setup_schuelerliste():
    form = FileForm()
    if form.validate_on_submit():
        f = form.file.data
        f.save('asdfasduf01nv010b923n.csv')
        datei = util.username_password_csv_erweiterung('asdfasduf01nv010b923n.csv', 'csv', 7)
        try:
            d = database.session.query(structure.Person).where(structure.Person.position == 'Schueler').all()
            for person in d:
                database.session.delete(person)
            create_schueler(datei)
            return send_file(os.path.join(path, 'output.csv'),  as_attachment=True, download_name='SchuelerlisteMitZugangsdaten.csv')
        except Exception as e:
            return "Error: " + str(e)
    else:
        flash('Bitte nur .txt oder .csv files', category='error')
    if os.path.exists(os.path.join(path, 'asdfasduf01nv010b923n.csv')):
        os.remove(os.path.join(path, 'asdfasduf01nv010b923n.csv'))
    return render_template('upload.html', form=form)
    
    
def create_schueler(csv_file):
    data = pd.read_csv(csv_file, sep=',', encoding='utf-8')
    for row in data.itertuples():
        print(row[1], row[2], row[3], row[4])
        new_user = structure.Person(vorname=row[1], nachname=row[2], position='Schueler', username=row[3],  password=generate_password_hash(row[4], method='sha256'))
        database.session.add(new_user)
        database.session.commit()