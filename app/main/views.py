import threading
from flask import render_template, session, redirect, url_for,flash, abort,request,current_app, make_response
from flask_login import login_required,current_user
from .. import db
from ..models import User,Role,Post,Permission
from ..email import Mail
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm
from core.crawling import naver_crawling
from ..decorator import admin_required, permission_required



@main.route('/admin/')
@login_required
@admin_required
def admin_only():
    return 'For Admin'

#admin_only = admin_required(admin_only)

@main.route('/',methods=['GET','POST'])
def index():
    form =NameForm()
    if form.validate_on_submit():

        flash('메일로 크롤링 정보를 보내드렸습니다.')
        mail = Mail(naver_crawling(), form.email.data)
        t=threading.Thread(target=mail.naver_send_email) # 다른 스레드이용.
        t.start()

        session['email'] = form.email.data

        form.email.data=''

        return redirect(url_for('.index')) #post/rediret/get patter 기법. 마지막 요청을 post로 남기지 않기 위해.

    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query

    page = request.args.get('page',1,type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=10,error_out=False
    )
    posts = pagination.items

    return render_template('index.html',form=form,posts=posts,
                           show_follwed=show_followed,pagination=pagination)

@main.route('/profile/<user_name>/')
def profile(user_name):
    user = User.query.filter_by(user_name=user_name).first()

    if user is None:
        abort(404)
    return render_template('profile.html',user=user)


@main.route('/profile/<user_name>/edit/',methods=['GET','POST'])
def edit_profile(user_name):
    user = User.query.filter_by(user_name=user_name).first()
    form = EditProfileForm()

    if form.validate_on_submit():
        user.name = form.name.data
        user.location =form.location.data
        user.about_me =form.about_me.data

        db.session.add(user)

        return redirect(url_for('main.profile',user_name=user_name))

    return render_template('edit_profile.html',form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.user_name = form.user_name.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.user_name.data = user.user_name
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me

    return render_template('edit_profile.html', form=form, user=user)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(user_name=username).first()

    if user is None:
        flash('invalid user!')
        return redirect(url_for('main.index'))

    if current_user.is_following(user):
        flash('you already follow this user')
        return redirect(url_for('main.profile',user_name=username))

    current_user.follow(user)
    flash('')

    return redirect(url_for('main.profile',user_name=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(user_name=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('main.profile', user_name=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('main.profile', user_name=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(user_name=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=20,
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(user_name=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=20,
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp
