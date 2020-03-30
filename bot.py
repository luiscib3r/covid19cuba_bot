import config

import telebot

import requests

bot = telebot.TeleBot(config.token)

def summary():
    message = "Diagnosticados: {}\nActivos: {}\nRecuperados: {}\nEvacuados: {}\nMuertes: {}\nActualizado: {}"

    data = requests.get(config.api_url + '/summary').json()

    return message.format(
        data['Diagnosticados'],
        data['Activos'],
        data['Recuperados'],
        data['Evacuados'],
        data['Muertes'],
        data['Updated'],
    )

    

@bot.message_handler(commands=['start', 'summary'])
def send_summary(message):
    bot.reply_to(
        message,
        summary()
    )

@bot.message_handler(commands=['evolution'])
def send_evolution(message):
    cid = message.chat.id

    evolution_graph = requests.get(config.api_url + '/evolution').content

    with open('evolution.png', 'wb') as f:
        f.write(evolution_graph)

    bot.send_photo(cid, open('evolution.png', 'rb'))


@bot.message_handler(commands=['sexo'])
def send_sexo(message):
    cid = message.chat.id

    sexo_graph = requests.get(config.api_url + '/sexo').content
    data = requests.get(config.api_url + '/sexo_text').json()

    with open('sexo.png', 'wb') as f:
        f.write(sexo_graph)

    texto = 'Hombres: {} | Mujeres {}'.format(data['hombres'], data['mujeres'])

    bot.send_photo(cid, open('sexo.png', 'rb'), texto)

@bot.message_handler(commands=['modo'])
def send_modo(message):
    cid = message.chat.id

    modo_graph = requests.get(config.api_url + '/modo').content

    with open('modo.png', 'wb') as f:
        f.write(modo_graph)

    bot.send_photo(cid, open('modo.png', 'rb'))

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