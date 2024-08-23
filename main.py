import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import json

logging.basicConfig(level=logging.INFO)

TOKEN = '7402656149:AAFJqM2fk--mxFZ7rkR2vLSYeHCfS4VbKKc'

# Инициализация базы данных
try:
    with open('database.json', 'r') as f:
        database = json.load(f)
except FileNotFoundError:
    database = {}

def start(update, context):
    user_id = update.effective_user.id
    if user_id not in database:
        database[user_id] = {'height': 0, 'last_increase': datetime.datetime.now() - datetime.timedelta(days=1)}
        with open('database.json', 'w') as f:
            json.dump(database, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Привет! Ты можешь увеличить свой рост раз в 24 часа.')

def height(update, context):
    user_id = update.effective_user.id
    if user_id not in database:
        database[user_id] = {'height': 0, 'last_increase': datetime.datetime.now() - datetime.timedelta(days=1)}
        with open('database.json', 'w') as f:
            json.dump(database, f)
    last_increase = database[user_id]['last_increase']
    if (datetime.datetime.now() - last_increase).days >= 1:
        database[user_id]['height'] += 1
        database[user_id]['last_increase'] = datetime.datetime.now()
        with open('database.json', 'w') as f:
            json.dump(database, f)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Твой рост теперь {database[user_id]["height"]} см!')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ты можешь увеличить свой рост только раз в 24 часа.')

def me(update, context):
    user_id = update.effective_user.id
    if user_id not in database:
        database[user_id] = {'height': 0, 'last_increase': datetime.datetime.now() - datetime.timedelta(days=1)}
        with open('database.json', 'w') as f:
            json.dump(database, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Твой рост {database[user_id]["height"]} см!')

def top(update, context):
    sorted_database = sorted(database.items(), key=lambda x: x[1]['height'], reverse=True)
    top_users = ''
    for i, (user_id, user_data) in enumerate(sorted_database):
        top_users += f'{i+1}. {user_data["height"]} см\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=top_users)

def remove(update, context):
    user_id = update.effective_user.id
    if user_id not in database:
        database[user_id] = {'height': 0, 'last_increase': datetime.datetime.now() - datetime.timedelta(days=1)}
        with open('database.json', 'w') as f:
            json.dump(database, f)
    if database[user_id]['height'] == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text='У тебя уже 0 см!')
    else:
        database[user_id]['height'] = 0
        with open('database.json', 'w') as f:
            json.dump(database, f)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Твой рост теперь 0 см!')

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('рост', height))
    dp.add_handler(CommandHandler('я', me))
    dp.add_handler(CommandHandler('топ', top))
    dp.add_handler(CommandHandler('убрать', remove))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
