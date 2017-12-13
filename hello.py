# !/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,redirect,url_for,flash
from flask import request, make_response, abort, session
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = '2922562067@qq.com'
app.config['MAIL_PASSWORD'] = 'luqfyhsdwlqadeed'
app.config['MAIL_DEBUG'] = True


db = SQLAlchemy(app)
mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
manager = Manager(app)

def send_email():
    msg = Message('hello', sender='2922562067@qq.com',  recipients=['xpl_@travelsky.com'])
    msg.body = "This is a first email"
    mail.send(msg)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

    users = db.relationship('User', backref='role')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
       return '<User %r>' % self.usernam

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

#db.create_all()

@app.route("/",  methods=['GET', 'POST'])
def index():
       user_agent = request.headers.get('User-Agent')
       response = make_response("<h1>hell response<h1>")
       response.set_cookie('answer', '42')
       #return redirect('http://www.baidu.com')
       name = None
       form = NameForm()
       if form.validate_on_submit():
           username = form.name.data
           user_list =  Role.query.all()
           user = User.query.filter_by(username=form.name.data).first()
           #send_email()
           if user is None:
               user = User(username = form.name.data)
               db.session.add(user)
               session['known'] = False
           else:
               session['known'] = True
          # old_name = session.get('name')
          # if old_name is not None and old_name != form.name.data:
          #     flash('Looks like you have changed your name!')
           session['name'] = form.name.data
           form.name.data = ''
           return redirect(url_for('index'))
       return render_template('index.html', current_time=datetime.utcnow(), form=form, name= session.get('name'), known = session.get('known', False))

@app.route('/user/<name>')
def user(name):
    if name ==  'li':
        abort(404)
    return  render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

#print app.url_map

if __name__ == "__main__":
    manager.run()