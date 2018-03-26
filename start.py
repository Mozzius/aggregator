from flask import Flask, render_template, url_for
import db

app = Flask(__name__)

@app.route('/')
@app.route('/r/<subname>')
@app.route('/r/<subname>/<sort>')
def sub(subname='frontpage',sort='hot'):
    if sort == 'post':
        sort = 'hot'
    page = db.getSub(subname)
    if sort == 'hot':
        posts = db.hot(subname)
    elif sort == 'new':
        posts = db.new(subname)
    else:
        posts = False
    return render_template('roddit.html',page=page,posts=posts)

if __name__ == '__main__':
    app.run(port=2018,debug=True,host='0.0.0.0')