import threading
from flask import render_template, session, redirect, url_for, current_app,flash
from .. import db
from ..models import User
from ..email import Mail
from . import main
from .forms import NameForm
from core.crawling import naver_crawling

@main.route('/',methods=['GET','POST'])
def index():
    form =NameForm()

    if form.validate_on_submit():
        name = User.query.filter_by(user_name=form.name.data).first()

        if name is None:
            #새로운 사용자 db에 추가
            flash('db에 사용자가 추가되었습니다.')
            user = User(user_name=form.name.data,email=form.email.data)
            db.session.add(user)
            session['known']=False
        else:
            session['known']=True

        flash('메일로 크롤링 정보를 보내드렸습니다.')
        mail = Mail(naver_crawling(), form.email.data)
        t=threading.Thread(target=mail.naver_send_email) # 다른 스레드이용.
        t.start()

        session['name']= form.name.data
        session['email'] = form.email.data

        form.name.data=''
        form.email.data=''

        return redirect(url_for('.index')) #post/rediret/get patter 기법. 마지막 요청을 post로 남기지 않기 위해.

    return render_template('index.html',form=form,name=session['name'],
                           known=session.get('known',False))

@main.route('/profile/<int:id>/')
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html',user=user)