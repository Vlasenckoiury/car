## -*- coding: utf-8 -*-
import logging
import os
from environs import Env


import psycopg2
from functools import wraps

env = Env()
env.read_env()


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
        )
        cursor = conn.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            conn.commit()
            return result
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
    return wrapper


@db_connection
def insert_tg(cursor, user_id, username, first_name, last_name):
    # SQL-запрос для вставки данных
    insert_query = """
    INSERT INTO av_car_botuser (telegram_id, username, first_name, last_name) VALUES (%s, %s, %s, %s)
    """
    # Выполнение запроса
    cursor.execute(insert_query, (user_id, username, first_name, last_name))
    print("Данные успешно сохранены в базе данных")


@db_connection
def get_all_links(cursor):
    select_query = f"SELECT name, chat_link FROM av_car_telegramchat"
    cursor.execute(select_query)
    column = cursor.fetchall()
    return column


@db_connection
def get_contact(cursor, message):
    update_query = f"""UPDATE av_car_botuser SET contact = %s WHERE telegram_id = {message.chat.id}"""
    # Выполнение запроса
    cursor.execute(update_query, (message.contact.phone_number, ))
    print(f"Значение в колонке {message.contact.phone_number} пользователя с telegram_id {message.chat.id} успешно обновлено в базе данных")


@db_connection
def get_time(cursor):
    # cursor.execute("SELECT start_time FROM av_car_newmessage WHERE created_at >= NOW() - INTERVAL '1 day'")
    cursor.execute("SELECT start_time, end_time FROM av_car_newmessage")
    new_records = cursor.fetchall()
    return new_records


@db_connection
def get_channel(cursor):
    try:
        cursor.execute("""
        SELECT av_car_telegramchat.chat_link, av_car_newmessage.message
        FROM av_car_newmessage
        INNER JOIN av_car_telegramchat ON av_car_newmessage.link_chat_id = av_car_telegramchat.id;
        """)
        rows = cursor.fetchall()
        return rows
    except Exception as err:
        logging.info(f'Данные не получены {err}')


@db_connection
def get_week_day(cursor):
    try:
        cursor.execute("SELECT day_monday, " 
                       "day_tuesday, "
                       "day_wednesday, "
                       "day_thursday, "
                       "day_friday, "
                       "day_saturday, "
                       "day_sunday "
                       "FROM av_car_newmessage")
        week = cursor.fetchall()
        return week
    except Exception as err:
        logging.info(f'Данные не получены {err}')


@db_connection
def old_ask(cursor, chat, message):
    try:
        cursor.execute("SELECT * FROM av_car_askmessage WHERE chat_id = %s AND question = %s AND answer = null", (chat, message))
        row = cursor.fetchall()
        return row
    except Exception as err:
        logging.info(f'ID чата и текст не получены {err}')


@db_connection
def get_answer(cursor, chat, message):
    try:
        cursor.execute("SELECT answer FROM av_car_askmessage WHERE chat_id = %s AND question = %s AND answer IS NOT NULL AND answer != ''", (chat, message))
        results = cursor.fetchall()
        for ans in results:
            return ans[0]
    except Exception as err:
        logging.info(f'{err}')


@db_connection
def new_ask(cursor, chat, message):
    try:
        cursor.execute("INSERT INTO av_car_askmessage (chat_id, question) VALUES (%s, %s);", (chat, message))
        logging.info(f'Вопрос отправлен')
        return True
    except Exception as err:
        logging.info(f'Вопрос не отправлен {err}')
