# import logging
import pytz
import schedule
import telebot
from django.conf import settings

from av_project.av_backend.av_car.db_tg import *
from datetime import datetime
from datetime import time


bot_channel = telebot.TeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


def send_message():
    channel = get_channel()
    if channel:
        for result in channel:
            bot_channel.send_message(chat_id=result[0], text=result[1])  # ошибка передать канал с @news_av_car
    else:
        logger.info(f'Сообщение не отправлено в канал')


def scheduled_message():
    week_day = get_week_day()
    key_week = {0: week_day[0][0],
                1: week_day[0][1],
                2: week_day[0][2],
                3: week_day[0][3],
                4: week_day[0][4],
                5: week_day[0][5],
                6: week_day[0][6]}
    today_weekday = datetime.now().weekday()
    if today_weekday in key_week and key_week[today_weekday] == True:
        new_records = get_time()
        if new_records:
            now = datetime.now(pytz.timezone('Europe/Moscow'))
            current_time = now.time()
            start_time = new_records[0][0]
            end_time = new_records[0][1]
            if start_time < end_time and start_time <= current_time <= end_time:
                logger.info("Текущее время заданно в диапазоне заданному времени")
                send_message()
            elif start_time > end_time and (start_time >= current_time <= end_time or
                   start_time <= current_time >= end_time):
                send_message()
            else:
                logger.info("Текущее время заданно вне диапазоне заданному времени ")
    else:
        if any(key_week) == False:
            logger.info('Если не выбран ни один день, то будет отправлять во все дни')
        else:
            logger.info(f'Ошибка с днями неделями')


schedule.every(5).seconds.do(scheduled_message)

while True:
    schedule.run_pending()
