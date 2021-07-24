import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

Bootstrap(app)

app.config['SECRET_KEY'] = os.environ['day_56_key']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)
    is_complete = db.Column(db.Boolean, nullable=False)

class TaskForm(FlaskForm):
    activity = StringField("Task", validators=[DataRequired()])
    due_date = StringField("Due Date", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    tasks = Task.query.all()
    return render_template("home.html", tasks=tasks)

@app.route("/add", methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            activity = form.activity.data,
            due_date = form.due_date.data,
            is_complete = False
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('task.html', form=form, title="Add a Task")

@app.route("/edit/<int:task_id>", methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    form = TaskForm(
        activity = task.activity,
        due_date = task.due_date
    )
    if form.validate_on_submit():
        task.activity = form.activity.data
        task.due_date = form.due_date.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("task.html", form=form, title="Edit Task")

@app.route("/delete/<int:task_id>", methods=['GET', 'POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/finish_task/<int:task_id>", methods=['GET', 'POST'])
def finish_task(task_id):
    task = Task.query.get(task_id)
    task.is_complete = not task.is_complete
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)