from flask import Flask
import os
from flask import render_template
from config import development
from flask_sqlalchemy import SQLAlchemy
from models import Posts, db
from flask_wtf import CSRFProtect
import forms
from flask import request
from flask import redirect, url_for

app = Flask(__name__)
SECRET_KEY = 'ULTRA_SECRET_KEY'
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_object(development)
csrf = CSRFProtect()

db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50))

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/posts")
def posts_index():
    posts = Posts.query.all()
    return render_template('posts/index.html', posts = posts)

@app.route("/posts/<id>")
def posts_show(id):
    post = Posts.query.get(id)
    return render_template('posts/show.html', post = post)

@app.route("/posts/new")
def posts_new():
    form = forms.PostForm(request.form)
    return render_template('posts/new.html', form = form)

@app.route("/posts/new", methods=['POST'])
def posts_create():
    form = forms.PostForm(request.form)
    if request.method == 'POST' and form.validate():
        content = form.content.data
        post = Posts(content=content)
        db.session.add(post)
        db.session.commit()
    return render_template('posts/show.html', post = post)

@app.route('/posts/<id>', methods=['POST'])
def post_delete(id):
    post = Posts.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts_index'))

@app.route('/posts/<id>/edit')
def edit_post(id):
    form = forms.PostForm()
    post = Posts.query.get(id)
    return render_template('posts/edit.html', form = form, post = post)

@app.route('/posts/<id>/edit', methods = ['POST'])
def update_post(id):
    form = forms.PostForm(request.form)
    post = Posts.query.get(id)
    post.content = form.content.data
    db.session.commit()
    return redirect(url_for('posts_index'))


if __name__ == '__main__':
    csrf.init_app(app)
    db.create_all()
    app.run(debug=True)
