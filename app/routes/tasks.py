from flask import Blueprint, render_template,redirect,session, request, url_for, flash
from app import db
from app.models import User, Task


tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/")
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(username=session['user']).first()
    tasks = Task.query.filter_by(user_id=user.user_id).all()
    return render_template('tasks.html', tasks = tasks)

@tasks_bp.route('/add', methods= ['POST'])
def add_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(username=session['user']).first()
    
    title = request.form.get('title')
    if title:
        new_task = Task(title = title, status = 'pending',user_id=user.user_id)
        db.session.add(new_task)
        db.session.commit()
        flash('task added successfully', 'success')
        
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods = ['POST'])
def toggle_status(task_id):
    
    user = User.query.filter_by(username=session['user']).first()
    task = Task.query.filter_by(id=task_id,user_id=user.user_id).first()
    if task:
        if task.status == 'pending':
            task.status = 'working'
        elif task.status == 'working':
            task.status = 'done'
        else:
            task.status = 'pending'
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))



@tasks_bp.route('/edit/<int:task_id>',methods=['POST'])
def edit_task(task_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['user']).first()
    task = Task.query.filter_by(id=task_id,user_id=user.user_id).first()

    if task:
        updated_title = request.form.get('title')
        if updated_title:
            task.title = updated_title
            db.session.commit()
            flash('Task updated successfully!','success')

    return redirect(url_for('tasks.view_tasks'))



@tasks_bp.route('/delete/<int:task_id>',methods=['POST'])
def delete_task(task_id):

    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['user']).first()
    task = Task.query.filter_by(id=task_id,user_id=user.user_id).first()

    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!','success')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods= ['POST'])
def clear_tasks():
    user = User.query.filter_by(username=session['user']).first()
    Task.query.filter_by(user_id=user.user_id).delete()
    db.session.commit()
    flash('all task cleared!!', 'info')
    
    return redirect(url_for('tasks.view_tasks'))
    
    