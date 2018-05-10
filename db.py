#!/usr/bin/env python3
import pymongo
import bleach
import re
import hashlib
import datetime
from bson import ObjectId
from string import ascii_letters, digits

client = pymongo.MongoClient('localhost', 27017)

posts = client.roddit.posts
subs = client.roddit.subs
users = client.roddit.users

PERMITTED_CHARS = ascii_letters + digits + '_-'

def sha256(msg):
    return hashlib.sha256(msg.encode('utf-8')).digest()

def alphanumericify(msg,extra=''):
    return "".join([ch for ch in msg if ch in PERMITTED_CHARS+extra])

def addPost(post):
    posts.insert_one(post)
    print('Added post:',post.title)

def getPosts(subname,sort):
    sub = getSub(subname)
    if sub != None:
        if subname == 'all':
            subPosts = posts.find()
        else:
            subPosts = posts.find({'sub_id':sub['_id']})
        if sort == 'hot':
            return list(subPosts)
        elif sort == 'new':
            return list(subPosts.sort('date',pymongo.DESCENDING))
        elif sort == 'top':
            return list(subPosts.sort('score',pymongo.DESCENDING))
        elif sort == 'controversial':
            return list(subPosts.sort('score',pymongo.ASCENDING))
    else:
        return None

def getPost(name,prop='_id'):
    return posts.find_one({prop:name})

def getSub(name,prop='name'):
    return subs.find_one({prop:name})

def getUser(name,prop='name'):
    return users.find_one({prop:name})

def getComments(name,post='post_id'):
    return list(comments.find({prop,name}))

def addUser(name,email,password):
    # need to get bleach working
    name = alphanumericify(name)
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
        print(title != '')
        assert title != ''
        assert text != ''
        sub = getSub(subname)
        thumbnail = link # fix this
        posts.insert_one({'title':title,'link':link,'thumbnail':thumbnail,'score':10,'sub_id':sub['_id'],'user_id':ObjectId(uid),'text':text,'date':datetime.datetime.utcnow()})
        print('Inserted Post:',title)
        return True
    except:
        print('Error inserting post')
        return False

def createSub(uid,name,sidebar,primary,secondary):
    name = alphanumericify(name).lower()
    sidebar = bleach.clean(sidebar)
    match1 = re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',primary)
    match2 = re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',secondary)
    #and name != '' and sidebar != ''
    if match1 and match2 and subs.find({'name':name}).count() == 0:
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