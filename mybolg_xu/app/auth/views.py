# -*- coding: UTF-8 -*-
from flask import render_template, redirect, request, url_for, flash
from app import db
from . import auth
from flask.ext.login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from app.email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('不正确的邮箱或密码.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("您已成功登出。")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认您的账户', 'auth/email/confirm', user=user, token=token)
        flash('确认邮件已经发到了您的邮箱中')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经确认了您的账户，多谢！')
    else:
        flash('您的连接不可用或者已失效。')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirmed')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认您的账户', 'auth/email/confirm', user=current_user , token=token)
    flash('确认邮件已经发到了您的邮箱中')
    return redirect(url_for('main.index'))

@auth.route('/ChangePassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if current_user.confirmed:
        if form.validate_on_submit():
            if current_user.verify_password(form.password.data):
                current_user.password = form.password2.data
                db.session.add(current_user)
                flash('您的密码修改成功')
                return redirect(url_for('main.index'))
    else:
        flash('无法修改密码。')
        return redirect(url_for('main.index'))
    return render_template('auth/changepassword.html', form=form)
