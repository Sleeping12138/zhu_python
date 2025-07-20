from ..exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"<id:{self.id},  username:{self.username},  age:{self.age}>"
