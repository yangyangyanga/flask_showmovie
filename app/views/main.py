from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import Movie, UserAndMovie
from flask_login import current_user, login_required
from app.extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # movies = Movie.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Movie.query.paginate(page=page, per_page=5, error_out=False)
    movies = pagination.items
    return render_template('main/index.html', movies=movies, pagination=pagination)

# 添加收藏
@main.route('/addmovie/<postid>')
@login_required
def addmovie(postid):
    movies = []
    if current_user.is_authenticated:
        # 创建,写入数据库
        useraddmovie = UserAndMovie(postid=postid, uid=current_user.id)
        db.session.add(useraddmovie)
        db.session.commit()
        # 因为一个用户有对应的多个postid
        uam = UserAndMovie.query.filter_by(uid=current_user.id).all()
        print("===", uam)
        for m in uam:
            print("postid = ", m.postid)
            movies1 = Movie.query.filter_by(postid=m.postid).first()
            movies.append(movies1)
    flash('亲，您已收藏成功~~~')
    movies = list(set(movies))
    return render_template('movie/addmovie.html', movies=movies)

# 移除收藏
@main.route('/removemovie/<postid>/')
@login_required
def removemovie(postid):
    if current_user.is_authenticated:
        userandmovie = UserAndMovie.query.filter_by(postid=postid).all()
        for uam in userandmovie:
            db.session.delete(uam)
    flash('移除收藏成功~~~')
    return redirect(url_for('main.index'))