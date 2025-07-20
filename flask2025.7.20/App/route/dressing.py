from flask import Blueprint
from sqlalchemy import and_, or_, not_

from ..model.User import *

bp = Blueprint('dressing', __name__)


@bp.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@bp.route('/addUser')
def add_user():
    try:
        for i in range(10):
            user = User(username='张三' + str(i), age=18 + i)
            db.session.add(user)
            db.session.commit()
        return 'success'
    except Exception as e:
        print(e)
        return 'fail'


@bp.route('/updateUser')
def update_user():
    user = User.query.first()
    user.age = 20
    db.session.commit()
    return 'success'


@bp.route('/deleteUser')
def delete_user():
    user = User.query.first()
    db.session.delete(user)
    db.session.commit()
    return 'success'


@bp.route('/getUser')
def get_user():
    # users = User.query.all()
    # print(users)
    # print(User.query)
    # for user in users:
    #     print(f"id: {user.id}, username: {user.username},age: {user.age}")

    # users = User.query.filter_by(age=25)
    # for user in users:
    #     print(f"id: {user.id}, username: {user.username},age: {user.age}")

    user = User.query.get(9)
    print(f"id: {user.id}, username: {user.username},age: {user.age}")

    return 'success'
