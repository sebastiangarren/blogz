from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#TODO: I still need to create these with Python

class Blog_post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

#Each blog post has a title and a body

    def __init__(self, name, body):
        self.name = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def index():

#TODO: rewrite blogz.html
#1) The action on blogz routes to '/new_post'
#2) blogs queries database
#3) and returns all the Blog_post.name and Blog_post.body

    if request.method == 'POST':
        post_name = request.form['new_post_name']
        post_body = request.form['new_post_body']
        new_post = Blog_post(post_name, post_body)
        db.session.add(new_post)
        db.session.commit()

#TODO:Fix parameters to match blogz.HTML

    posts = Blog_post.query.all()
    return render_template('blogz.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)


@app.route('/new_post', methods=['POST'])
def new_post():

#TODO:I think this only needs to render new_post.html

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()