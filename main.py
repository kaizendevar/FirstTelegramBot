import logging
import requests
import re

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def hola(update, context):
    """Send a message when the command /hola is issued."""
    user = update.message.from_user
    update.message.reply_text('Hola! ' + user.first_name + ' :). Tu apellido es: ' + user.last_name + ', ¿cuál es tu descendencia? ')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text('Me gusta que me hayas escrito: ' + update.message.text)    

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def imagen(update, context):
        url = get_url()    
        context.bot.send_photo(chat_id=update.message.chat_id, photo=url)         

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('El "%s" caused error "%s"', bot, update.error)    

def main():
    token = config.get('GLOBAL','TokenTelegramBot')
    updater = Updater(token=token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('hola',   hola))
    dp.add_handler(CommandHandler('imagen', imagen))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)    

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()