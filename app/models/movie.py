from app.extensions import db

class Movie(db.Model):
    __tablename__ = 'movies'
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True)
    image = db.Column(db.String(256))
    # 指定外键，关联users表
    # uid = db.Column(db.Integer, db.ForeignKey('users.id'))