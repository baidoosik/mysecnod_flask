import threading
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm,RegistrationForm
from ..email import Mail

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
        db.session.commit()

        token= user.generate_confirmation_token()
        token = token.decode('utf-8')
        token_url = 'http://127.0.0.1:5000/auth/confirm/'+token
        mail=Mail(token_url,user.email)
        t=threading.Thread(target=mail.naver_send_email) # 다른 스레드이용.
        t.start()
        flash('finish sign up process check your mail')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if current_user.confirm(token):
        flash("you success to register!")

    else:
        flash("your link is invalid")

    return redirect(url_for('main.index'))