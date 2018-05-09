#!/usr/bin/env python3
from flask import Flask, render_template, url_for, redirect, session, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
import hashlib
from bson import ObjectId

try:
    import db
except ImportError:
    import aggregator.db as db

app = Flask(__name__)
login = LoginManager(app)

def sha256(msg):
    return hashlib.sha256(msg.encode('utf-8')).digest()

class User():
    def __init__(self,user):
        self.name = user['name']
        self.id = str(user['_id'])
        self.email = user['email']

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

@login.user_loader
def load_user(userid):
    user = db.getUser(ObjectId(userid),'_id')
    if user:
        return User(user)
    else:
        return None

@app.route('/')
@app.route('/r/<subname>')
@app.route('/r/<subname>/<sort>')
def sub(subname='frontpage',sort='hot'):
    page = db.getSub(subname.lower())
    if page != None:
        posts = db.getPosts(subname.lower(),sort)
        newposts = posts
        for i in range(len(posts)):
            newposts[i]['user_name'] = db.getUser(posts[i]['user_id'],'_id')['name']
            newposts[i]['sub_name'] = db.getSub(posts[i]['sub_id'],'_id')['name']
        return render_template('roddit.html',page=page,posts=newposts,type='sub')
    else:
        return render_template('roddit.html',page=page,type='sub')

@app.route('/r/<subname>/submit',methods=['GET','POST'])
@login_required
def submit(subname):
    page = db.getSub(subname.lower())
    if request.method == 'POST':
        form = request.form
        fail = db.addPost(current_user.get_id(),form['title'],form['link'],subname,form['text'])
        if fail:
            return render_template('roddit.html',page=page,type='submit',fail=True)
        else:
            return redirect('/r/'+subname)
    return render_template('roddit.html',page=page,type='submit',fail=False)

@app.route('/createsub',methods=['GET','POST'])
@login_required
def createsub():
    if request.method == 'POST':
        form = request.form
        fail = db.createSub(current_user.id,form['name'],form['sidebar'],form['primary'],form['secondary'])
        if fail:
            return render_template('roddit.html',type='makesub',fail=True)
        else:
            return redirect('/r/'+form['name'].lower())
    else:
        return render_template('roddit.html',type='makesub',fail=False)

@login.unauthorized_handler
def unauthHandler():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = request.form
        if db.verifyUser(form['email'],form['password']):
            user = db.getUser(form['email'],'email')
            login_user(User(user))
            return redirect('/')
        else:
            return render_template('roddit.html',type='login',fail=True)
    else:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('roddit.html',type='login',fail=False)

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        if db.addUser(form['username'],form['email'],form['password']):
            user = db.getUser(form['email'],'email')
            login_user(User(user))
            return redirect('/')
        else:
            return render_template('roddit.html',type='signup',fail=True)
    else:
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('roddit.html',type='signup',fail=False)

@app.route('/u/<user>')
def user(user):
    user = db.getUser(user)
    posts = []
    if user:
        posts = db.getUserPosts(user['_id'])
        newposts = posts
        for i in range(len(posts)):
            newposts[i]['user_name'] = db.getUser(posts[i]['user_id'],'_id')['name']
            newposts[i]['sub_name'] = db.getSub(posts[i]['sub_id'],'_id')['name']
    return render_template('roddit.html',page=user,posts=newposts,type='user')

if __name__ == '__main__':
    app.secret_key = 'localhost'
    app.run(port=80,debug=True,host='127.0.0.1')