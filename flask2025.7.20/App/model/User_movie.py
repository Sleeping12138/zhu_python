from App.exts import db

collect = db.Table(
    'collect',
    db.Column('watcher_id', db.Integer, db.ForeignKey('watcher.watcher_id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'))
)


class Watcher(db.Model):
    watcher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    users = db.relationship("Watcher", backref='movies', lazy=True)
