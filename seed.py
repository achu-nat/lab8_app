from app import application
from database import db
from models import User, Class

with application.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="admin", role="admin")

    t1 = User(username="ahepworth", password="123", role="teacher")
    t2 = User(username="cnorris", password="123", role="teacher")

    s1 = User(username="mindy", password="123", role="student")
    s2 = User(username="chuck", password="123", role="student")

    c1 = Class(name="CSE 108", capacity=3, teacher=t1)
    c2 = Class(name="CSE 111", capacity=3, teacher=t2)
    c3 = Class(name="CSE 165", capacity=2, teacher=t2)

    db.session.add_all([admin, t1, t2, s1, s2, c1, c2, c3])
    db.session.commit()

    print("Database seeded.")