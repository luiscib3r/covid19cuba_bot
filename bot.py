import config

import telebot

import requests

bot = telebot.TeleBot(config.token)

def summary():
    message = '''
        Diagnosticados: {}
        Activos: {}
        Recuperados: {}
        Evacuados: {}
        Muertes: {}
        Actualizado: {}
    '''

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
def send_welcome(message):
    bot.reply_to(
        message,
        summary()
    )

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