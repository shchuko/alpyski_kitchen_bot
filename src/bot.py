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
from datetime import date
from calendar import monthrange

import telebot
from telebot.apihelper import ApiTelegramException

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
        self.room_list_2 = ['1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', '1021', '1022',
                            '1023']

    def add_remind_time(self, remind_time, remind_day_of_month):
        # 21:01 UTC == 00:01 Moscow
        schedule.every().day.at('21:01').do(
            lambda: self.bot.send_message(chat_id, "Happy New Year!") if date.today().day == 1 else lambda: None)

        schedule.every().day.at(remind_time).do(
            lambda: self.__clean_reminder() if date.today().day == remind_day_of_month else lambda: None)

    def polling(self):
        thread = threading.Thread(target=self.__polling_loop)
        thread.start()

    def __clean_reminder(self):
        message = bmsg.clean_headers[random.randint(0, len(bmsg.clean_headers) - 1)] + '\n'

        day_date = datetime.datetime.today()
        days_in_month = monthrange(day_date.year, day_date.month)[1]
        for i in range(days_in_month):
            room_first = self.room_list_1[(day_date - self.start_date).days % len(self.room_list_1)]
            room_second = self.room_list_2[(day_date - self.start_date).days % len(self.room_list_2)]
            message += bmsg.clean_body.format(day_date.strftime("%d.%m"), room_first, room_second)
            day_date += timedelta(days=1)

        message += bmsg.clean_hashtag

        message_info = self.bot.send_message(chat_id, message)

        try:
            self.bot.unpin_all_chat_messages(chat_id)
        except ApiTelegramException:
            pass  # Sometimes telegram responses with 429 for some reason

        self.bot.pin_chat_message(chat_id, message_info.message_id)

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


@bot.message_handler(commands=['chat_id'])
def handle_chat_id(message):
    bot.reply_to(message, f"Current chat id: {message.chat.id}")


@bot.message_handler(commands=['who_clean'])
def handle_who_clean(message):
    day_date = datetime.datetime.today()
    room_list_1 = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010', '1011']
    room_list_2 = ['1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', '1021', '1022', '1023']
    room_first = room_list_1[(day_date - fixed_date).days % len(room_list_1)]
    room_second = room_list_2[(day_date - fixed_date).days % len(room_list_2)]
    bot.reply_to(message, bmsg.clean_body.format(day_date.strftime("%d/%m/%Y"), room_first, room_second))


@bot.message_handler(content_types=["new_chat_members"])
def handle_joinchat(message):
    bot.reply_to(message, bmsg.hlp)


if __name__ == '__main__':
    reminder = CleaningReminder(token, chat_id, fixed_date)
    reminder.add_remind_time('13:00', 1)
    reminder.polling()

    bot.polling()
