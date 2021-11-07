import pyrebase
from tokens import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def get_pairs(server):
    pairs = db.child("server_pairs").child(server.id).get()
    return pairs.each()[0].val()

def upload_pairs(guild, pairs):
    
    # Upload data to cloud

    db.child("server_pairs").child(guild.id).push(pairs)        