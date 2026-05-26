from flask import Blueprint,render_template,redirect,url_for,flash,request, session
from app.models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            flash('login successful', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('invalid username or password', 'danger')
    
    return render_template('login.html')        
        

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('logged out', 'info')
    return redirect(url_for('auth.login'))