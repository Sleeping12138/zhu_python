from flask import Blueprint
from ..model.Classroom_student import *
from ..exts import db

cs = Blueprint('class_student', __name__)


@cs.route('/addClassroom')
def add_classroom():
    classroom = Classroom(name='1班')
    db.session.add(classroom)
    db.session.commit()
    return 'success'


@cs.route('/addStudent')
def add_student():
    student_list = []
    try:
        for i in range(10):
            stu = Student(name='张三' + str(i), age=18 + i, classroom_id=1)
            student_list.append(stu)
        db.session.add_all(student_list)
        db.session.commit()
        return 'success'
    except Exception as e:
        print("e:", e)
        db.session.rollback()
        return 'fail'


@cs.route('/getAllStudent')
def get_all_student():
    students = Classroom.query.get(1).students
    for stu in students:
        print(stu.name, stu.age, stu.classroom.name)
        print(stu.classroom)
    return 'success'
