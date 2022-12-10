from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from structure import Person 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = Person.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash('Logged in sucessfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('choose.select'))
        else:
            flash('Incorrect password, try again.', category='error')
    else:
        flash('Email does not exist.', category='error')
    
    return render_template('login.html', user=current_user) 
