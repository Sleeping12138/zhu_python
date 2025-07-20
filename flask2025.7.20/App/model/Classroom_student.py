from ..exts import db


class Classroom(db.Model):
    __tablename__ = 'classroom'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    students = db.relationship('Student', backref='classroom', lazy=True)


class Student(db.Model):
    # Define the table name
    __tablename__ = 'student'
    # Define the id column
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Define the name column
    name = db.Column(db.String(20))
    # Define the age column
    age = db.Column(db.Integer)
    # Define the classroom_id column
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'))
