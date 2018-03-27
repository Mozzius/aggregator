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
    # TODO: Sorting algorithm
    return list(getPosts(sub))

def new(sub):
    return list(getPosts(sub).sort('date',pymongo.DESCENDING))

def top(sub):
    return list(getPosts(sub).sort('score',pymongo.DESCENDING))

def controversial(sub):
    return list(getPosts(sub).sort('score',pymongo.ASCENDING))

def getSub(name):
    return subs.find_one({'name':name})

def getUser(name):
    return users.find_one({'name':name})

def getUserPosts(id):
    return users.find({'user_id':id}).sort('date',pymongo.DESCENDING)