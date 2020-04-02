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

import rmessages

def send_alert():
    chats = mdb.allchats()

    for chat in chats:
        try:
            bot.send_message(chat, rmessages.getMessage())
        except ApiException:
            mdb.removechat(chat)

def send_remember():
    message = '''Mantenerse informado de las medidas adoptadas por las autoridades de salud de su país forma parte de tu obligación como ciudadano en la lucha contra la pandemia de la COVID-19. En unos minutos, justo a las 11 de la mañana, el Ministerio de Salud Pública de la República de Cuba comenzará su habitual Conferencia de Prensa. No dejes de verla, mantenernos informados es vital para apoyar a las autoridades a erradicar este mal que nos azota a todos.'''

    chats = mdb.allchats()

    for chat in chats:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

@server.route('/remember')
def remember():
    Pool().apply_async(send_remember)

    return jsonify({
        'message': 'remember',
    })

@server.route('/alert')
def alert():
    Pool().apply_async(send_alert)

    return jsonify({
        'message': 'alert',
    })

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