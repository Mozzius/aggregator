#!/usr/bin/env python3
import pymongo
import re
import hashlib
import datetime
from string import ascii_letters, digits

client = pymongo.MongoClient('localhost', 27017)

posts = client.roddit.posts
subs = client.roddit.subs
users = client.roddit.users

PERMITTED_CHARS = ascii_letters + digits + '_-'

def sha256(msg):
    return hashlib.sha256(msg.encode('utf-8')).digest()

def alphanumericify(msg):
    return "".join([ch for ch in msg if ch in PERMITTED_CHARS])

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

def addUser(name,email,password):
    # need to get bleach working
    name = alphanumericify(name)
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',email)
    password = sha256(password)
    if match and name != '' and users.find({'email':email}).count() != 0:
        users.insert_one({'name':name,'email':email,'password':password})
        return True
    else:
        return False

def addPost(uid,title,link,sub,text=''):
    title = alphanumericify(title)
    try:
        posts.insert_one({'title':title,'link':link,'score':10,'user_id':uid,'text':text,'date':datetime.datetime.utcnow()})
        return True
    except:
        return False

def createSub(uid,name,sidebar,primary,secondary):
    name = alphanumericify(name)
    sidebar = alphanumericify(sidebar)
    match1 = re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',primary)
    match2 = re.match('^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',secondary)
    if match1 and match2 and name != '' and sidebar != '':
        subs.insert_one({'name':name,'sidebar':sidebar,'creator':uid,'primary':primary,'secondary':secondary})

def verifyUser(email,password):
    user = users.find_one({'email':email})
    if user and user['password'] == sha256(password):
        return True
    else:
        return False

def getUserPosts(id):
    return list(posts.find({'user_id':id}).sort('date',pymongo.DESCENDING))