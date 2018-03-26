import pymongo

with open('../pwd.txt') as o:
    key = o.readline()

client = pymongo.MongoClient('localhost', 27017)

posts = client.roddit.posts
subs = client.roddit.subs
users = client.roddit.users

def addPost(post):
    posts.insert_one(post)
    print('Added post:',post.title)

def getPosts(sub):
    if sub == 'all':
        return posts.find()
    else:
        return posts.find({'sub':sub})

def hot(sub):
    return list(getPosts(sub))

def new(sub):
    return list(posts.find().sort('date',pymongo.DECENDING))

def top(sub):
    return list(posts.find().sort('score',pymongo.DECENDING))

def getSub(name):
    return subs.find_one({'name':name})