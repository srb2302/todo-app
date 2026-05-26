from flask import Blueprint,render_template,redirect,url_for,flash,request, session
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!", "danger")
            return render_template('register.html')
        
        if password != confirm_password:
            flash('password should be same','danger')
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username,email=email,password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')
        
       