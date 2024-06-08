import logging
import telebot
from django.conf import settings
from telebot import types

from av_project.av_backend.av_car.db_tg import *
from django.core.exceptions import ObjectDoesNotExist

bot = telebot.TeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


@bot.chat_member_handler()
def chat_member_handler_bot(message):  # функция, которая присылает кто подписался на канал
    status = message.difference.get('status')
    invite_link = message.invite_link
    full_name = message.from_user.full_name
    username = message.from_user.username
    id = message.from_user.id
    invite_link_name = ''
    invite_link_url = ''
    channel_title = message.chat.title
    channel_username = message.chat.username
    try:
        invite_link_name = getattr(invite_link, 'name')
        invite_link_url = getattr(invite_link, 'invite_link')
    except AttributeError as err:
        print(f'Не получил пригласительную ссылку: {err}')
        logger.info(f'Не получил пригласительную ссылку: {err}')
    current_subscriber_status = status[1]
    if current_subscriber_status == 'member':
        status_text = '🚀 Подписались'
    else:
        status_text = '😔 Отписались'
    text_message = (f'Статус: {status_text}\n'
                    f'Имя: <b>{full_name}</b>\n'
                    f'ID: <b>{id}</b>\n'
                    f'Канал: <b>{channel_title}</b>\n'
                    f'Ссылка канала: @{channel_username}')
    if username:
        text_message += f'\nНикнейм: @{username}'
    if invite_link_name:
        text_message += f'\nИмя ссылки: {invite_link_name}'
    if invite_link_url:
        text_message += f'\n<b>URL</b>: {invite_link_url}'
    bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN, text=text_message)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """🚗""",)
    bot.send_message(message.chat.id, """Добро пожаловать в Av Car\nВыберите команду в <b>Меню</b>""",)
    user_id = message.from_user.id
    username = f'@{message.from_user.username}'
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    return insert_tg(user_id, username, first_name, last_name)


@bot.message_handler(commands=['news'])
def news(message):
    try:
        links = get_all_links()
        if links:
            reply_markup = types.InlineKeyboardMarkup()
            for link in links:
                button = types.InlineKeyboardButton(text=link[0], url=link[1])
                reply_markup.add(button)
            bot.send_message(message.chat.id, "<b></b> 📰")
            bot.send_message(message.chat.id, "<b>Выберите Канал</b>", parse_mode='HTML', reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "Нет доступных каналов новостей.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")
        bot.reply_to(message, f"Произошла ошибка перезапустите бота /start")


@bot.message_handler(commands=['ask'])
def ask_command(message):
    bot.send_message(message.chat.id, "Вы можете Задать вопрос ❓\nИ менеджер Вам ответит как можно быстрее!")
    bot.register_next_step_handler(message, ask_message)


def ask_message(message):
    text = message.text
    chat_id = message.chat.id
    try:
        res = get_answer(chat=chat_id, message=text)
        existing_message = old_ask(chat=chat_id, message=text)
        new = new_ask(chat=chat_id, message=text)
        if existing_message:
            bot.send_message(chat_id, "Этот вопрос уже был задан. Ждите ответа менеджера.")
        elif res:
            bot.send_message(chat_id, f'На Ваш вопрос (<b>{text}</b>) ответ получен.')
            bot.send_message(chat_id, res)
        elif new:
            bot.send_message(chat_id, "Я ваш вопрос передал менеджеру\nОн ответит Вам в ближайшее время.")
    except Exception as err:
        bot.send_message(chat_id, f"Ваш вопрос не получен, возникла ошибка")


@bot.message_handler(commands=['site'])
def site(message):
    reply_markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Открыть Сайт', url='https://av.by/')
    reply_markup.add(button)
    bot.send_message(message.from_user.id, "<b></b> 📰", parse_mode='HTML', reply_markup=reply_markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name}\nВы можете обратиться в тех.поддержку по номеру:\n+375(29)111-11-11')
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)  # Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Также можете поделиться номером телефона 📱\nи менеджер Вам перезвонит 📲', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        get_contact(message)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Упс ошибка 😔')
