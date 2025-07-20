from flask import Blueprint
from ..model.User_movie import *

um = Blueprint('user_movie', __name__)


@um.route('/addUserMovie')
def add_user_movie():
    movie_list = []
    try:
        for i in range(5):
            movie = Movie(name='电影' + str(i))
            movie_list.append(movie)
            db.session.add_all(movie_list)
            db.session.commit()
        return 'success'
    except Exception as e:
        print("e:", e)
        db.session.rollback()
        return 'fail'


