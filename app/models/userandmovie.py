from app.extensions import db

class UserAndMovie(db.Model):
    # 一个用户能收藏多部电影，一部电影能被多个用户收藏
    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.Integer, db.ForeignKey('movies.postid'))
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
