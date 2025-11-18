from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config
from database import db
from models import User, Class, Enrollment
from forms import LoginForm

# --------------------------------------
# Create Flask Application
# --------------------------------------
application = Flask(__name__)
application.config.from_object(Config)

db.init_app(application)

# --------------------------------------
# Login Manager
# --------------------------------------
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login"

# --------------------------------------
# Admin Panel (Flask-Admin)
# --------------------------------------
admin = Admin(application, name="ACME Admin")
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(Enrollment, db.session))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------------------------------
# LOGIN ROUTES
# --------------------------------------
@application.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            login_user(user)
            if user.role == "student":
                return redirect("/student")
            if user.role == "teacher":
                return redirect("/teacher")
            return redirect("/adminpage")
    return render_template("login.html", form=form)


@application.route("/logout")
def logout():
    logout_user()
    return redirect("/")


# --------------------------------------
# STUDENT ROUTES
# --------------------------------------
@application.route("/student")
@login_required
def student_dashboard():
    return render_template("student_dashboard.html")


@application.route("/student/my_classes")
@login_required
def student_my_classes():
    classes = [e.class_obj for e in current_user.enrollments]
    return render_template("student_my_classes.html", classes=classes)


@application.route("/student/all_classes")
@login_required
def student_all_classes():
    classes = Class.query.all()
    my_ids = {e.class_id for e in current_user.enrollments}
    return render_template("student_all_classes.html", classes=classes, my_ids=my_ids)


@application.route("/student/enroll/<int:class_id>")
@login_required
def enroll(class_id):
    cls = Class.query.get(class_id)

    if len(cls.enrollments) >= cls.capacity:
        return "Class Full!"

    existing = Enrollment.query.filter_by(student_id=current_user.id, class_id=class_id).first()
    if existing:
        return "Already Enrolled!"

    enroll = Enrollment(student_id=current_user.id, class_id=class_id)
    db.session.add(enroll)
    db.session.commit()
    return redirect("/student/all_classes")


# --------------------------------------
# TEACHER ROUTES
# --------------------------------------
@application.route("/teacher")
@login_required
def teacher_dashboard():
    if current_user.role != "teacher":
        return redirect("/")
    classes = current_user.classes
    return render_template("teacher_dashboard.html", classes=classes)


@application.route("/teacher/class/<int:class_id>", methods=["GET", "POST"])
@login_required
def teacher_class(class_id):
    if current_user.role != "teacher":
        return redirect("/")

    cls = Class.query.get(class_id)

    # prevent teachers from accessing other teachers' classes
    if cls.teacher_id != current_user.id:
        return "Unauthorized", 403

    enrollments = cls.enrollments

    if request.method == "POST":
        eid = request.form["eid"]
        grade = request.form["grade"]

        enr = Enrollment.query.get(eid)
        enr.grade = grade
        db.session.commit()

        return redirect(f"/teacher/class/{class_id}")  # refresh after save

    return render_template("teacher_class.html", cls=cls, enrollments=enrollments)


# --------------------------------------
# ADMIN ROUTE
# --------------------------------------
@application.route("/adminpage")
@login_required
def admin_page():
    return render_template("admin.html")


# --------------------------------------
# Run Server
# --------------------------------------
if __name__ == "__main__":
    application.run(debug=True)


# the commands to run everything in order:
# 1. pip install -r requirements.txt (this installs all necessary flask packages)
# 2. run python seed.py
# 3. run python app.py
# logins:
# admin/admin
# mindy/123
# chuck/123
# ahepworth/123
