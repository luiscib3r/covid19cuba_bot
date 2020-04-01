import config

from flask import Flask, request, jsonify

from bot import bot, summary

import telebot

import mdb

from telebot.apihelper import ApiException

from multiprocessing import Pool

server = Flask(__name__)

def send_notify():
    chats = mdb.allchats()

    for chat in chats:
        try:
            bot.send_message(chat, 'ℹ️ La base de datos se ha actualizado\n\n' + summary())
        except ApiException:
            mdb.removechat(chat)

@server.route('/notify')
def notify():
    Pool().apply_async(send_notify)    

    return jsonify({
        'message': 'notify'
    })

@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(
            request.stream.read().decode("utf-8")
        )]
    )

    return "!", 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://covid19cuba-bot.herokuapp.com/' + config.token)
    return "!", 200