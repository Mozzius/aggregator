from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return sub('frontpage')

@app.route('/r/<subname>')
def sub(subname):
    posts = [{
        'thumbnail': 'https://i.imgur.com/myE1tkjs.jpg',
        'title': 'Cute lil pupper',
        'comments': 3,
        'user': 'mozzius',
        'sub': 'rarepuppers'
    },{
        'thumbnail': 'https://i.imgur.com/myE1tkjs.jpg',
        'title': 'Pupperinos are the best!',
        'comments': 0,
        'user': 'mozzius',
        'sub': 'rarepuppers'
    },{
        'thumbnail': 'https://i.imgur.com/myE1tkjs.jpg',
        'title': 'woofer alert',
        'comments': 5,
        'user': 'mozzius',
        'sub': 'rarepuppers'
    }]
    posts = False
    return render_template('roddit.html',subName=subname,posts=posts)

if __name__ == '__main__':
    app.run(port=80,debug=True,host='0.0.0.0')