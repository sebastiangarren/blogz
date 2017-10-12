from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

#The Database is running, but it also needs cleaning.

class Blog_post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

#Each blog post has a title and a body

    def __init__(self,title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog_post %r>' % self.title

def get_blog_posts():
    posts = Blog_post.query.order_by(Blog_post.id).all()
    return posts

@app.route('/blog', methods=['POST', 'GET'])
def index():
    
#1) The action on blogz routes to '/new_post'
#2) blogs queries database
#3) and returns all the Blog_post.name and Blog_post.body

    if request.method == 'POST':
        post_name = request.form['new_post_name']
        post_body = request.form['new_post_body']
        new_post = Blog_post(post_name, post_body)

        if new_post.body == '' or new_post.title == '':
            flash("Every post must have text in the title and the body.", "error")
            return render_template("/new_post.html", new_post_name=post_name, new_post_body=post_body)
        else:
            db.session.add(new_post)
            db.session.commit()
            return redirect('blog?id=' + str(new_post.id))
    
    if request.args:
        id_number = (request.args['id'])
        post = Blog_post.query.filter_by(id=id_number).first()
        return render_template('post_page.html', post=post)

    return render_template('blogz.html', posts=get_blog_posts())
    


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    
#new_post function only needs to return new_post.html
    
    return render_template("/new_post.html")

if __name__ == '__main__':
    app.run()