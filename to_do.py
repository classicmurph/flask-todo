import sqlite3
from flask import Flask, request, g, redirect, url_for, \
     render_template, flash
from contextlib import closing


DATABASE = '/tmp/todo.db'
DEBUG = True
SECRET_KEY = 'development-key'


app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_tasks():
    cur = g.db.execute('select id, text from tasks order by id desc')
    tasks = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('to_do.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_entry():
    task = request.form['text']
    g.bd.execute('insert into tasks (text) values (?)', (task))
    g.db.commit()
    flash('New task was successfully posted')
    return redirect(url_for('show_tasks'))


@app.route('/', methods=['POST'])
def remove_task():
    for selected in request.form.getlist('task'):
        g.db.execute('delete from tasks where id = ?', selected)


if __name__ == '__main__':
    app.run()
