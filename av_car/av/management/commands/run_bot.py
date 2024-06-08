import asyncio
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from telebot import util

from av_project.av_backend.av_car.main_bot import bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Запуск бота"

    def handle(self, *args, **options):
        try:
            # asyncio.run(bot.infinity_polling(logger_level=settings.LOG_LEVEL, allowed_updates=util.update_types))
            bot.infinity_polling()
        except Exception as err:
            logger.error(f'Ошибка: {err}')
