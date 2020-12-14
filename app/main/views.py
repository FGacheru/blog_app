from flask import render_template,request,redirect,url_for,abort
from app.models import *
from . import main
from ..request import get_quote
from .. import db,photos
from flask_login import login_required, current_user
import markdown2
from .forms import *


@main.route('/')
def index():
    '''
    Index page
    return
    '''
    title= 'Blog-App!'
    message= "WELCOME TO GACHERU BLOG WEBSITE!!"
    quote = get_quote()

    return render_template('index.html', title = title,message = message, quote = quote)



@main.route('/user/<uname>')
@login_required
def profile(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, quote=quote)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form, quote=quote)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    quote = get_quote()
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/views/new_views', methods = ['GET','POST'])
@login_required
def new_views():
    quote = get_quote()

    form = ViewsForm()

    if form.validate_on_submit():
        views = form.description.data
        title = form.views_title.data

        # Updated views instance
        new_views = Views(views_title=title,description= views,user_id=current_user.id)

        title='New views'

        new_views.save_views()

        return redirect(url_for('main.new_views'))

    return render_template('views.html',form= form, quote=quote)

@main.route('/views/all', methods=['GET', 'POST'])
@login_required
def all():
    opinion = Views.query.all()
    quote = get_quote()
    return render_template('opinion.html', opinion=opinion, quote=quote)

@main.route('/comments/<id>')
@login_required
def comment(id):
    '''
    function to return the comments
    '''
    quote = get_quote()
    comm =Comments.get_comment(id)
    title = 'comments'
    return render_template('comments.html',comment = comm,title = title,quote=quote)

@main.route('/new_comment/<int:views_id>', methods = ['GET','POST'])
@login_required
def new_comment(views_id):
    quote = get_quote()
    opinion = Views.query.filter_by(id = views_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment=comment,user_id=current_user.id, views_id=views_id)

        new_comment.save_comment()

        return redirect(url_for('main.index'))
    title='New comment'
    return render_template('new_comment.html',title=title,comment_form = form,views_id=views_id,quote=quote)
