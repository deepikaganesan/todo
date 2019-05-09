from flask import Flask, request
from flask import render_template
from flask import redirect

from flask import Flask, flash, redirect, render_template, request, session, abort
import os

from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('log.html')
    else:
        return render_template('todolist.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()  



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content


db.create_all()


@app.route('/index')
def tasks_list():
    tasks = Task.query.all()
    return render_template('todolist.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/index')


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/index')

    db.session.delete(task)
    db.session.commit()
    return redirect('/index')


@app.route('/done/<int:task_id>')
def resolve(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/index')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/index')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()

   
