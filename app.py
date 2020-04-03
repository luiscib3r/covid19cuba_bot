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
    message = '''Mantenerse informado de las medidas adoptadas por las autoridades de salud de su país forma parte de tu obligación como ciudadano en la lucha contra la pandemia de la COVID-19. En unos minutos, justo a las 11 a.m, el Ministerio de Salud Pública de la República de Cuba comenzará su habitual Conferencia de Prensa. No dejes de verla, mantenernos informados es vital para apoyar a las autoridades a erradicar este mal que nos azota a todos.'''

    chats = mdb.allchats()

    for chat in chats:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

def send_claps():
    message = '''Los nuevos super héroes merecen ser reverenciados. Gracias al  personal de salud por servir de ejército activo contra esta pandemia. Salgamos todos a dar un aplauso fuerte como merecen justo a las 9 pms'''

    chats = mdb.allchats()

    for chat in chats:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

def send_updating():
    message = '''ℹ️ Se esta trabajando en la actualizacion de los datos se enviara una notificacion cuando este lista la informacion'''

    chats = mdb.allchats()

    for chat in chats:
        try:
            bot.send_message(chat, message)
        except ApiException:
            mdb.removechat(chat)

@server.route('/updating', methods=['POST'])
def updating():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'alert'
        })

    Pool().apply_async(send_updating)

    return jsonify({
        'message': 'updating',
    })

@server.route('/claps', methods=['POST'])
def claps():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'claps'
        })


    Pool().apply_async(send_claps)

    return jsonify({
        'message': 'claps',
    })

@server.route('/remember', methods=['POST'])
def remember():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'remember'
        })

    Pool().apply_async(send_remember)

    return jsonify({
        'message': 'remember',
    })

@server.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'alert'
        })

    Pool().apply_async(send_alert)

    return jsonify({
        'message': 'alert',
    })

@server.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()

    if data['token'] != config.STOKEN:
        return jsonify({
            'message': 'notify'
        })

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