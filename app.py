#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging
from lxml import html
import requests
import re
from queue import Queue
from threading import Thread

TOKEN=os.environ.get('TOKEN')
def Query():
	page = requests.get("http://www.loteriadehoy.com/animalitos/")
	tree = html.fromstring(page.content)
	# fecha=tree.xpath('//input[@id="fecha"]/text()"')
	titles=tree.xpath('//div[@class="doughnut-chart"]/span[contains(@class,"chart-title")]/text()') #17 titulos en el primer lotto
	scope=["Delfin","Ballena","Carnero","Toro","Ciempies","Alacran","Leon","Rana","Perico","Raton","Aguila","Tigre","Gato","Caballo","Mono","Paloma","Zorro","Oso","Pavo","Burro","Chivo","Cochino","Gallo","Iguana","Camello","Zebra","Gallina","Vaca","Perro","Zamuro","Elefante","Caiman","Lapa","Ardilla","Pescado","Venado","Jirafa","Culebra","Por Salir"]
	animales=[(titulo,re.findall(r'(\d+:\d\d)',titles[index+1])[0]) for index,titulo in enumerate(titles) if titulo.strip(" ") in scope]
	results={titles[0]:[animal for index,animal in enumerate(animales,1) if index<=8],titles[17]:[b for a,b in enumerate(animales,1) if a>8]}
	print("Estos son los resultados del día: ")
	print("----Animales----")
	print(results)
	return results

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    data=Query()
except:
    date=None;
def start(bot, update):
    keyboard = [[InlineKeyboardButton("Lotto Activo", callback_data='1'),
                 InlineKeyboardButton("La Granjita", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Por favor elija su opción:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    if data==None:
    	response="Disculpe pero el servicio de resultados no se encuentra disponible en estos momentos , intente de nuevo."
    	bot.edit_message_text(text=response,
	                          chat_id=query.message.chat_id,
	                          message_id=query.message.message_id)
    if query.data=='1':
    	response="".join(['\n {value} Hora: {time} '.format(value=a,time=b) for a,b in data[' Lotto Activo ']]) 
    	bot.edit_message_text(text=response,
	                          chat_id=query.message.chat_id,
	                          message_id=query.message.message_id)
    if query.data=='2':
    	response="".join(['\n {value} Hora: {time} '.format(value=a,time=b) for a,b in data[' La Granjita ']]) 
    	bot.edit_message_text(text=response,
	                          chat_id=query.message.chat_id,
	                          message_id=query.message.message_id)

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    webhook_url="https://calm-forest-84206.herokuapp.com/"
    PORT = int(os.environ.get('PORT'))
    updater = Updater(TOKEN)
    bot = updater.bot
    dp = updater.dispatcher
    # add handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
    updater.bot.set_webhook(webhook_url + TOKEN)
    updater.idle()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
