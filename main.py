from flask import Flask, request, redirect, render_template, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cgi
from app import app, db
from models import Author, Blog_post

#Initialize Classes

#Global functions

#require login
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')

#return all posts indiscriminately and with extreme prejudice
def get_blog_posts():
    posts = Blog_post.query.all()
    return posts

#return all users undiscriminately and with extreme prjudice
def get_users():
    users = Author.query.all()
    return users

#display username if logged in
def get_session_name():
    if session['username']:
        session_name = session['username']
        return session_name

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    
#1) The action on blogz routes to '/new_post'
#2) blogs queries database
#3) and returns all the Blog_post.name and Blog_post.body

    if request.method == 'POST':
        post_name = request.form['new_post_name']
        post_body = request.form['new_post_body']
        username = session['username']
        author = Author.query.filter_by(username=username).first()
        pub_date = datetime.utcnow()
        new_post = Blog_post(post_name, post_body, author.id, pub_date)

        if new_post.body == '' or new_post.title == '':
            flash("Every post must have text in the title and the body.", "error")
            return render_template("/new_post.html", new_post_name=post_name, new_post_body=post_body, session_name=get_session_name())
        else:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id=' + str(new_post.id))

    #for each type of args I need to render a different type of page

    if request.args.get('id'):
        post_number = request.args['id']
        post = Blog_post.query.filter_by(id=post_number).first()
        user_id = post.author_id
        user = Author.query.filter_by(id=user_id).first()
        return render_template('post_page.html', post=post, user=user)
    if request.args.get('user'):
        user_number = request.args['user']
        posts = Blog_post.query.filter_by(author_id=user_number).all()
        user = Author.query.filter_by(id=user_number).first()
        return render_template('SingleUser.html', posts=posts, user=user, session_name=get_session_name())

    return render_template('blogz.html', posts=get_blog_posts(), users=get_users(), session_name=get_session_name())
    


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    
#new_post function only needs to return new_post.html

    return render_template("new_post.html", session_name=get_session_name())

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = Author.query.filter_by(username=username).first()
        if not existing_user and password == verify:
            new_user = Author(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/new_post')
        elif existing_user:
            flash('That username already exists. Try a different one.', 'error')
        if len(password) < 3:
            flash('Your password must be three characters or longer.', 'error')
        if password != verify:
            flash('Passwords do not match.', 'error')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Author.query.filter_by(username=username).first()
        #check validity
        if user and user.password == password:
            session['username'] = username
            return redirect("/new_post")
        elif not user:
            flash("Invalid username.", "error")
        else:
            if password != user.password:
                flash("Username and password do not match.", "error")
                return render_template('login.html')

    return render_template('login.html')

#Render a list of users for index.html, click user name to see user's posts.
@app.route('/')
def index():
    return render_template('index.html', users=get_users(), session_name=get_session_name())

#logout function handles POST to /logout, delete username from session, redirect to blog
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()

#signup.html is a signup page
#login.html is a standard route
#index.html
#singleUser.html
#
#new route handlers signup, login, index

#
#For /login page:
# User enters a username that is stored in the database with the correct password 
#   and is redirected to the /newpost page with their username being stored in a session.
# User enters a username that is stored in the database 
#   with an incorrect password and is redirected to the /login page with a message that their password is incorrect.
# User tries to login with a username that is not stored in the database 
#   and is redirected to the /login page with a message that this username does not exist.
# User does not have an account and clicks "Create Account" and is directed to the /signup page.

# For /signup page:
# User enters new, valid username, a valid password, and 
#   verifies password correctly and is redirected to the 
#   '/newpost' page with their username being stored in a session.
# User leaves any of the username, password, or verify 
#   fields blank and gets an error message that one or more fields are invalid.
# User enters a username that already exists and gets an   error message that username already exists.
# User enters different strings into the password and 
#   verify fields and gets an error message that the passwords do not match.
# User enters a password or username less than 
#   3 characters long and gets either an invalid username or an invalid password message.

