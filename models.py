from database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # student / teacher / admin

    enrollments = db.relationship("Enrollment", backref="student", lazy=True)
    classes = db.relationship("Class", backref="teacher", lazy=True)

    def __repr__(self):
        return self.username

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    enrollments = db.relationship("Enrollment", backref="class_obj", lazy=True)


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"))
    grade = db.Column(db.String(5))