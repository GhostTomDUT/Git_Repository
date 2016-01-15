 #-*- coding: UTF-8 -*-
from flask import Flask, render_template, session, redirect, url_for, current_app
from datetime import datetime
from app.email import send_email
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/',methods = ['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        print (form.validate_on_submit())
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            session['known'] = False;
            user = User(username=form.name.data)
            db.session.add(user)
            if current_app.config['FLASKY_ADMIN']:
                 send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                            'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())