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
import threading
from datetime import timedelta

import telebot
from telebot import apihelper

import botmessages as bmsg

print('I\'m alive!')
token = os.environ['TOKEN']
chat_id = os.environ['CHAT_ID']
print('Env vars reading successful')

fixed_date = datetime.datetime(2019, 4, 10)
bot = telebot.TeleBot(token)

class CleaningReminder:
    def __init__(self, token, chat_id, start_date):
        self.bot = telebot.TeleBot(token)
        
        self.chat_id = chat_id
        self.start_date = start_date

        self.room_list_1 = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010', '1011']
        self.room_list_2 = ['1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', '1021', '1022', '1023']
    
        self.pinned_message_id = None

    def add_remind_time(self, remind_time):
        schedule.every().monday.at(remind_time).do(self.__clean_reminder)

    def polling(self):
        thread = threading.Thread(target=self.__polling_loop)
        thread.start()

    def __clean_reminder(self):
        message = bmsg.clean_headers[random.randint(0, len(bmsg.clean_headers) - 1)]
        
        day_date = datetime.datetime.today()
        for i in range(7):
            room_first = self.room_list_1[(day_date - self.start_date).days % len(self.room_list_1)]
            room_second = self.room_list_2[(day_date - self.start_date).days % len(self.room_list_2)]
            message += bmsg.clean_body.format(day_date.strftime("%A"), room_first, room_second)
            day_date += timedelta(days=1)
        
        message += bmsg.clean_hashtag
        
        message_info = self.bot.send_message(chat_id, message)
        
        if self.pinned_message_id is not None:
            self.bot.unpin_chat_message(chat_id, self.pinned_message_id)

        self.bot.pin_chat_message(chat_id, message_info.message_id)
        self.pinned_message_id = message_info.message_id


    def __polling_loop(self): 
        while True:
            schedule.run_pending()
            time.sleep(1)
    

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, bmsg.start + bmsg.hlp)    


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, bmsg.hlp)


@bot.message_handler(commands=['links'])
def handle_links(message):
    bot.reply_to(message, bmsg.links)


@bot.message_handler(commands=['faq_ru'])
def handle_faq_ru(message):
    bot.reply_to(message, bmsg.faq_ru)


@bot.message_handler(commands=['faq_en'])
def handle_faq_en(message):
    bot.reply_to(message, bmsg.faq_en)


@bot.message_handler(content_types=["new_chat_members"])
def handle_joinchat(message):
    bot.reply_to(message, bmsg.hlp)


if __name__ == '__main__':
    reminder = CleaningReminder(token, chat_id, fixed_date)
    reminder.add_remind_time('13:00')
    reminder.polling()

    bot.polling()

