from app import db

class Task(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(20), default = 'pending')
    
    
class User(db.Model):
    tasks = db.relationship('Task', backref='owner', lazy=True)
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)  