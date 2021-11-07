import pyrebase
from tokens import config
import random

firebase = pyrebase.initialize_app(config)
db = firebase.database()

""" def store_user(msgID, userID):
    db.child("msgIDs").child(msgID).push(userID)

def retrieve_user(msgID):
    userID = db.child("msgIDs").child(msgID).get()
    return userID.val()[list(userID.val())[0]] """

def get_pairs(server):
    pairs = db.child("server_pairs").child(server.id).get()
    return pairs.each()[0].val()

def upload_pairs(guild, pairs):
    
    # Upload data to cloud

    db.child("server_pairs").child(guild.id).push(pairs)        

def access_santa(ctx):
    pass

def access_recipient(ctx):
    pass