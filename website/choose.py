
from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user

choose = Blueprint('choose', __name__)

@choose.route('/choose', methods=['GET', 'POST'])
#@login_required
def select():
    
    return render_template('select_project.html', user=current_user) 
