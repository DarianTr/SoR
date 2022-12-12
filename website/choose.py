from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
from flask import abort
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