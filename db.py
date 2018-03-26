import pymongo

client = pymongo.MongoClient('localhost', 27017)

posts = client.roddit.posts

def addPost(post):
    posts.insert_one(post)
    print('Added post:',post.title)

def getPosts(sub):
    return list(posts.find({'sub':sub}))