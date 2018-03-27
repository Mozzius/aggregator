from flask import Flask, render_template, url_for
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
    return render_template('roddit.html',page=page,posts=posts,type='sub')

@app.route('/r/<subname>/submit')
def submit(subname):
    page = db.getSub(subname)
    return render_template('roddit.html',page=page,type='submit')


@app.route('/u/<user>')
def user(user):
    user = db.getUser(user)
    print(user)
    posts = []
    if user:
        posts = db.getUserPosts(user['_id'])
    return render_template('roddit.html',page=user,posts=posts,type='user')

if __name__ == '__main__':
    app.run(port=80,debug=True,host='0.0.0.0')