from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:password@localhost/flask_todo_db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.text}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo = request.form['todo']
        db.session.add(Todo(text=todo))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', todos=Todo.query.all())

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)