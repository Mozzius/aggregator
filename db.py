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

def getPosts(sub,sort):
    if sub == 'all':
        subPosts = posts.find()
    else:
        subPosts = posts.find({'sub':sub})
    if sort == 'hot':
        return list(subPosts)
    elif sort == 'new':
        return list(subPosts.sort('date',pymongo.DESCENDING))
    elif sort == 'top':
        return list(subPosts.sort('score',pymongo.DESCENDING))
    elif sort == 'controversial':
        return list(subPosts.sort('score',pymongo.ASCENDING))

def getSub(name):
    return subs.find_one({'name':name})

def getUser(name,prop='name'):
    return users.find_one({prop:name})

def getUserPosts(id):
    return list(posts.find({'user_id':id}).sort('date',pymongo.DESCENDING))