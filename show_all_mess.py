# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


from config import token
from telebot import TeleBot
from datetime import datetime


bot = TeleBot(token)

print('\n' + str(bot.get_me()))


def log_me(message):
    if message.chat.username != None:
        (message.chat.username == 'https://t.me/' +
            str(message.chat.username))
    else:
        message.chat.username = '#'
    print(('\n{4} | {0} {1} ({2}):\n{3}'
           ).format(message.chat.first_name,
                    message.chat.last_name,
                    str(message.chat.id),
                    message.text,
                    str(datetime.now())[:-7]))


def call_back_log_me(call_back):
    if call_back.message.chat.username != None:
        (call_back.message.chat.username == 'https://t.me/' +
            str(call_back.message.chat.username))
    else:
        call_back.message.chat.username = '#'
    print(('\n{4} | {0} {1} ({2}):\n{3}'
           ).format(call_back.message.chat.first_name,
                    call_back.message.chat.last_name,
                    str(call_back.message.chat.id),
                    call_back.data,
                    str(datetime.now())[:-7]))


def inline_log_me(query):
    if query.from_user.username != None:
        (query.from_user.username == 'https://t.me/' +
            str(query.from_user.username))
    else:
        query.from_user.username = '#'
    print(('\n{4} | {0} {1} ({2}):\n{3}'
           ).format(query.from_user.first_name,
                    query.from_user.last_name,
                    str(query.from_user.id),
                    query.query,
                    str(datetime.now())[:-7]))


@bot.message_handler(content_types=["text"])
def message_text_handler(message):
    log_me(message)


@bot.callback_query_handler(func=lambda call_back: call_back.data)
def callback_query_text_handler(call_back):
    call_back_log_me(call_back)


@bot.inline_handler(func=lambda query: query.query)
def inline_text_handler(query):
    inline_log_me(query)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
