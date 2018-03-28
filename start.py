from flask import Flask, render_template, url_for, redirect, session, request
import db

app = Flask(__name__)

@app.route('/')
@app.route('/r/<subname>')
@app.route('/r/<subname>/<sort>')
def sub(subname='frontpage',sort='hot'):
    page = db.getSub(subname)
    if sort == 'hot':
        posts = db.hot(subname)
    elif sort == 'new':
        posts = db.new(subname)
    elif sort == 'top':
        posts = db.top(subname)
    elif sort == 'top':
        posts = db.top(subname)
    elif sort == 'controversial':
        posts = db.controversial(subname)
    else:
        posts = False
    return render_template('roddit.html',page=page,posts=posts,type='sub',user={'name':'mozzius'})

@app.route('/r/<subname>/submit')
def submit(subname):
    page = db.getSub(subname)
    return render_template('roddit.html',page=page,type='submit')

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        if db.checkLogin(form['email'],form['password']):
            session['loggedin'] = True
            session['name'] = db.user['name']
            session['email'] = db.user['email']
            return redirect('/')
        else:
            return render_template('login.html', fail = True)
    else:
        if 'loggedin' in session and session['loggedin'] == True:
            return redirect('/')
        return render_template('login.html', fail=False)

@app.route('/signout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/u/<user>')
def user(user):
    user = db.getUser(user)
    posts = []
    if user:
        posts = db.getUserPosts(user['_id'])
        print(posts)
    return render_template('roddit.html',page=user,posts=posts,type='user')

if __name__ == '__main__':
    app.run(port=80,debug=True,host='0.0.0.0')