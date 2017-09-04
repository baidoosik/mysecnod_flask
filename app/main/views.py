import threading
from flask import render_template, session, redirect, url_for, current_app,flash, abort
from flask_login import login_required
from .. import db
from ..models import User
from ..email import Mail
from . import main
from .forms import NameForm,EditProfileForm
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

    return render_template('index.html',form=form)

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


