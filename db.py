import pyrebase
from tokens import config
import random

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def store_user(msgID, userID):
    db.child("msgIDs").child(msgID).push(userID)

def retrieve_user(msgID):
    userID = db.child("msgIDs").child(msgID).get()
    return userID.val()[list(userID.val())[0]]

def randomize_users(guild, users):
    try:
        if users == "all":
            users = guild.members

        users = users.split(",")
        random.shuffle(users)
        
        # Key = Santa, Value = Recipient
        pairs = {}

        # DM user at last spot that their person is the first person
        for i in range(len(users) - 1):
            # DM user that their recipient is user in next pos
            
            # Store dict of users and recipients
            pairs[users[i].name + "#" + users[i].avatar] = users[i+1]
        
        # Send message that all users have been sent their recipient and upload data to cloud
    
        db.child("server_pairs").child('''serverID''').put(pairs)            

    except:
        # Send failure message
        pass

def access_santa(userID):
    try:
    except:
        # DM they aren't in a Secret Santa in this server

def access_recipient(userID):
    try:
    except:
        # DM they aren't in a Secret Santa in this server

store_user(123, "Drin#879")

print(retrieve_user(123))