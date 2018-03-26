from flask import Flask, render_template, url_for
import db

app = Flask(__name__)

@app.route('/')
def index():
    return sub('frontpage')

@app.route('/r/<subname>')
def sub(subname):
    posts = db.getPosts(subname)
    print(posts)
    return render_template('roddit.html',subName=subname,posts=posts)

if __name__ == '__main__':
    app.run(port=2018,debug=True,host='0.0.0.0')