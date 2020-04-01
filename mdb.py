import config

from pymongo import MongoClient

client = MongoClient(config.MONGO_URI)

db = client.tbot

def savechat(chatid):
    chat = {'chatid': chatid}

    chats = db.chats

    if not chats.find_one({'chatid': chatid}):
        chats.insert_one(chat)

def allchats():
    chats = db.chats

    todos = chats.find()

    return [e['chatid'] for e in todos]