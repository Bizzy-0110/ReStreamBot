# Code made by Bizzy-0110 on GitHub

import asyncio
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
NGINX_RELOAD_COMMAND = 'sudo /usr/local/nginx/sbin/nginx -s reload' # Command for restarting the nginx service

#-------------------------------------------------------------------------------


def _gen_new_token(): # Generate a new token key

    characters= 'ABCDEFGHIKLMNOPQRSTUVXYZabcdefghiklmnopqrstuvxyz1234567890'
    lenght = TOKEN_LENGTH
    gen_token = ""

    for k in range(lenght):
        gen_token+= random.choice(characters)

    return gen_token

def _get_last_token(): # Get the last token key

    old_token = open(TOKEN_FILE_PATH, 'r').read()
    return old_token

def _replace_token(old, new): # Replace the old token with the new one in the nginx configuration file

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


def _reload_ngnix():
    os.system(NGINX_RELOAD_COMMAND)
    print("Nginx restarted")

def _change_key(): # change the token key
    _replace_token(_get_last_token(), _gen_new_token())

# ----------------------- Telegram Bot ------------------------

help_text = (
"Welcome to the Restream Bot!\n\n"
"Commands:\n"
"/stop = stop the stream and change the token\n"
"/start = generate a new token and start the nginx service\n"
"/restart = reload the nginx service\n"
"/get_token = get the current token\n"
"/help = get help for the commands\n"
)

def _is_authorized(user_id: int) -> bool:
    return user_id in WHITE_LIST

async def start(update: Update, context: CallbackContext) -> None:
    if not _is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    
    _change_key()
    await update.message.reply_text(f'The service has started, this is the token: ```{_get_last_token()}```', parse_mode='MarkdownV2')


async def stop(update: Update, context: CallbackContext) -> None:
    if not _is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    
    _change_key()
    
    await update.message.reply_text('Stream stopped and token changed. Use /start to start the stream again.')

async def restart(update: Update, context: CallbackContext) -> None:
    if not _is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    _reload_ngnix()
    await update.message.reply_text('Nginx restarted.')

async def get_token(update: Update, context: CallbackContext) -> None:
    if not _is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    
    await update.message.reply_text(f'Current token: ```{_get_last_token()}```', parse_mode='MarkdownV2')

async def help_command(update: Update, context: CallbackContext) -> None:
    if not _is_authorized(update.message.from_user.id):
        await update.message.reply_text('Access denied')
        return
    
    await update.message.reply_text(help_text)

def main():

    # create the application
    application = Application.builder().token(TG_API_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("get_token", get_token))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()

if __name__ == '__main__':
    main()