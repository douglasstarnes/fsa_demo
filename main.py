from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fsa_demo.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text())

    def __repr__(self):
        return '<Post %r>' % (self.title)


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def get_post(post_id):
    p = Post.query.get(post_id)
    return render_template('post.html', post=p)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')
    else:
        post_title = request.form['post_title']
        post_body = request.form['post_body']

        p = Post(title=post_title, body=post_body)
        db.session.add(p)
        db.session.commit()

        return redirect(url_for('index'))
