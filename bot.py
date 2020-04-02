import config

import telebot

import requests

import mdb

bot = telebot.TeleBot(config.token)

def summary():
    message = "🤒 Diagnosticados: {}\n🔬 Diagnosticados hoy: {}\n🤧 Activos: {}\n😃 Recuperados: {}\n🤩 Índice de Recuperación: {}%\n✈️ Evacuados: {}\n⚰️ Fallecidos: {}\n😵 Mortalidad: {}%\n🏥 Ingresados {}\n📆 Actualizado: {}\n\n Más Información en @covid19cubadata_bot"

    data = requests.get(config.api_url + '/summary').json()

    return message.format(
        data['Diagnosticados'],
        data['DiagnosticadosDay'],
        data['Activos'],
        data['Recuperados'],
        data['Recuperacion'],
        data['Evacuados'],
        data['Muertes'],
        data['Mortalidad'],
        data['Ingresados'],
        data['Updated'],
    )

def about():
    return '''Covid19 Cuba Data Telegram Bot 

Web de Covid19 Cuba Data:

🌐 https://covid19cubadata.github.io/
🇨🇺 http://www.cusobu.nat.cu/covid/

📲 Aplicación Movil:

Apklis: https://www.apklis.cu/application/club.postdata.covid19cuba
Github: https://github.com/covid19cuba/covid19cuba-app/releases/

👨‍💻Bot Source Code:

https://github.com/correaleyval/covid19cuba_bot
https://github.com/correaleyval/covid19cuba_api
https://github.com/correaleyval/covid19cuba_async'''

@bot.message_handler(commands=['start'])
def start_summary(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    bot.reply_to(
        message,
        summary()
    )

@bot.message_handler(commands=['about'])
def about_handler(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    bot.reply_to(
        message,
        about()
    )

@bot.message_handler(commands=['summary'])
def send_summary(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    bot.reply_to(
        message,
        summary()
    )

    graph1 = requests.get(config.api_url + '/summary_graph1').content
    graph2 = requests.get(config.api_url + '/summary_graph2').content

    with open('summary1.png', 'wb') as f:
        f.write(graph1)

    with open('summary2.png', 'wb') as f:
        f.write(graph2)

    bot.send_photo(cid, open('summary1.png', 'rb'))
    bot.send_photo(cid, open('summary2.png', 'rb'))

@bot.message_handler(commands=['evolution'])
def send_evolution(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    evolution_graph = requests.get(config.api_url + '/evolution').content
    fallecidos_graph = requests.get(config.api_url + '/evolution_fallecidos').content

    with open('evolution.png', 'wb') as f:
        f.write(evolution_graph)
    
    with open('evolution_fallecidos.png', 'wb') as f:
        f.write(fallecidos_graph)

    bot.send_photo(cid, open('evolution.png', 'rb'))
    bot.send_photo(cid, open('evolution_fallecidos.png', 'rb'))


@bot.message_handler(commands=['sexo'])
def send_sexo(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    sexo_graph = requests.get(config.api_url + '/sexo').content
    data = requests.get(config.api_url + '/sexo_text').json()

    with open('sexo.png', 'wb') as f:
        f.write(sexo_graph)

    texto = 'Hombres: {} | Mujeres {}'.format(data['hombres'], data['mujeres'])

    bot.send_photo(cid, open('sexo.png', 'rb'), texto)

@bot.message_handler(commands=['modo'])
def send_modo(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    modo_graph = requests.get(config.api_url + '/modo').content

    with open('modo.png', 'wb') as f:
        f.write(modo_graph)

    bot.send_photo(cid, open('modo.png', 'rb'))

@bot.message_handler(commands=['casos_extranjeros'])
def send_casos_extranjeros(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    casos_extranjeros_graph = requests.get(config.api_url + '/casos_extranjeros').content

    with open('casos_extranjeros.png', 'wb') as f:
        f.write(casos_extranjeros_graph)

    bot.send_photo(cid, open('casos_extranjeros.png', 'rb'))

@bot.message_handler(commands=['nacionalidad'])
def send_nacionalidad(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    nacionalidad_graph = requests.get(config.api_url + '/nacionalidad').content
    data = requests.get(config.api_url + '/nacionalidad_text').json()

    with open('nacionalidad.png', 'wb') as f:
        f.write(nacionalidad_graph)

    texto = 'Cubanos: {} | Extranjeros {}'.format(data['Cubanos'], data['Extranjeros'])

    bot.send_photo(cid, open('nacionalidad.png', 'rb'), texto)

@bot.message_handler(commands=['edad'])
def send_edad(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    edad_graph = requests.get(config.api_url + '/edad').content

    with open('edad.png', 'wb') as f:
        f.write(edad_graph)

    bot.send_photo(cid, open('edad.png', 'rb'))

@bot.message_handler(commands=['test'])
def send_test(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    test_graph = requests.get(config.api_url + '/test').content

    with open('test.png', 'wb') as f:
        f.write(test_graph)

    bot.send_photo(cid, open('test.png', 'rb'))

@bot.message_handler(commands=['provincias'])
def send_provincias(message):
    cid = message.chat.id

    bot.send_chat_action(cid, 'typing')
    mdb.savechat(cid)

    provincias_graph = requests.get(config.api_url + '/provincias').content
    municipios_graph = requests.get(config.api_url + '/municipios').content

    with open('provincias.png', 'wb') as f:
        f.write(provincias_graph)

    with open('municipios.png', 'wb') as f:
        f.write(municipios_graph)

    bot.send_photo(cid, open('provincias.png', 'rb'))
    bot.send_photo(cid, open('municipios.png', 'rb'))

@bot.message_handler(commands=['notify'])
def notify(message):
    cid = message.chat.id
    mid = message.message_id

    cant_users = len(mdb.allchats())

    bot.reply_to(message, 'CID: {} MID {} USERS {}'.format(cid, mid, cant_users))

from telebot.apihelper import ApiException

def send_notifiation(cid, mid):
    users = mdb.allchats()

    for uid in users:
        try:
            bot.forward_message(uid, cid, mid)
        except ApiException:
            mdb.removechat(uid)

from multiprocessing import Pool

@bot.message_handler(content_types=['document', 'text', 'photo'])
def notifications(message):
    cid = message.chat.id
    mid = message.message_id

    if str(cid) == str(config.admin):
        Pool().apply_async(send_notifiation, args=(cid, mid))
    else:
        bot.reply_to(message, 'Seleccione un comando de la lista [/]')


### INLINE MODE

from telebot import types

@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle(
            '1',
            'Covid19 Cuba Data',
            types.InputTextMessageContent(
                summary(),
                parse_mode='HTML'
            )
        )

        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


import time
import sys

def main_loop():
    bot.polling(True)
    
    while 1:
        time.sleep(3)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)