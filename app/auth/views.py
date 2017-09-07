import threading
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm,RegistrationForm, PasswordChangeForm,EmailChangeForm
from ..email import Mail



@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('invalid username or password')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(user_name=form.username.data,
                    email=form.email.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()# token 생성을 위해서

        token= user.generate_confirmation_token()
        token_url = 'http://127.0.0.1:5000 /auth/confirm/'+token
        mail=Mail(token_url,user.email)
        t=threading.Thread(target=mail.naver_send_email) # 다른 스레드이용.
        t.start()
        flash('finish sign up process check your mail')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if current_user.confirm(token):
        flash("you success to register!")

    else:
        flash("your link is invalid")

    return redirect(url_for('main.index'))


@auth.route('/profile/<int:id>/password_change/',methods=['GET','POST'])
@login_required
def password_change(id):
    user = User.query.get(id)
    form = PasswordChangeForm()

    if form.validate_on_submit():
        if user.verify_password(form.present_password.data):
            user.password=form.change_password.data
            db.session.add(user)
            flash('비밀번호 변경이 완료 됐습니다.')
            return redirect(url_for('main.profile',id=user.id))
        else:
            flash("현재 비밀번호가 올바르지 않습니다.")
            return redirect(url_for('auth.password_change'))

    return render_template('auth/password_change.html',form=form)


@auth.route('/profile/<int:id>/email_change/',methods=['GET','POST'])
@login_required
def email_change(id):
    user = User.query.get(id)
    form = EmailChangeForm()

    if form.validate_on_submit():
        token= user.generate_confirmation_token()
        token_url = 'http://127.0.0.1:5000/auth/confirm/'+token
        mail=Mail(token_url,form.change_email.data)
        t=threading.Thread(target=mail.naver_send_email) # 다른 스레드이용.
        t.start()
        user.email = form.change_email.data
        user.confirmed = False
        db.session.add(user)

        flash('finish sign up process check your new mail')

        return redirect(url_for('auth.login'))

    return render_template('auth/email_change.html',form=form)