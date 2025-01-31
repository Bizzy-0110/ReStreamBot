# Code made by Bizzy-0110 on GitHub

import os
import random
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

REDACTED_DATA = 'secret.json' # Path to the file containing the bot token and the white list

with open(REDACTED_DATA, 'r') as file:
    redacted = json.load(file)


WHITE_LIST = redacted["WHITE_LIST"]# List of users id's that can use the bot

TG_API_TOKEN = redacted['TELEGRAM_TOKEN'] # token for the telegram bot
TOKEN_LENGTH = 20 # Increase this value for better security
TOKEN_FILE_PATH = './prev_key.txt' # Path to the file where the token is stored
NGINX_CONF_PATH = '/usr/local/nginx/conf/nginx.conf' # Path to the nginx configuration file

#-------------------------------------------------------------------------------


def gen_new_token():

    characters= 'ABCDEFGHIKLMNOPQRSTUVXYZabcdefghiklmnopqrstuvxyz1234567890'
    lenght = TOKEN_LENGTH
    gen_token = ""

    for k in range(lenght):
        gen_token+= random.choice(characters)

    return gen_token

def get_last_token():

    old_token = open(TOKEN_FILE_PATH, 'r').read()
    return old_token

def replace_token(old, new):

    #Update the token file
    txt = open(TOKEN_FILE_PATH, 'w')
    txt.write(new)

    #Update the nginx conf file
    t1 = open(NGINX_CONF_PATH, 'r')
    text = t1.read()
    t1.close()
    out = text.replace(str(old), str(new))

    t2 = open(NGINX_CONF_PATH, 'w')
    t2.write(out)


#---------------------------------------------------------------------------------------------------------

def _reload_ngnix():
    os.system('sudo /usr/local/nginx/sbin/nginx -s reload')
    print("Nginx restarted")

def refresh_stream():
    
    replace_token(get_last_token(), gen_new_token())
    _reload_ngnix()

    print("Stream stopped")


# ----------------------- Telegram Bot ------------------------

help_text = (
"Welcome to the Restream Bot!\n\n"
"Commands:"
"/stop = stop the stream and change the token"
"/start = generate a new token and start the nginx service"
"/reload = reload the nginx service"
"/get_token = get the current token"
"/help = get help for the commands"
)

def is_authorized(user_id: int) -> bool:
    return user_id in WHITE_LIST

async def start(update: Update, context: CallbackContext) -> None:
    if not is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    await update.message.reply_text(f'The service has started, this is the token: ```{get_last_token()}```', parse_mode='MarkdownV2')


async def stop(update: Update, context: CallbackContext) -> None:
    if not is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    
    refresh_stream()
    
    await update.message.reply_text('Stream fermato e token rinnovato.')

async def reload(update: Update, context: CallbackContext) -> None:
    if not is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    _reload_ngnix()
    await update.message.reply_text('Nginx ricaricato.')

async def get_token(update: Update, context: CallbackContext) -> None:
    if not is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    
    await update.message.reply_text(f'Current token: ```{get_last_token()}```', parse_mode='MarkdownV2')

async def help_command(update: Update, context: CallbackContext) -> None:
    if not is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    
    await update.message.reply_text(help_text)

def main():

    # create the application
    application = Application.builder().token(TG_API_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("reload", reload))
    application.add_handler(CommandHandler("get_token", get_token))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()

if __name__ == '__main__':
    main()
