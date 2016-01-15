 #-*- coding: UTF-8 -*-
from wtforms import StringField, SubmitField
from flask.ext.wtf import Form
from wtforms.validators import DataRequired
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class NameForm(Form):
    name = StringField('如何称呼?', validators=[DataRequired()])
    submit = SubmitField('提交')

