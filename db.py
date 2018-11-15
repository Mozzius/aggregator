#!/usr/bin/env python3
import pymongo
import bleach
import re
import hashlib
import datetime
from bson import ObjectId
from string import ascii_letters, digits
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from math import log

client = pymongo.MongoClient('localhost', 27017)

posts = client.roddit.posts
subs = client.roddit.subs
users = client.roddit.users
comments = client.roddit.comments

PERMITTED_CHARS = ascii_letters + digits + '_-'

def alphanumericify(msg,extra=''):
    # for creating clean sub names
    return "".join([ch for ch in msg if ch in PERMITTED_CHARS+extra])

def sha256(msg):
    return hashlib.sha256(msg.encode('utf-8')).digest()

def addPost(post):
    posts.insert_one(post)
    print('Added post:',post.title)

def getPosts(subname,sort):
    sub = getSub(subname)
    if sub != None:
        if subname == 'all':
            subPosts = posts.find().limit(30)
        else:
            subPosts = posts.find({'sub_id':sub['_id']}).limit(30)
        if sort == 'hot':
            return list(subPosts.sort('score',pymongo.DESCENDING))
        elif sort == 'new':
            return list(subPosts.sort('date',pymongo.DESCENDING))
        elif sort == 'top':
            return list(subPosts.sort('upvotes',pymongo.DESCENDING))
        elif sort == 'controversial':
            return list(subPosts.sort('downvotes',pymongo.ASCENDING))
    else:
        return None

def getPost(name,prop='_id'):
    if prop == '_id':
        name = ObjectId(name)
    return posts.find_one({prop:name})

def getSub(name,prop='name'):
    return subs.find_one({prop:name})

def getUser(name,prop='name'):
    return users.find_one({prop:name})

def getComments(name,prop='post_id'):
    return list(comments.find({prop:name}))

def addUser(name,email,password):
    # cleaning inputs
    name = bleach.clean(name)
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',email)
    password = sha256(password)
    if match and name != '' and users.find({'email':email}).count() == 0 and users.find({'name':name}).count() == 0:
        users.insert_one({'name':name,'email':email,'password':password})
        return True
    else:
        return False

def addPost(uid,title,link,subname,text=''):
    title = bleach.clean(title)
    text = bleach.clean(text)
    try:
        assert title != ''
        sub = getSub(subname)
        thumbnail = link # fix this
        post = {
            'title':title,
            'link':link,
            'thumbnail':thumbnail,
            'upvotes':1,
            'downvotes':0,
            'score':0,
            'sub_id':sub['_id'],
            'user_id':ObjectId(uid),
            'text':text,
            'date':datetime.datetime.utcnow()
        }
        posts.insert_one(post)
        print('Inserted Post:',title)
        calcPostScore(post)
        return True
    except:
        print('Error inserting post')
        return False

def createSub(uid,name,sidebar,primary,secondary):
    name = alphanumericify(name).lower()
    sidebar = bleach.clean(sidebar)
    sidebar = bleach.linkify(sidebar)
    match1 = re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',primary)
    match2 = re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',secondary)
    #and name != '' and sidebar != ''
    if match1 and match2 and subs.find({'name':name}).count() == 0 and name != 0:
        subs.insert_one({'name':name,'sidebar':sidebar,'creator':uid,'primary':primary,'secondary':secondary})
        return True
    else:
        return False

def verifyUser(email,password):
    user = users.find_one({'email':email})
    if user and user['password'] == sha256(password):
        return True
    else:
        return False

def getUserPosts(id):
    return list(posts.find({'user_id':id}).sort('date',pymongo.DESCENDING))

### WARNING: BROKEN AS HECK ###

def getThumb(url):
    pass

def generateThumb(url):
    # get the largest image from the url
    page = requests.get(url)
    print(page)
    soup = BeautifulSoup(page.text,'html5lib')
    imgs = dict()
    for img in soup.find_all('img'):
        print(img.get('src'))
        if img.get('src',False):
            print(img.get('src'))
            imgs[img.get('src'):img.get('width', 50)]
    print('imgs:',imgs)
    if imgs != {}:
        src = max(imgs, key=lambda k: imgs[k])
        print(src)
    else:
        return None

#generateThumb('https://imgur.com/gallery/ZpRhfju')

###############################

def upvotePost(id,user_id):
    post = posts.find_one({'_id':id})
    user = users.find_one({'_id':user_id})
    post['upvotes'] += 1
    user['upvoted'].append(id)
    posts.update({'_id':id},{'$set':post})
    users.update({'_id':id},{'$set':post})

def downvotePost(id):
    post = posts.find_one({'_id':id})
    user = users.find_one({'_id':user_id})
    post['downvotes'] += 1
    user['downvoted'].append(id)
    posts.update({'_id':id},{'$set':post})

def unvotePost(id,user_id):
    post = posts.find_one({'_id':id})
    user = users.find_one({'_id':user_id})
    if id in user['upvoted']:
        post['upvotes'] -= 1
        user['upvoted'].remove(id)
    else:
        post['downvotes'] -= 1
        user['downvoted'].remove(id)
    posts.update({'_id':id},{'$set':post})
    users.update({'_id':id},{'$set':post})

epoch = datetime(1970, 1, 1)

def epochSeconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def calcPostScore(post):
    # reddit's hot algorithm
    # https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9
    s = post['upvotes'] - post['downvotes']
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epochSeconds(post['date']) - 1134028003
    posts['score'] = round(sign * order + seconds / 45000, 7)
    # update the database
    posts.update({'_id':post['_id']},{'$set':post})