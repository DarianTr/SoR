import path
import sys
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from structure import Person 
from website import database

auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Person.query.where(Person.username == username).first()
        print(check_password_hash(user.password, password), user.password)
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in sucessfully!', category='success')
                login_user(user, remember=True)
                if user.pos() == 'Schueler':
                    return redirect(url_for('schueler.list'))
                else:
                    return redirect(url_for('lehrer.lehrerview'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Usename does not exist.', category='error')
    return render_template('login.html', user=current_user) 


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        klasse = request.form.get('klasse')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        position = request.form.get('position')
        user = Person.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            print("test")
            new_user = Person(vorname=vorname, nachname=nachname, klassenstufe = klasse, position=position, username=username,  password=generate_password_hash(password1, method='sha256'))
            database.session.add(new_user)
            database.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            if current_user.pos() == 'Schueler':
                return redirect(url_for('schueler.list'))
            else:
                return redirect(url_for('lehrer.lehrerview'))

    return render_template("signup.html", user=current_user)