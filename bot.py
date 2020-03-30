import config

import telebot

import requests

bot = telebot.TeleBot(config.token)

def summary():
    message = "Diagnosticados: {}\nActivos: {}\nRecuperados: {}\nEvacuados: {}\nFallecidos: {}\nIngresados {}\nActualizado: {}"

    data = requests.get(config.api_url + '/summary').json()

    return message.format(
        data['Diagnosticados'],
        data['Activos'],
        data['Recuperados'],
        data['Evacuados'],
        data['Muertes'],
        data['Ingresados']
        data['Updated'],
    )

    

@bot.message_handler(commands=['start', 'summary'])
def send_summary(message):
    cid = message.chat.id

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

@bot.message_handler(commands=['casos_extranjeros'])
def send_casos_extranjeros(message):
    cid = message.chat.id

    casos_extranjeros_graph = requests.get(config.api_url + '/casos_extranjeros').content

    with open('casos_extranjeros.png', 'wb') as f:
        f.write(casos_extranjeros_graph)

    bot.send_photo(cid, open('casos_extranjeros.png', 'rb'))

@bot.message_handler(commands=['nacionalidad'])
def send_nacionalidad(message):
    cid = message.chat.id

    nacionalidad_graph = requests.get(config.api_url + '/nacionalidad').content
    data = requests.get(config.api_url + '/nacionalidad_text').json()

    with open('nacionalidad.png', 'wb') as f:
        f.write(nacionalidad_graph)

    texto = 'Cubanos: {} | Extranjeros {}'.format(data['Cubanos'], data['Extranjeros'])

    bot.send_photo(cid, open('nacionalidad.png', 'rb'), texto)

@bot.message_handler(commands=['edad'])
def send_edad(message):
    cid = message.chat.id

    edad_graph = requests.get(config.api_url + '/edad').content

    with open('edad.png', 'wb') as f:
        f.write(edad_graph)

    bot.send_photo(cid, open('edad.png', 'rb'))

@bot.message_handler(commands=['test'])
def send_test(message):
    cid = message.chat.id

    test_graph = requests.get(config.api_url + '/test').content

    with open('test.png', 'wb') as f:
        f.write(test_graph)

    bot.send_photo(cid, open('test.png', 'rb'))

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