""" Simple notify-by-schedule telegram bot

- coding: utf-8 -

Author: shchuko
Email: yaroshchuk2000@gmail.com
Website: github.com/shchuko

"""

import time
import schedule
import datetime
import random
import os
from datetime import timedelta

import telebot
from telebot import apihelper

import botmessages as bmsg

print('Hello, I\'m alive')

token = os.environ['TOKEN']
chat_id = os.environ['CHAT_ID']
print('Env vars reading successful')

bot = telebot.TeleBot(token)

fixed_date = datetime.datetime(2019, 4, 10)
room_list = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010', '1011',
             '1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', '1021', '1022', '1023']


def clean_reminder():
    message = bmsg.clean_headers[random.randint(0, len(bmsg.clean_headers) - 1)]
    
    day_date = datetime.datetime.today()
    for i in range(7):
        room_first = room_list[(day_date - fixed_date).days % 11]
        room_second = room_list[(day_date - fixed_date).days % 12 + 12]
        message += bmsg.clean_body.format(day_date.strftime("%A"), room_first, room_second)
        day_date += timedelta(days=1)
    
    message += bmsg.clean_hashtag
    
    message_info = bot.send_message(chat_id, message)
    bot.pin_chat_message(chat_id, message_info.message_id)


def debug_message():
    message = 'Debug message\n'
    for hdr in bmsg.clean_headers:
        message += hdr
    
    for i in range(13):
        room_first = room_list[i % 11]
        room_second = room_list[i % 12 + 11]
        message += bmsg.clean_body.format('Weekday', room_first, room_second)
    
    message += bmsg.clean_hashtag
    message_info = bot.send_message(chat_id, message)

def send_start_msg():
    bot.send_message(chat_id, bmsg.start)
    #debug_message()
    clean_reminder()


schedule.every().monday.at('13:00').do(clean_reminder)

if __name__ == '__main__':
    send_start_msg()

    while True:
        schedule.run_pending()
        time.sleep(1)
    
