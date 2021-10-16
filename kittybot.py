# kittybot/kittybot.py
import os
import sys
import requests
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import logging

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
URL_cat = 'https://api.thecatapi.com/v1/images/search'
URL_dog = 'https://api.thedogapi.com/v1/images/search'
bot = Bot(token=TELEGRAM_TOKEN)
# text = 'Вам телеграмма!'
# bot.send_message(chat_id, text)
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

def get_new_image(animal):
    if animal == 'cat':
        try:
            response = requests.get(URL_cat)
        except Exception as error:
            logging.error(f'Ошибка при запросе к основному API: {error}')

    elif animal == 'dog':
        try:
            response = requests.get(URL_dog)
        except Exception as error:
            logging.error(f'Ошибка при запросе к основному API: {error}')


    response = response.json()
    random_animal = response[0].get('url')
    return random_animal


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image('cat'))

def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image('dog'))


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([
                ['/new_cat'],
                ['/new_dog'],
            ], resize_keyboard=True)

    context.bot.send_message(chat_id=chat.id,
                             text=f'Привет, {name}! Держи фото!',
                             reply_markup=button)
    context.bot.send_photo(chat.id, get_new_image('cat'))


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('new_cat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('new_dog', new_dog))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling(poll_interval=10.0)
    updater.idle()


if __name__ == '__main__':
    main()
