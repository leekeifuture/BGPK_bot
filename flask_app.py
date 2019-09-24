# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import re
import cherrypy
import telebot as tb
from os import uname
import config as conf
from json import dumps
from time import sleep
from logging import INFO
import functions as func
from sys import exc_info
import constants as const
from sqlite3 import connect
from datetime import datetime
import registration_functions as reg_func


class WebhookServer(object):
    '''
    Check incoming message
    '''
    @cherrypy.expose
    def index(self):
        if ('content-length' in cherrypy.request.headers and
                'content-type' in cherrypy.request.headers and
                cherrypy.request.headers['content-type'] == 'application/json'):
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode('utf-8')
            update = tb.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


bot = tb.TeleBot(conf.token)  # skip_pending=False
bot_username = bot.get_me().username

logger = tb.logger
tb.logger.setLevel(INFO)

main_keyboard_btn = tb.types.ReplyKeyboardMarkup(True)
main_keyboard_btn.row(const.emoji['anticlockwise'] + ' Замены')
main_keyboard_btn.row(const.emoji['info'], const.emoji['star'],
                  const.emoji['settings'],
                  const.emoji['alarm_clock'], const.emoji['bell'])

main_keyboard_m50 = tb.types.ReplyKeyboardMarkup(True)
main_keyboard_m50.row(const.emoji['page_facing_up'] + ' Расписание',
                      const.emoji['anticlockwise'] + ' Замены')
main_keyboard_m50.row(const.emoji['info'], const.emoji['star'],
                      const.emoji['settings'],
                      const.emoji['alarm_clock'], const.emoji['bell'])


def main_keyboard(chat_id):
    if (chat_id in const.m50ids and
            func.get_student_group(chat_id).lower()) == 'м50':
        return main_keyboard_m50
    return main_keyboard_btn


schedule_keyboard = tb.types.ReplyKeyboardMarkup(True)
schedule_keyboard.row('Сегодня', 'Завтра', 'Неделя')
schedule_keyboard.row(const.emoji['back'])

replacements_keyboard = tb.types.ReplyKeyboardMarkup(True)
replacements_keyboard.row('Сегoдня', 'Зaвтрa', 'Нeделя')
replacements_keyboard.row(const.emoji['back'], const.emoji['magnifying_glass'])


'''
@bot.message_handler(content_types=['text'])
def handle_text(message):
    print(message.text)


@bot.callback_query_handler(func=lambda call_back: call_back.data)
def callback_query_test(call_back):
    print(call_back.data)
'''


@bot.message_handler(func=lambda mess: func.is_user_banned(mess.chat.id),
                     content_types=['text'])
def banned_user_handler(message):

    remove_keyboard = tb.types.ReplyKeyboardRemove()
    answer = const.emoji['no_entry'] + (' Вы заблокированы по причине '
                                        'неоднократного спама! Если считаете что не виновны и хотите вновь '
                                        'начать пользоваться сервисом — сообщите об этом '
                                        '<a href="https://t.me/lee_kei">разработчику</a>.')
    bot.send_message(message.chat.id, answer, True,
                     reply_markup=remove_keyboard,
                     parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(commands=['start'])
def start_handler(message, back=False):
    answer = ''
    if message.text == '/start' and not func.is_user_exist(message.chat.id):
        answer = 'Приветствую!\n'
    answer += 'Загружаю данные из базы\U00002026'
    if back:
        bot_msg = bot.edit_message_text(text=answer, chat_id=message.chat.id,
                                        message_id=message.message_id)
    else:
        bot_msg = bot.send_message(message.chat.id, answer)

    answer = 'Для начала выбери в качестве кого ты хочешь зайти:'
    types_keyboard = tb.types.ReplyKeyboardMarkup(True,
                                                  False,
                                                  row_width=1)
    [types_keyboard.row(type_name) for type_name in const.existing_types]
    types_keyboard.row('Поддержка', 'Завершить')
    data = dumps(const.types, ensure_ascii=False)

    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''DELETE FROM user_choice
                            WHERE user_id = ?''', (message.chat.id,))
    sql_con.commit()
    cursor.execute('''INSERT INTO user_choice (user_id, types_json)
                           VALUES (?, ?)''', (message.chat.id, data,))
    sql_con.commit()
    if func.is_user_in_all_users(message.chat.id) == False:
        cursor.execute('''INSERT INTO all_users (id)
                               VALUES (?)''', (message.chat.id,))
        sql_con.commit()
    cursor.close()
    sql_con.close()

    bot.edit_message_text(text='Готово!',
                          chat_id=message.chat.id,
                          message_id=bot_msg.message_id)

    bot.send_message(message.chat.id, answer,
                     reply_markup=types_keyboard)
    reg_func.set_next_step(message.chat.id, 'select_status')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Поддержка',
                     content_types=['text'])
def problem_text_handler(message):

    answer = ('Если ты нашёл баг, возникла проблема или появилась идея, то ты '
              'всегда можешь связаться с <a href="https://t.me/lee_kei">разработчиком</a>.\n'
              '/help - краткая информация о возможностях бота.')
    bot.send_message(message.chat.id, answer, True,
                     parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(commands=['exit'])
@bot.message_handler(func=lambda mess: mess.text == 'Завершить',
                     content_types=['text'])
def exit_handler(message):

    func.delete_user(message.chat.id, only_choice=False)
    remove_keyboard = tb.types.ReplyKeyboardRemove()
    answer = 'До встречи!\nДля регистрации используй /start'
    bot.send_message(message.chat.id, answer, reply_markup=remove_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess:
                     (reg_func.get_step(mess.chat.id) ==
                      'select_status' and
                      mess.text != '/home' and
                      'Назад' not in mess.text),
                     content_types=['text'])
def select_status_handler(message):

    reg_func.select_status(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess:
                     (reg_func.get_step(mess.chat.id) ==
                      'select_teacher' and
                      mess.text != '/home' and
                      'Назад' not in mess.text),
                     content_types=['text'])
def select_teacher_handler(message):

    reg_func.select_teacher(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess:
                     (reg_func.get_step(mess.chat.id) ==
                      'select_division' and
                      mess.text != '/home' and
                      'Назад' not in mess.text),
                     content_types=['text'])
def select_division_handler(message):

    reg_func.select_division(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess:
                     (reg_func.get_step(mess.chat.id) ==
                      'select_admission_year' and
                      mess.text != '/home' and
                      'Назад' not in mess.text),
                     content_types=['text'])
def select_admission_year_handler(message):

    reg_func.select_admission_year(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess:
                     (reg_func.get_step(mess.chat.id) ==
                      'select_student_group' and
                      mess.text != '/home' and
                      'Назад' not in mess.text),
                     content_types=['text'])
def select_student_group_handler(message):

    reg_func.select_student_group(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess:
                     (reg_func.get_step(mess.chat.id) ==
                      'confirm_choice' and
                      mess.text != '/home' and
                      'Назад' not in mess.text),
                     content_types=['text'])
def confirm_choice_handler(message):

    reg_func.confirm_choice(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess:
                     (reg_func.get_step(mess.chat.id) ==
                      'confirm_choice_teacher' and
                      mess.text != '/home' and
                      'Назад' not in mess.text),
                     content_types=['text'])
def confirm_choice_teacher_handler(message):

    reg_func.confirm_choice_teacher(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess:
                     reg_func.get_step(mess.chat.id) and
                     ('choice' in reg_func.get_step(mess.chat.id) or
                      'select' in reg_func.get_step(mess.chat.id)) and
                     not func.is_user_exist(mess.chat.id),
                     commands=['home'])
def home_registration_handler(message):
    start_handler(message)
    func.log_me(message)
    return


@bot.message_handler(func=lambda mess: not func.is_user_exist(mess.chat.id),
                     content_types=['text'])
def not_exist_user_handler(message):

    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    if func.is_user_in_all_users(message.chat.id) == False:
        cursor.execute('''INSERT INTO all_users (id)
                               VALUES (?)''', (message.chat.id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()

    remove_keyboard = tb.types.ReplyKeyboardRemove()
    answer = ('Чтобы начать пользоваться сервисом, необходимо '
              'зарегистрироваться.\nВоспользуйся коммандой /start')
    bot.send_message(message.chat.id,
                     answer,
                     reply_markup=remove_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Сменить группу ({0})'
                     .format(func.get_student_group(mess.chat.id)) or
                     mess.text == 'Перезайти',
                     content_types=['text'])
def change_group_handler(message):

    data = dumps(const.types, ensure_ascii=False)
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''DELETE FROM user_choice
                            WHERE user_id = ?''', (message.chat.id,))
    sql_con.commit()
    cursor.execute('''INSERT INTO user_choice (user_id, types_json)
                           VALUES (?, ?)''', (message.chat.id, data,))
    sql_con.commit()
    cursor.close()
    sql_con.close()

    if message.text == 'Перезайти':
        message.text = const.types[1]['Type']
        answer = 'Смена преподавателя\nДля отмены используй /home'
    else:
        answer = ('Смена группы <b>{0}</b>\nДля отмены используй /home'
                  .format(func.get_student_group(message.chat.id)))
        message.text = const.types[0]['Type']
    bot.send_message(message.chat.id, answer,
                     parse_mode='HTML')

    reg_func.select_status(message, True)
    func.log_me(message)


@bot.message_handler(commands=['help'])
@bot.message_handler(func=lambda mess: mess.text == const.emoji['info'],
                     content_types=['text'])
def help_handler(message):

    inline_full_info_keyboard = tb.types.InlineKeyboardMarkup()
    inline_full_info_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['Полное ИНФО']])
    answer = const.briefly_info_answer
    bot.send_message(message.chat.id, answer, True,
                     reply_markup=inline_full_info_keyboard,
                     parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(commands=['id'])
def id_handler(message):

    bot.send_message(message.chat.id, str(message.from_user.id))
    func.log_me(message)


@bot.message_handler(commands=['home'])
@bot.message_handler(func=lambda mess: mess.text == 'Назад' or
                     mess.text == '« Назад' or
                     mess.text == const.emoji['back'],
                     content_types=['text'])
def home_handler(message):

    func.delete_user(message.chat.id, only_choice=True)
    answer = 'Главное меню'
    bot.send_message(message.chat.id, answer,
                     reply_markup=main_keyboard(message.chat.id))
    func.log_me(message)


@bot.message_handler(commands=['settings'])
@bot.message_handler(func=lambda mess: mess.text == const.emoji['settings'],
                     content_types=['text'])
def settings_handler(message):

    alias = func.get_alias(message.chat.id)
    answer = 'Настройки'
    settings_keyboard = tb.types.ReplyKeyboardMarkup(True)

    func.delete_user(message.chat.id, only_choice=True)

    if alias == 'PREP':
        re_entrance = 'Перезайти'
    else:
        re_entrance = 'Сменить группу ({0})'.format(
            func.get_student_group(message.chat.id))

    settings_keyboard.row(re_entrance, 'Завершить')
    settings_keyboard.row('« Назад', 'Поддержка')

    if message.chat.id == int(conf.my_id):
        settings_keyboard.row('Управление')

    bot.send_message(message.chat.id, answer, reply_markup=settings_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == const.emoji['page_facing_up'] + ' Расписание' and (mess.chat.id in const.m50ids and func.get_student_group(mess.chat.id).lower() == 'м50'),
                     content_types=['text'])
def schedule_handler(message):

    answer = 'Меню расписания'
    bot.send_message(message.chat.id, answer, reply_markup=schedule_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == const.emoji['anticlockwise'] + ' Замены' or
                     mess.text == '« Назaд',
                     content_types=['text'])
def replacements_handler(message):

    answer = 'Меню замен'
    bot.send_message(message.chat.id, answer,
                     reply_markup=replacements_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Сегодня' and (mess.chat.id in const.m50ids and func.get_student_group(mess.chat.id).lower() == 'м50'))
def today_schedule_handler(message):

    answer = func.create_schedule_answer(message.chat.id)
    bot.send_message(message.chat.id, answer, parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Завтра' and (mess.chat.id in const.m50ids and func.get_student_group(mess.chat.id).lower() == 'м50'))
def tomorrow_schedule_handler(message):

    answer = func.create_schedule_answer(message.chat.id, True)
    bot.send_message(message.chat.id, answer, parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Сегoдня')
def today_replace_handler(message):

    func.replacements_today(message.chat.id)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Зaвтрa')
def tomorrow_replace_handler(message):

    func.replacements_tomorrow(message.chat.id)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Неделя' and (mess.chat.id in const.m50ids and func.get_student_group(mess.chat.id).lower() == 'м50'))
def calendar_handler(message):

    answer = 'Выбери день:'
    week_day_calendar = tb.types.InlineKeyboardMarkup()
    week_day_calendar.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in const.week_day_number.keys()])
    week_day_calendar.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['Вся неделя']])
    bot.send_message(message.chat.id, answer, reply_markup=week_day_calendar)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Нeделя')
def calendar_replace_handler(message):

    group = func.get_student_group(message.chat.id)
    if func.get_alias(message.chat.id) == 'PREP':
        index = const.cap_teachers.index(group)
        for_any = 'преподавателя'
        group = const.sht_teachers[index][:-1]
    else:
        for_any = 'группы'

    answer = ('Выбери день:\n' + const.emoji['check_mark'] + ' – Есть замены для ' + for_any + ' <b>{0}</b>.\n'.format(group)
              + const.emoji['negative_squared_cross_mark'] +
              ' – Нет замен для ' + for_any + ' <b>{0}</b>.\n'.format(group)
              + const.emoji['cross_mark'] +
              ' – Замены на ближайший день недели ещё не вывесили (будут показаны предыдущие замены).')
    week_day_calendar = tb.types.InlineKeyboardMarkup()
    active_days = func.get_active_replace_days(message.chat.id)
    y = []
    n = []
    cross = []
    for day in active_days:
        if const.emoji['check_mark'] in day:
            y.append(1)
        elif const.emoji['negative_squared_cross_mark'] in day:
            n.append(1)
        elif const.emoji['cross_mark'] in day:
            cross.append(1)
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [day]])
    if len(y) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['check_mark'] + ' Вся нeделя']])
    elif len(n) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['negative_squared_cross_mark'] + ' Вся нeделя']])
    elif len(cross) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['cross_mark'] + ' Вся нeделя']])
    else:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in ['Вся нeделя']])

    bot.send_message(message.chat.id, answer,
                     reply_markup=week_day_calendar, parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == const.emoji['alarm_clock'])
def sending_handler(message):

    answer = ('Выбери, на рассылку чего ты хочешь <b>подписаться</b> или <b>отписаться</b>:\n'
              + const.emoji['check_mark'] + ' – Рассылка включена.\n'
              + const.emoji['negative_squared_cross_mark'] + ' – Рассылка отключена.')
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT sending_rasp, sending_rasp_5, sending_zam, sending_without_repl
                        FROM user_data
                       WHERE id = ?''',
                   (message.chat.id,))
    data = cursor.fetchall()[0]
    cursor.close()
    sql_con.close()

    not_replace = False
    # if data[0] or data[1]:
    #     schedule = ('Расписания (%s)' %
    #                 const.emoji['check_mark'])
    # else:
    #     schedule = ('Расписания (%s)' %
    #                 const.emoji['negative_squared_cross_mark'])
    if data[2]:
        replace = ('Замен (%s)' %
                   const.emoji['check_mark'])
        if data[3]:
            not_replace = ('Отсутствие замен (%s)' %
                           const.emoji['check_mark'])
        else:
            not_replace = ('Отсутствие замен (%s)' %
                           const.emoji['negative_squared_cross_mark'])
    else:
        replace = ('Замен (%s)' %
                   const.emoji['negative_squared_cross_mark'])

    sending_keyboard = tb.types.InlineKeyboardMarkup(True)
    sending_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name,
                                        callback_data=name)
            for name in [replace]])
    if not_replace:
        sending_keyboard.row(tb.types.InlineKeyboardButton(
            text=not_replace, callback_data=not_replace))
    bot.send_message(message.chat.id, answer, parse_mode='HTML',
                     reply_markup=sending_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == const.emoji['star'])
def rate_handler(message):

    answer = 'Оцените качество сервиса:'
    user_rate = func.get_user_rate(message.chat.id)
    rate_keyboard = tb.types.InlineKeyboardMarkup(row_width=5)
    rate_keyboard.add(*[tb.types.InlineKeyboardButton(
        text=const.emoji[
            'star2'] if user_rate < count_of_stars else const.emoji['star'],
        callback_data=str(count_of_stars))
        for count_of_stars in (1, 2, 3, 4, 5)])
    rate_keyboard.add(
        *[tb.types.InlineKeyboardButton(text=name,
                                        callback_data=name)
            for name in ['Связь', 'Статистика']])
    bot.send_message(message.chat.id, answer, parse_mode='HTML',
                     reply_markup=rate_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == const.emoji['bell'])
def calls_handler(message):

    answer = 'Звонки'
    call_keyboard = tb.types.ReplyKeyboardMarkup(True)
    call_keyboard.row('Пн – пт', 'Суббота', 'В сокр. дни')
    call_keyboard.row('« Назад', 'Ближайший звонок')
    bot.send_message(message.chat.id, answer, reply_markup=call_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Пн – пт')
def calls_pnpt_handler(message):

    answer = const.calls_pnpt
    bot.send_message(message.chat.id, answer, True,
                     parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Суббота')
def calls_sb_handler(message):

    answer = const.calls_sb
    bot.send_message(message.chat.id, answer, True,
                     parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'В сокр. дни')
def calls_sokr_handler(message):

    answer = const.calls_sokr
    bot.send_message(message.chat.id, answer, True,
                     parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Ближайший звонок')
def bliz_zvonok_handler(message):

    blzv0 = func.blzv()[0]
    minorh = 'мин'
    run = const.emoji['blue_diamond']
    if blzv0 >= 60:
        blzv0 = func.blzv()[0] // 60
        minorh = 'ч {0} мин'.format(func.blzv()[0] % 60)
    elif blzv0 <= 2:
        run = const.emoji['runner']
    elif blzv0 <= 5:
        run = const.emoji['orange_diamond']
    answer = ('{0} <i>Через</i> {1} {2}\n'
              'Ближайший звонок в <b>{3}</b> ({4})'.format(run,
                                                           blzv0,
                                                           minorh,
                                                           func.blzv()[1],
                                                           func.blzv()[2]))
    bot.send_message(message.chat.id, answer, True, parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == const.emoji['magnifying_glass'] or
                     mess.text == '« Нaзад',
                     content_types=['text'])
def search_replacements_handler(message):

    answer = 'Выбери, по какому признаку хочешь найти замены:'
    search_replacements_keyboard = tb.types.ReplyKeyboardMarkup(True)
    search_replacements_keyboard.row('Группа', 'Направление')
    search_replacements_keyboard.row('Курс', 'Препoдаватель')
    search_replacements_keyboard.row('« Назaд')
    bot.send_message(message.chat.id, answer,
                     reply_markup=search_replacements_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Группа' or
                     mess.text == 'Курс' or
                     mess.text == 'Направление' or
                     mess.text == 'Препoдаватель',
                     content_types=['text'])
def select_type_of_search_handler(message):

    answer = ('Укажи ' + message.text.lower().replace('па', 'пу') +
              ' для поиска:')
    reply_markup = tb.types.ReplyKeyboardMarkup(True)
    force_markup = tb.types.ForceReply()

    if message.text == 'Препoдаватель':
        answer = 'Введи Фамилию препoдавателя для пoиска: <i>(и И. О.)</i>'
        markup = force_markup
    elif message.text == 'Группа':
        markup = force_markup
        answer = '%s (можно через запятую):' % answer.replace(':', '')
    elif message.text == 'Курс':
        [reply_markup.row(course) for course in const.existing_courses]
        reply_markup.row('« Нaзад')
        markup = reply_markup
    elif message.text == 'Направление':
        [reply_markup.row(division) for division in const.existing_divisions]
        reply_markup.row('« Нaзад')
        markup = reply_markup

    answer += '\nДля отмены используй /home'
    bot.send_message(message.chat.id, answer, reply_markup=markup,
                     parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.reply_to_message is not None and
                     mess.reply_to_message.from_user.username ==
                     bot_username and
                     ' для поиска' in mess.reply_to_message.text,
                     content_types=['text'])
def write_replacement_group_handler(message):

    answer = 'Меню замен'
    nothing_to_search = []
    valid_splited_mess = []
    splited_mess = message.text.split(',')

    for mess in splited_mess:
        if mess not in valid_splited_mess:
            valid_splited_mess.append(mess)

    for mess_text in valid_splited_mess:
        if 'группу' in message.reply_to_message.text:
            lower_groups = [group.lower() for group in const.existing_groups]
            if mess_text.lower().replace(' ', '') in lower_groups:
                index = lower_groups.index(mess_text.lower().replace(' ', ''))
                group = const.existing_groups[index]
                answers = func.get_data_from_replacements(group=group)
                if answers != None:
                    for answer in answers:
                        if len(valid_splited_mess) != 1:
                            answer = answer.replace(
                                const.emoji['anticlockwise'],
                                '%s <b>[%s]</b>' % (
                                    const.emoji['anticlockwise'], group))
                        bot.send_message(message.chat.id, answer,
                                         parse_mode='HTML')
                else:
                    answer = const.emoji['clock'] + ' Замены ещё не вывесили.'
                    bot.send_message(message.chat.id, answer,
                                     reply_markup=replacements_keyboard)
            else:
                if mess_text not in nothing_to_search:
                    nothing_to_search.append(mess_text)

    if nothing_to_search:
        nothing_answer = 'Ничего не найдено для:\n'
        for text in nothing_to_search:
            if text == nothing_to_search[-1]:
                nothing_answer += '<b>%s</b>.' % text.strip()
            else:
                nothing_answer += '<b>%s</b>, ' % text.strip()
        bot.send_message(message.chat.id, nothing_answer,
                         reply_markup=replacements_keyboard, parse_mode='HTML')
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text in const.existing_courses or
                     mess.text in const.existing_divisions,
                     content_types=['text'])
def write_replacement_handler(message):

    loading_answer = 'Загрузка\U00002026'
    loading_message = bot.send_message(message.chat.id, loading_answer)

    valid_groups = []
    if message.text in const.existing_courses:
        for alias in const.student_groups:
            str_alias = list(alias.keys())[0]
            if message.text[0] in str_alias:
                for name in alias[str_alias]:
                    valid_groups.append(name['StudentGroupName'])
    elif message.text in const.existing_divisions:
        for division in const.divisions:
            if division['Name'] == message.text:
                valid_alias = division['Alias']
        for alias in const.student_groups:
            str_alias = list(alias.keys())[0]
            if valid_alias in str_alias:
                for name in alias[str_alias]:
                    valid_groups.append(name['StudentGroupName'])

    dates = []
    all_repls = []
    count_of_days = []
    for group in valid_groups:
        repls = func.get_data_from_replacements(group=group)
        if repls == None:
            repls = const.emoji['clock'] + ' Замены ещё не вывесили.'
            bot.edit_message_text('Готово!', message.chat.id,
                                  loading_message.message_id)
            bot.send_message(message.chat.id, repls,
                             reply_markup=replacements_keyboard)
            return
        else:
            if not count_of_days:
                count_of_days.append(len(repls))

            for repl in repls:
                all_repls.append('%s$|$%s' % (group, repl))

    for i in range(count_of_days[0]):
        curent_repl = all_repls[i].split('$|$')[1]
        if 'Нет замен' in curent_repl:
            dates.append(curent_repl.replace('(', '').replace(')', '')
                         .split()[-1][:-1])
        else:
            dates.append(curent_repl.split('\n')[0].split()[-1])

    dates.sort()
    circle = 1
    for date in dates:
        answer = ''
        dt = date.split('.')
        answer += '%s Замена на %s %s' % (
            const.emoji['anticlockwise'],
            func.day_of_week_parsing_day(datetime.isoweekday(datetime(
                int(dt[2]), int(dt[1]), int(dt[0])))),
            date)

        without_repl = []
        for repl in all_repls:
            grp_and_repl = repl.split('$|$')
            if date in grp_and_repl[1]:
                if 'Нет замен' in grp_and_repl[1]:
                    without_repl.append(grp_and_repl[0])
                else:
                    answer += '\n\n<b>—————— [%s] ——————</b>\n%s' % (
                        grp_and_repl[0],
                        '\n\n'.join(grp_and_repl[1].split('\n\n')[1:]))

        if without_repl:
            if '—' in answer:
                prefix = '%s ' % const.emoji['anticlockwise']
            else:
                prefix = ''
            answer += '\n\n%sНет замен для:\n' % prefix
            for group in without_repl:
                if group == without_repl[-1]:
                    answer += '<b>%s</b>.' % group
                else:
                    answer += '<b>%s</b>, ' % group

        if circle == 1:
            bot.edit_message_text('Готово!', message.chat.id,
                                  loading_message.message_id)

        func.send_long_message(bot, answer, message.chat.id,
                               replacements_keyboard)

        circle += 1
    func.log_me(message)


# @bot.message_handler(func=lambda mess: mess.text == const.emoji['bust_in_silhouette'] and (mess.chat.id in const.m50ids and func.get_student_group(mess.chat.id).lower() == 'м50'),
#                      content_types=['text'])
# def teacher_schedule_handler(message):

#     if message.text == const.emoji['bust_in_silhouette']:
#         answer = (
#             'Введи Фамилию преподавателя: <i>(и И. О.)</i>\n'
#             'Для отмены используй /home')
#     markup = tb.types.ForceReply()
#     bot.send_message(message.chat.id, answer, parse_mode='HTML',
#                      reply_markup=markup)
#     func.log_me(message)


# @bot.message_handler(func=lambda mess: mess.reply_to_message is not None and
#                      mess.reply_to_message.from_user.username ==
#                      bot_username and (mess.chat.id in const.m50ids and func.get_student_group(mess.chat.id).lower() == 'м50') and
#                      ('Введи Фамилию преподавателя:' in
#                       mess.reply_to_message.text or
#                       'препoдавателя' in
#                       mess.reply_to_message.text),
#                      content_types=['text'])
# def write_teacher_name_handler(message):

#     i = 0
#     answer = ''

#     educators = []
#     teachers = func.search_teacher(message.text, from_menu=True)

#     if 'препoдавателя' in message.reply_to_message.text:
#         sched_keyboard = replacements_keyboard
#     else:
#         sched_keyboard = schedule_keyboard

#     if len(teachers) is 0:
#         answer = 'Никого не найдено'
#         bot.send_message(message.chat.id, answer,
#                          reply_markup=sched_keyboard)
#         func.log_me(message)
#         return

#     short_teachers = func.shorting_teachers(teachers)
#     teachers_keyboard = tb.types.InlineKeyboardMarkup(row_width=2)

#     if teachers[0] and len(teachers[0]) <= 20:
#         if 'Введи Фамилию преподавателя:' in message.reply_to_message.text:
#             if len(short_teachers) == 1:
#                 answer += (const.emoji['mag_right'] +
#                            ' Найденный преподаватель:')
#                 if func.is_data_invalid(short_teachers[0]):
#                     if short_teachers[0] in const.teacher_name:
#                         index = const.teacher_name.index(short_teachers[0])
#                     elif short_teachers[0] in const.sht_teachers:
#                         index = const.sht_teachers.index(short_teachers[0])
#                     elif short_teachers[0] in const.cap_teachers:
#                         index = const.cap_teachers.index(short_teachers[0])
#                     short_teachers[0] = const.teacher_name[index]
#             else:
#                 answer += (const.emoji['mag_right'] +
#                            ' Найденные преподаватели:')
#         elif 'препoдавателя' in message.reply_to_message.text:
#             if len(short_teachers) == 1:
#                 answer += (const.emoji['mag_right'] +
#                            ' Нaйденный преподаватель:')
#                 if func.is_data_invalid(short_teachers[0]):
#                     if short_teachers[0] in const.teacher_name:
#                         index = const.teacher_name.index(short_teachers[0])
#                     elif short_teachers[0] in const.sht_teachers:
#                         index = const.sht_teachers.index(short_teachers[0])
#                     elif short_teachers[0] in const.cap_teachers:
#                         index = const.cap_teachers.index(short_teachers[0])
#                     short_teachers[0] = const.teacher_name[index]
#             else:
#                 answer += (const.emoji['mag_right'] +
#                            ' Нaйденные преподаватели:')

#         for teacher in short_teachers:
#             try:
#                 educators.append(tb.types.InlineKeyboardButton(
#                     text=teacher,
#                     callback_data=teacher + '|' + str(teachers[1][i])))
#                 i += 1
#             except:
#                 continue
#         teachers_keyboard.add(*educators)
#         teachers_keyboard.row(tb.types.InlineKeyboardButton(
#             text='Отмена', callback_data='Отмена'))

#         bot.send_message(message.chat.id, 'Готово!',
#                          reply_markup=sched_keyboard)
#         bot.send_message(message.chat.id, answer,
#                          reply_markup=teachers_keyboard)
#     elif len(teachers[0]) > 20:
#         answer += ('Слишком много преподавателей\n'
#                    'Пожалуйста, <b>уточни</b>')
#         bot.send_message(message.chat.id, answer, parse_mode='HTML',
#                          reply_markup=sched_keyboard)
#     else:
#         answer = 'Никого не найдено'
#         bot.send_message(message.chat.id, answer,
#                          reply_markup=sched_keyboard)
#         func.log_me(message)


@bot.message_handler(func=lambda mess: mess.reply_to_message is not None and
                     mess.reply_to_message.from_user.username ==
                     bot_username and
                     'Напиши мне что-нибудь' in mess.reply_to_message.text,
                     content_types=['text'])
def users_callback_handler(message):

    bot.forward_message(conf.my_id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Записал. Жди ответа от разработчика.',
                     reply_to_message_id=message.message_id,
                     reply_markup=main_keyboard(message.chat.id))
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Управление' and
                     mess.chat.id == int(conf.my_id),
                     content_types=['text'])
def manage_handler(message):

    answer = 'Управление'
    manage_keyboard = tb.types.ReplyKeyboardMarkup(True)
    manage_keyboard.row('Сокращение звонков', 'Рассылка')
    manage_keyboard.row('« Назад')
    bot.send_message(message.chat.id, answer, reply_markup=manage_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Сокращение звонков' and
                     mess.chat.id == int(conf.my_id),
                     content_types=['text'])
def abridged_calls_handler(message):

    answer = 'Укажи дату сокращенных пар:'
    force_reply = tb.types.ForceReply()
    bot.send_message(message.chat.id, answer, reply_markup=force_reply)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Рассылка' and
                     mess.chat.id == int(conf.my_id),
                     content_types=['text'])
def newsletter_handler(message):

    answer = 'Для кого рассылка:'
    newsletter_keyboard = tb.types.ReplyKeyboardMarkup(True)
    newsletter_keyboard.row('Студентам', 'Преподавателям')
    newsletter_keyboard.row('Всем')
    bot.send_message(message.chat.id, answer, reply_markup=newsletter_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Студентам' and
                     mess.chat.id == int(conf.my_id),
                     content_types=['text'])
def students_newsletter_handler(message):

    answer = 'Введи список групп через запятую:'
    newsletter_keyboard = tb.types.ReplyKeyboardMarkup(True)
    newsletter_keyboard.row('Студентам', 'Преподавателям')
    newsletter_keyboard.row('Всем')
    bot.send_message(message.chat.id, answer, reply_markup=newsletter_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Преподавателям' and
                     mess.chat.id == int(conf.my_id),
                     content_types=['text'])
def teachers_newsletter_handler(message):

    answer = 'Введи список преподавателей через запятую:'
    newsletter_keyboard = tb.types.ReplyKeyboardMarkup(True)
    newsletter_keyboard.row('Студентам', 'Преподавателям')
    newsletter_keyboard.row('Всем')
    bot.send_message(message.chat.id, answer, reply_markup=newsletter_keyboard)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.text == 'Всем' and
                     mess.chat.id == int(conf.my_id),
                     content_types=['text'])
def all_newsletter_handler(message):

    answer = 'Укажи сообщение для отправки:'
    force_reply = tb.types.ForceReply()
    bot.send_message(message.chat.id, answer, reply_markup=force_reply)
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.reply_to_message is not None and
                     mess.reply_to_message.from_user.username ==
                     bot_username and mess.chat.id == int(conf.my_id) and
                     mess.reply_to_message.text ==
                     'Укажи сообщение для отправки:',
                     content_types=['text'])
def send_newsletter_to_all_handler(message):

    for user in func.get_not_banned_users(message.chat.id):
        try:
            bot.send_message(user[0], message.text, True,
                             parse_mode='HTML', reply_markup=main_keyboard(message.chat.id))
        except Exception as err:
            answer = (const.emoji['cross_mark'] +
                      ' ' + str(user[0]) + '\n' + str(err))
            bot.send_message(message.chat.id, answer)
            continue
        sleep(0.04)
    bot.send_message(message.chat.id, const.emoji['check_mark'])
    func.log_me(message)


@bot.message_handler(func=lambda mess: mess.reply_to_message is not None and
                     mess.reply_to_message.from_user.username ==
                     bot_username and
                     'Укажи дату сокращенных пар' in mess.reply_to_message.text
                     and mess.chat.id == int(conf.my_id),
                     content_types=['text'])
def save_abridged_call_handler(message):

    write_answer = 'Записал'
    invalid_format_answer = 'Неверный формат'

    if re.match(r'\d\d.\d\d.\d\d\d\d', message.text):
        sql_con = connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT abridged_calls
                            FROM offer''')
        previous_value = cursor.fetchone()[0]
        cursor.close()
        sql_con.close()

        if previous_value == None:
            new_value = message.text
        else:
            new_value = previous_value + '\n' + message.text

        sql_con = connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE offer
                             SET abridged_calls = ?''', (new_value,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        answer = write_answer
    else:
        answer = invalid_format_answer
    bot.send_message(message.chat.id, answer,
                     reply_to_message_id=message.message_id,
                     reply_markup=main_keyboard(message.chat.id))
    func.log_me(message)


'''
        Inline handlers
'''


@bot.inline_handler(func=lambda query: reg_func.get_step(query.from_user.id) ==
                    False and
                    func.is_user_exist(query.from_user.id) ==
                    False)
def not_exist_user_query_handler(query):
    answer = tb.types.InlineQueryResultArticle(
        id=1,
        title='Начать пользоваться сервисом',
        input_message_content=tb.types.InputTextMessageContent(
            message_text='/start')
    )
    bot.answer_inline_query(query.id, [answer], cache_time=1)
    func.inline_log_me(query)


@bot.inline_handler(func=lambda query: reg_func.get_step(
                    query.from_user.id) == 'select_teacher' and
                    len(query.query) is 0)
def empty_query_handler(query):
    answer = tb.types.InlineQueryResultArticle(
        id=1,
        title='Начианай вводить фамилию преподавателя',
        input_message_content=tb.types.InputTextMessageContent(
            message_text='Введи ФИО преподавателя')
    )
    bot.answer_inline_query(query.id, [answer], cache_time=1)
    func.inline_log_me(query)


@bot.inline_handler(func=lambda query: reg_func.get_step(
                    query.from_user.id) == 'select_teacher' and
                    len(query.query) > 0)
def query_text_handler(query):
    teachers = func.search_teacher(query.query)

    if teachers and len(teachers) <= 10:
        answers = []

        query_id = 1
        for teacher in teachers:
            answer = tb.types.InlineQueryResultArticle(
                id=query_id, title=teacher,
                input_message_content=tb.types.InputTextMessageContent(
                    message_text=teacher)
            )
            answers.append(answer)
            query_id += 1
        bot.answer_inline_query(query.id, answers, cache_time=1)
    elif len(teachers) > 10:
        answer = tb.types.InlineQueryResultArticle(
            id=1,
            title='Слишком много преподавателей',
            description='Пожалуйста, уточни',
            input_message_content=tb.types.InputTextMessageContent(
                message_text='Слишком много преподавателей\n'
                'Пожалуйста, <b>уточни</b>',
                parse_mode='HTML')
        )
        bot.answer_inline_query(query.id, [answer], cache_time=1)

    else:
        answer = tb.types.InlineQueryResultArticle(
            id=1,
            title='Никого не найдено',
            input_message_content=tb.types.InputTextMessageContent(
                message_text='Никого не найдено\n'
                'Если по какой-то причине отсусвует какой либо '
                             'преподаватель, просьба сразу сообщить '
                             '<a href="https://t.me/lee_kei">разработчику</a>.',
                parse_mode='HTML',
                disable_web_page_preview=True)
        )
        bot.answer_inline_query(query.id, [answer], cache_time=1)
    func.inline_log_me(query)


'''
        Callback query handlers
'''


@bot.callback_query_handler(func=lambda call_back: func.is_user_banned(
    call_back.message.chat.id))
def banned_user_inline_handler(call_back):
    answer = const.emoji['no_entry'] + (' Вы заблокированы по причине неоднократного спама! '
                                        'Если считаете что не виновны и хотите вновь начать '
                                        'пользоваться сервисом — сообщите об этом <a href="https://t.me/lee_kei">разработчику</a>.')
    bot.edit_message_text(answer, call_back.message.chat.id,
                          call_back.message.message_id,
                          parse_mode='HTML',
                          disable_web_page_preview=True)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'back_reg' and
                            (reg_func.get_step(call_back.message.chat.id) ==
                             'select_teacher' or
                             func.is_user_exist(call_back.message.chat.id)))
def back_from_reg_handler(call_back):
    if func.is_user_exist(call_back.message.chat.id):
        answer = 'Главное меню'
        bot.edit_message_text(answer, call_back.message.chat.id,
                              call_back.message.message_id)
        bot.send_message(call_back.message.chat.id, answer,
                         reply_markup=main_keyboard(call_back.message.chat.id))
    else:
        start_handler(call_back.message, True)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back: reg_func.get_step(
    call_back.message.chat.id) == 'select_teacher' and
    (call_back.data.split('|')[0] in const.teacher_name or
     call_back.data.split('|')[0] in const.sht_teachers or
     call_back.data.split('|')[0] in const.cap_teachers))
def search_teacher_inline_handler(call_back):
    bot.send_chat_action(call_back.message.chat.id, 'typing')
    edit_msg = bot.edit_message_text('Почти готово! '
                                     'Запоминаю твой выбор\U00002026',
                                     call_back.message.chat.id,
                                     call_back.message.message_id)

    index = int(call_back.data.split('|')[1])
    teacher = const.cap_teachers[index]

    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''UPDATE user_choice
                         SET student_group_name = ?
                       WHERE user_id = ?''',
                   (teacher, call_back.message.chat.id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()

    text = '>> ' + teacher
    answer = 'Подтверди выбор преподавателя:\n' + '<b>' + text + '</b>'
    choice_keyboard = tb.types.ReplyKeyboardMarkup(True, False)
    buttons = ['Все верно',
               'Другой преподаватель',
               'Другой способ регистрации']
    for button in buttons:
        choice_keyboard.row(button)
    bot.edit_message_text('Готово!',
                          call_back.message.chat.id,
                          edit_msg.message_id)
    bot.send_message(call_back.message.chat.id, answer,
                     parse_mode='HTML',
                     reply_markup=choice_keyboard)

    reg_func.set_next_step(call_back.message.chat.id, 'confirm_choice_teacher')
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            reg_func.get_step(call_back.message.chat.id) ==
                            'select_status')
def confirm_status_inline_handler(call_back):
    bot.edit_message_text('Пожалуйста, выбери в качестве кого ты хочешь зайти:',
                          call_back.message.chat.id,
                          call_back.message.message_id)
    return


@bot.callback_query_handler(func=lambda call_back:
                            reg_func.get_step(call_back.message.chat.id) ==
                            'select_division')
def confirm_division_inline_handler(call_back):
    bot.edit_message_text('Пожалуйста, укажи направление:',
                          call_back.message.chat.id,
                          call_back.message.message_id)
    return


@bot.callback_query_handler(func=lambda call_back:
                            reg_func.get_step(call_back.message.chat.id) ==
                            'select_admission_year')
def confirm_admission_year_inline_handler(call_back):
    bot.edit_message_text('Пожалуйста, укажи курс:',
                          call_back.message.chat.id,
                          call_back.message.message_id)
    return


@bot.callback_query_handler(func=lambda call_back:
                            reg_func.get_step(call_back.message.chat.id) ==
                            'select_student_group')
def confirm_student_group_inline_handler(call_back):
    bot.edit_message_text('Пожалуйста, укажи группу:',
                          call_back.message.chat.id,
                          call_back.message.message_id)
    return


@bot.callback_query_handler(func=lambda call_back:
                            reg_func.get_step(call_back.message.chat.id ==
                                              'confirm_choice') or
                            reg_func.get_step(call_back.message.chat.id ==
                                              'confirm_choice_teacher'))
def confirm_choice_inline_handler(call_back):
    bot.edit_message_text('Пожалуйста, проверь правильно ли ты всё указал и '
                          'подтверди свой выбор:',
                          call_back.message.chat.id,
                          call_back.message.message_id)
    return


@bot.callback_query_handler(func=lambda call_back: not func.is_user_exist(
    call_back.message.chat.id))
def not_exist_inline_user_handler(call_back):
    answer = ('Чтобы начать пользоваться сервисом, необходимо '
              'зарегистрироваться.\nВоспользуйся коммандой /start')
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Полное ИНФО')
def show_full_info(call_back):
    inline_keyboard = tb.types.InlineKeyboardMarkup()
    inline_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
          name in ['Краткое ИНФО']])
    answer = const.full_info_answer
    bot.edit_message_text(answer, call_back.message.chat.id,
                          call_back.message.message_id,
                          parse_mode='HTML',
                          disable_web_page_preview=True,
                          reply_markup=inline_keyboard)
    inline_answer = 'Много текста ' + const.emoji['arrow_up']
    bot.answer_callback_query(call_back.id, inline_answer, cache_time=1)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Краткое ИНФО')
def show_briefly_info(call_back):
    inline_keyboard = tb.types.InlineKeyboardMarkup()
    inline_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
          name in ['Полное ИНФО']])
    answer = const.briefly_info_answer
    bot.edit_message_text(answer, call_back.message.chat.id,
                          call_back.message.message_id,
                          parse_mode='HTML',
                          disable_web_page_preview=True,
                          reply_markup=inline_keyboard)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back: (
    call_back.data.split('|')[0] in const.teacher_name or
    call_back.data.split('|')[0] in const.sht_teachers or
    call_back.data.split('|')[0] in const.cap_teachers))
def select_teacher_id_handler(call_back):
    index = int(call_back.data.split('|')[1])
    if 'Найденны' in call_back.message.text:
        teacher = const.teacher_name[index]
        func.send_teacher_week_answer(call_back.message, teacher)
    elif 'Нaйденны' in call_back.message.text:
        answers = func.get_data_from_replacements(
            teacher=const.cap_teachers[index])
        if answers != None:
            answers.sort(key=lambda date: date.replace('(', '').replace(')', '')
                         .split()[-1][:-1])
            none_repl = []
            for answer in answers.copy():
                if 'Нет замен' in answer:
                    none_repl.append(answer)
                    index_answer = answers.index(answer)
                    answers[index_answer] = (
                        answer.replace('Нет замен',
                                       'Для преподавателя <b>%s</b> нет замен'
                                       % const.teacher_name[index]))

            if len(answers) != 1 and len(none_repl) == len(answers):
                first_date = (answers[0].replace('(', '').replace(')', '')
                              .split()[-1][:-1])
                second_date = (answers[-1].replace('(', '').replace(')', '')
                               .split()[-1][:-1])
                answer = ('%s Для преподавателя <b>%s</b> нет замен с '
                          '<b>%s</b> по <b>%s</b>.'
                          % (const.emoji['anticlockwise'],
                             const.teacher_name[index],
                             first_date,
                             second_date))
                bot.edit_message_text(answer, call_back.message.chat.id,
                                      call_back.message.message_id,
                                      parse_mode='HTML')
                return

            for answer in answers:
                if answer == answers[0]:
                    bot.edit_message_text(answer, call_back.message.chat.id,
                                          call_back.message.message_id,
                                          parse_mode='HTML')
                else:
                    bot.send_message(call_back.message.chat.id, answer,
                                     parse_mode='HTML')
        else:
            answer = const.emoji['clock'] + ' Замены ещё не вывесили.'
            bot.edit_message_text(answer, call_back.message.chat.id,
                                  call_back.message.message_id)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back: call_back.data == 'Отмена' and (call_back.message.chat.id in const.m50ids and func.get_student_group(call_back.message.chat.id).lower() == 'м50'))
def cancel_handler(call_back):
    bot.send_chat_action(call_back.message.chat.id, 'typing')
    answer = 'Отмена'
    bot.edit_message_text(text=answer, chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id)
    if 'Найденны' in call_back.message.text:
        answer = 'Меню расписания'
        bot.send_message(call_back.message.chat.id, answer,
                         reply_markup=schedule_keyboard)
    elif 'Нaйденны' in call_back.message.text:
        answer = 'Меню замен'
        bot.send_message(call_back.message.chat.id, answer,
                         reply_markup=replacements_keyboard)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            (call_back.data in const.week_day_number.keys() or
                             call_back.data == 'Вся неделя') and (call_back.message.chat.id in const.m50ids and func.get_student_group(call_back.message.chat.id).lower() == 'м50'))
def select_week_day_schedule_handler(call_back):
    day = ''
    if call_back.data == 'Вся неделя':
        day += 'неделю'
    else:
        day += [item[0] for item in const.week_day_titles.items() if
                item[1] == call_back.data][0]

    answer = 'Расписание на <i>{0}</i>\n'.format(day)
    week_type_keyboard = tb.types.InlineKeyboardMarkup()
    ned_week = func.get_week()
    if datetime.isoweekday(datetime.now()) != 7:
        if ned_week == 'UP':
            arrow = const.emoji['arrow_up']
        elif ned_week == 'DOWN':
            arrow = const.emoji['arrow_down']
    elif datetime.isoweekday(datetime.now()) == 7:
        if ned_week == 'UP':
            arrow = const.emoji['arrow_down']
        elif ned_week == 'DOWN':
            arrow = const.emoji['arrow_up']
    week_type_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['Текущее (' + arrow + ')']]
    )
    week_type_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in [const.emoji['arrow_up'] + ' Верхнее',
                     const.emoji['arrow_down'] + ' Нижнее']]
    )
    week_type_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Нaзад']]
    )
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=week_type_keyboard)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data in func.get_active_replace_days(call_back.message.chat.id) or
                            'Вся нeделя' in call_back.data)
def select_week_day_replace_handler(call_back):

    back_from_calendar_replace_handler = tb.types.InlineKeyboardMarkup()
    back_from_calendar_replace_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Нaзaд']])

    if 'Вся нeделя' in call_back.data:
        answerr = []

        for i in range(1, 7):
            answerr.append(func.get_replace_of_day(
                const.num_day[str(i)], call_back.message.chat.id, True))

        if const.emoji['negative_squared_cross_mark'] in call_back.data:
            all_dates = []
            try:
                for date in answerr:
                    str_date = date[-12:][:10].split('.')
                    all_dates.append(
                        datetime(int(str_date[2]), int(str_date[1]), int(str_date[0])))
                all_dates.sort()

                n_d1 = str(all_dates[0])[:10].split('-')
                n_d2 = str(all_dates[-1])[:10].split('-')

                first_date = n_d1[2] + '.' + n_d1[1] + '.' + n_d1[0]
                second_date = n_d2[2] + '.' + n_d2[1] + '.' + n_d2[0]

                answer = (const.emoji['anticlockwise'] + ' Нет замен с <b>' + first_date +
                          '</b> по <b>' + second_date + '</b>.')
            except:
                bot.edit_message_text(text='<b>Упс, что-то пошло не так\U00002026</b>\n' + str(exc_info()[1]),
                                      chat_id=call_back.message.chat.id,
                                      message_id=call_back.message.message_id,
                                      parse_mode='HTML',
                                      reply_markup=back_from_calendar_replace_handler)
            else:
                bot.edit_message_text(text=answer,
                                      chat_id=call_back.message.chat.id,
                                      message_id=call_back.message.message_id,
                                      parse_mode='HTML',
                                      reply_markup=back_from_calendar_replace_handler)
        else:
            back_from_week_replace_handler = tb.types.InlineKeyboardMarkup()
            back_from_week_replace_handler.row(
                *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                    name in ['« Hазад']])
            for i in range(1, 7):
                if i == 1:
                    bot.edit_message_text(text=answerr[i - 1],
                                          chat_id=call_back.message.chat.id,
                                          message_id=call_back.message.message_id,
                                          parse_mode='HTML')
                elif i == 6:
                    bot.send_message(call_back.message.chat.id, answerr[
                                     i - 1], parse_mode='HTML', reply_markup=back_from_week_replace_handler)
                else:
                    bot.send_message(call_back.message.chat.id, answerr[
                                     i - 1], parse_mode='HTML', disable_notification=True)
    else:
        answer = ''

        if 'Понедельник' in call_back.data:
            answer += func.get_replace_of_day(1, call_back.message.chat.id)
        elif 'Вторник' in call_back.data:
            answer += func.get_replace_of_day(2, call_back.message.chat.id)
        elif 'Среда' in call_back.data:
            answer += func.get_replace_of_day(3, call_back.message.chat.id)
        elif 'Четверг' in call_back.data:
            answer += func.get_replace_of_day(4, call_back.message.chat.id)
        elif 'Пятница' in call_back.data:
            answer += func.get_replace_of_day(4, call_back.message.chat.id)
        elif 'Суббота' in call_back.data:
            answer += func.get_replace_of_day(6, call_back.message.chat.id)

        bot.edit_message_text(text=answer,
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='HTML',
                              reply_markup=back_from_calendar_replace_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            'Расписание на неделю' in call_back.message.text and (call_back.message.chat.id in const.m50ids and func.get_student_group(call_back.message.chat.id).lower() == 'м50'))
def all_week_schedule_handler(call_back):
    if (call_back.data == 'Текущее (' + const.emoji['arrow_up'] + ')' or
            call_back.data == 'Текущее (' + const.emoji['arrow_down'] + ')'):
        func.send_schedule_force_week_answer(call_back.message, 0)
    elif call_back.data == const.emoji['arrow_up'] + ' Верхнее':
        func.send_schedule_force_week_answer(call_back.message, 2)
    elif call_back.data == const.emoji['arrow_down'] + ' Нижнее':
        func.send_schedule_force_week_answer(call_back.message, 1)
    elif call_back.data == '« Нaзад':
        answer = 'Выбери день:'
        week_day_calendar = tb.types.InlineKeyboardMarkup()
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in const.week_day_number.keys()])
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in ['Вся неделя']])
        bot.edit_message_text(text=answer,
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='HTML',
                              reply_markup=week_day_calendar)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Текущее (' + const.emoji['arrow_up'] + ')' or
                            call_back.data == 'Текущее (' + const.emoji['arrow_down'] + ')' or
                            call_back.data == const.emoji['arrow_up'] + ' Верхнее' or
                            call_back.data == const.emoji['arrow_down'] + ' Нижнее')
def week_day_schedule_handler(call_back):
    td = const.week_day_number[const.week_day_titles[
        call_back.message.text.split('на ')[-1]]]

    if call_back.data == const.emoji['arrow_up'] + ' Верхнее':
        answer = func.create_schedule_week_answer(call_back.message.chat.id,
                                                  td,
                                                  2)
    elif call_back.data == const.emoji['arrow_down'] + ' Нижнее':
        answer = func.create_schedule_week_answer(call_back.message.chat.id,
                                                  td,
                                                  1)
    else:
        answer = func.create_schedule_week_answer(call_back.message.chat.id,
                                                  td,
                                                  0)

    day_type_keyboard = tb.types.InlineKeyboardMarkup()
    day_type_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Нaзад']])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=day_type_keyboard)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == '« Нaзaд')
def back_from_calendar_replace_handler(call_back):
    group = func.get_student_group(call_back.message.chat.id)
    if func.get_alias(call_back.message.chat.id) == 'PREP':
        index = const.cap_teachers.index(group)
        for_any = 'преподавателя'
        group = const.sht_teachers[index][:-1]
    else:
        for_any = 'группы'

    answer = ('Выбери день:\n' + const.emoji['check_mark'] + ' – Есть замены для ' + for_any + ' <b>{0}</b>.\n'.format(group)
              + const.emoji['negative_squared_cross_mark'] +
              ' – Нет замен для ' + for_any + ' <b>{0}</b>.\n'.format(group)
              + const.emoji['cross_mark'] +
              ' – Замены на ближайший день недели ещё не вывесили. Будут показаны предыдущие замены.')
    week_day_calendar = tb.types.InlineKeyboardMarkup()
    active_days = func.get_active_replace_days(call_back.message.chat.id)
    y = []
    n = []
    cross = []
    for day in active_days:
        if const.emoji['check_mark'] in day:
            y.append(1)
        elif const.emoji['negative_squared_cross_mark'] in day:
            n.append(1)
        elif const.emoji['cross_mark'] in day:
            cross.append(1)
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [day]])
    if len(y) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['check_mark'] + ' Вся нeделя']])
    elif len(n) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['negative_squared_cross_mark'] + ' Вся нeделя']])
    elif len(cross) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['cross_mark'] + ' Вся нeделя']])
    else:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in ['Вся нeделя']])

    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=week_day_calendar)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == '« Hазад')
def back_from_week_replace_handler(call_back):
    bot.edit_message_text(text=call_back.message.text,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML')

    bot.send_chat_action(call_back.message.chat.id, 'typing')
    group = func.get_student_group(call_back.message.chat.id)
    if func.get_alias(call_back.message.chat.id) == 'PREP':
        index = const.cap_teachers.index(group)
        for_any = 'преподавателя'
        group = const.sht_teachers[index][:-1]
    else:
        for_any = 'группы'

    answer = ('Выбери день:\n' + const.emoji['check_mark'] + ' – Есть замены для ' + for_any + ' <b>{0}</b>.\n'.format(group)
              + const.emoji['negative_squared_cross_mark'] +
              ' – Нет замен для ' + for_any + ' <b>{0}</b>.\n'.format(group)
              + const.emoji['cross_mark'] +
              ' – Замены на ближайший день недели ещё не вывесили. Будут показаны предыдущие замены.')
    week_day_calendar = tb.types.InlineKeyboardMarkup()
    active_days = func.get_active_replace_days(call_back.message.chat.id)
    y = []
    n = []
    cross = []
    for day in active_days:
        if const.emoji['check_mark'] in day:
            y.append(1)
        elif const.emoji['negative_squared_cross_mark'] in day:
            n.append(1)
        elif const.emoji['cross_mark'] in day:
            cross.append(1)
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [day]])
    if len(y) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['check_mark'] + ' Вся нeделя']])
    elif len(n) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['negative_squared_cross_mark'] + ' Вся нeделя']])
    elif len(cross) == 6:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in [const.emoji['cross_mark'] + ' Вся нeделя']])
    else:
        week_day_calendar.row(
            *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
                name in ['Вся нeделя']])

    bot.send_message(call_back.message.chat.id, answer,
                     reply_markup=week_day_calendar, parse_mode='HTML')
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == '« Нaзад')
def back_from_ned_rasp_handler(call_back):
    answer = 'Выбери день:'
    week_day_calendar = tb.types.InlineKeyboardMarkup()
    week_day_calendar.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in const.week_day_number.keys()])
    week_day_calendar.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['Вся неделя']])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=week_day_calendar)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == '« Haзад')
def back_from_week_handler(call_back):
    bot.edit_message_text(text=call_back.message.text,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML')

    bot.send_chat_action(call_back.message.chat.id, 'typing')
    answer = 'Выбери день:'
    week_day_calendar = tb.types.InlineKeyboardMarkup()
    week_day_calendar.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in const.week_day_number.keys()])
    week_day_calendar.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['Вся неделя']])
    bot.send_message(call_back.message.chat.id, answer,
                     reply_markup=week_day_calendar)
    func.call_back_log_me(call_back)


# @bot.callback_query_handler(func=lambda call_back:
#                             'Расписания' in call_back.data)
# def podpis_rasp_5_or_9_handler(call_back):
#     answer = 'Выбери, в какое время ты хочешь получать <b>расписание на следующий день</b>:'
#     sql_con = connect(const.path + 'Bot.db')
#     cursor = sql_con.cursor()
#     cursor.execute('''SELECT sending_rasp, sending_rasp_5
#                         FROM user_data
#                        WHERE id = ?''',
#                    (call_back.message.chat.id,))
#     data = cursor.fetchall()[0]
#     cursor.close()
#     sql_con.close()
#     if data[0]:
#         is_rasp_9 = const.emoji['check_mark']
#     else:
#         is_rasp_9 = const.emoji['negative_squared_cross_mark']
#     if data[1]:
#         is_rasp_5 = const.emoji['check_mark']
#     else:
#         is_rasp_5 = const.emoji['negative_squared_cross_mark']
#     sending_keyboard_rasp = tb.types.InlineKeyboardMarkup(True)
#     sending_keyboard_rasp.row(
#         *[tb.types.InlineKeyboardButton(text=name,
#                                         callback_data=name)
#             for name in [const.emoji['five_oclock'] + ' 17:00 (' + is_rasp_5 + ')',
#                          const.emoji['nine_oclock'] + ' 21:00 (' + is_rasp_9 + ')']])
#     sending_keyboard_rasp.row(
#         *[tb.types.InlineKeyboardButton(text=name,
#                                         callback_data='« Назад')
#             for name in ['« Назад']])
#     bot.edit_message_text(text=answer,
#                           chat_id=call_back.message.chat.id,
#                           message_id=call_back.message.message_id,
#                           parse_mode='HTML', reply_markup=sending_keyboard_rasp)
#     func.call_back_log_me(call_back)


# @bot.callback_query_handler(func=lambda call_back:
#                             const.emoji['five_oclock'] + ' 17:00' in call_back.data)
# def podpis_rasp_5_handler(call_back):
#     answer = (('%s Здесь ты можешь <b>подписаться</b> на рассылку расписания на '
#                'следующий день или <b>отписаться</b> от неё.\n'
#                '%s Рассылка производится в 17:00') %
#               (const.emoji['mailbox_on'], const.emoji['envelope']))
#     sending_keyboard_rasp = tb.types.InlineKeyboardMarkup(True)
#     if func.is_sending_rasp_on(call_back.message.chat.id, True):
#         sending_keyboard_rasp.row(
#             *[tb.types.InlineKeyboardButton(text=name,
#                                             callback_data='Отписаться_5')
#                 for name in [const.emoji['cross_mark'] + ' Отписаться']])
#     else:
#         sending_keyboard_rasp.row(
#             *[tb.types.InlineKeyboardButton(text=name,
#                                             callback_data='Подписаться_5')
#                 for name in [const.emoji['check_mark'] + ' Подписаться']])
#     sending_keyboard_rasp.row(
#         *[tb.types.InlineKeyboardButton(text=name,
#                                         callback_data='« Назад')
#             for name in ['« Назад']])
#     bot.edit_message_text(text=answer,
#                           chat_id=call_back.message.chat.id,
#                           message_id=call_back.message.message_id,
#                           parse_mode='HTML', reply_markup=sending_keyboard_rasp)
#     func.call_back_log_me(call_back)


# @bot.callback_query_handler(func=lambda call_back:
#                             const.emoji['nine_oclock'] + ' 21:00' in call_back.data)
# def podpis_rasp_9_handler(call_back):
#     answer = (('%s Здесь ты можешь <b>подписаться</b> на рассылку расписания на '
#                'следующий день или <b>отписаться</b> от неё.\n'
#                '%s Рассылка производится в 21:00') %
#               (const.emoji['mailbox_on'], const.emoji['envelope']))
#     sending_keyboard_rasp = tb.types.InlineKeyboardMarkup(True)
#     if func.is_sending_rasp_on(call_back.message.chat.id):
#         sending_keyboard_rasp.row(
#             *[tb.types.InlineKeyboardButton(text=name,
#                                             callback_data='Отписаться_9')
#                 for name in [const.emoji['cross_mark'] + ' Отписаться']])
#     else:
#         sending_keyboard_rasp.row(
#             *[tb.types.InlineKeyboardButton(text=name,
#                                             callback_data='Подписаться_9')
#                 for name in [const.emoji['check_mark'] + ' Подписаться']])
#     sending_keyboard_rasp.row(
#         *[tb.types.InlineKeyboardButton(text=name,
#                                         callback_data='« Назад')
#             for name in ['« Назад']])
#     bot.edit_message_text(text=answer,
#                           chat_id=call_back.message.chat.id,
#                           message_id=call_back.message.message_id,
#                           parse_mode='HTML', reply_markup=sending_keyboard_rasp)
#     func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            'Замен' in call_back.data)
def podpis_repl_handler(call_back):
    answer = (('%s Здесь ты можешь <b>подписаться</b> на рассылку замен на '
               'следующий день или <b>отписаться</b> от неё.\n%s Рассылка '
               'производится после публикования замен на сайте колледжа.') %
              (const.emoji['mailbox_on'], const.emoji['envelope']))
    sending_keyboard_repl = tb.types.InlineKeyboardMarkup(True)
    if func.is_sending_zam_on(call_back.message.chat.id):
        sending_keyboard_repl.row(
            *[tb.types.InlineKeyboardButton(text=name,
                                            callback_data='Отписaться')
                for name in [const.emoji['cross_mark'] + ' Отписaться']])
    else:
        sending_keyboard_repl.row(
            *[tb.types.InlineKeyboardButton(text=name,
                                            callback_data='Подписaться')
                for name in [const.emoji['check_mark'] + ' Подписaться']])
    sending_keyboard_repl.row(
        *[tb.types.InlineKeyboardButton(text=name,
                                        callback_data='« Назад')
            for name in ['« Назад']])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML', reply_markup=sending_keyboard_repl)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            'Отсутствие замен' in call_back.data)
def not_repl_handler(call_back):
    sending_keyboard_repl = tb.types.InlineKeyboardMarkup(True)
    if func.is_sending_not_repl_on(call_back.message.chat.id):
        answer = (('%s <b>Отписка</b> от рассылки об <b>отсутствии замен</b> '
                   'позволит <b>получать уведомления</b> только в том случае, '
                   'если <b>замены присутствуют.</b>\n%s Рассылка производится '
                   'после публикования замен на сайте колледжа.') %
                  (const.emoji['mailbox_off'], const.emoji['envelope']))
        sending_keyboard_repl.row(
            *[tb.types.InlineKeyboardButton(
                text=name,
                callback_data='Отписaться (отсутствия замен)')
              for name in [const.emoji['cross_mark'] + ' Отписaться']])
    else:
        answer = (('%s <b>Подписка</b> к рассылке об <b>отсутствии замен</b> '
                   'позволит <b>получать уведомления</b> даже в том случае, '
                   'если <b>замены отсусвуют.</b>\n%s Рассылка производится '
                   'после публикования замен на сайте колледжа.') %
                  (const.emoji['mailbox_on'], const.emoji['envelope']))
        sending_keyboard_repl.row(
            *[tb.types.InlineKeyboardButton(
                text=name,
                callback_data='Подписaться (отсутствия замен)')
              for name in [const.emoji['check_mark'] + ' Подписaться']])
    sending_keyboard_repl.row(
        *[tb.types.InlineKeyboardButton(text=name,
                                        callback_data='« Назад')
            for name in ['« Назад']])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML', reply_markup=sending_keyboard_repl)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == '« Назад')
def back_from_podpis_handler(call_back):
    answer = ('Выбери, на рассылку чего ты хочешь <b>подписаться</b> или <b>отписаться</b>:\n'
              + const.emoji['check_mark'] + ' – Рассылка включена.\n'
              + const.emoji['negative_squared_cross_mark'] + ' – Рассылка отключена.')
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor = sql_con.cursor()
    cursor.execute('''SELECT sending_rasp, sending_rasp_5, sending_zam, sending_without_repl
                        FROM user_data
                       WHERE id = ?''',
                   (call_back.message.chat.id,))
    data = cursor.fetchall()[0]
    cursor.close()
    sql_con.close()

    not_replace = False
    # if data[0] or data[1]:
    #     schedule = ('Расписания (%s)' %
    #                 const.emoji['check_mark'])
    # else:
    #     schedule = ('Расписания (%s)' %
    #                 const.emoji['negative_squared_cross_mark'])
    if data[2]:
        replace = ('Замен (%s)' %
                   const.emoji['check_mark'])
        if data[3]:
            not_replace = ('Отсутствие замен (%s)' %
                           const.emoji['check_mark'])
        else:
            not_replace = ('Отсутствие замен (%s)' %
                           const.emoji['negative_squared_cross_mark'])
    else:
        replace = ('Замен (%s)' %
                   const.emoji['negative_squared_cross_mark'])

    sending_keyboard = tb.types.InlineKeyboardMarkup(True)
    sending_keyboard.row(
        *[tb.types.InlineKeyboardButton(text=name,
                                        callback_data=name)
            for name in [replace]])
    if not_replace:
        sending_keyboard.row(tb.types.InlineKeyboardButton(
            text=not_replace, callback_data=not_replace))
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=sending_keyboard)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Подписаться_5')
def sending_on_rasp_5_handler(call_back):
    func.set_sending_rasp(call_back.message.chat.id, True, True)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = ('{0} Рассылка <b>активирована</b>\nЖди рассылку в 17:00'
              ''.format(const.emoji['mailbox_on']))
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Отписаться_5')
def sending_off_rasp_5_handler(call_back):
    func.set_sending_rasp(call_back.message.chat.id, False, True)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = '{0} Рассылка <b>отключена</b>'.format(const.emoji['mailbox_off'])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Подписаться_9')
def sending_on_rasp_9_handler(call_back):
    func.set_sending_rasp(call_back.message.chat.id, True)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = ('{0} Рассылка <b>активирована</b>\nЖди рассылку в 21:00'
              ''.format(const.emoji['mailbox_on']))
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Отписаться_9')
def sending_off_rasp_9_handler(call_back):
    func.set_sending_rasp(call_back.message.chat.id, False)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = '{0} Рассылка <b>отключена</b>'.format(const.emoji['mailbox_off'])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Подписaться')
def sending_on_repl_handler(call_back):
    func.set_sending_zam(call_back.message.chat.id, True)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = ('{0} Рассылка <b>активирована</b>\nЖди рассылку после опубликования замен.'
              ''.format(const.emoji['mailbox_on']))
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Отписaться')
def sending_off_repl_handler(call_back):
    func.set_sending_zam(call_back.message.chat.id, False)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = '{0} Рассылка <b>отключена</b>'.format(const.emoji['mailbox_off'])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Подписaться (отсутствия замен)')
def sending_on_not_repl_handler(call_back):
    func.set_sending_not_zam(call_back.message.chat.id, True)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = ('{0} Рассылка об отсутствии замен <b>активирована</b>\nЖди рассылку после опубликования замен.'
              ''.format(const.emoji['mailbox_on']))
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Отписaться (отсутствия замен)')
def sending_off_not_repl_handler(call_back):
    func.set_sending_not_zam(call_back.message.chat.id, False)
    back_from_podpis_handler = tb.types.InlineKeyboardMarkup()
    back_from_podpis_handler.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Назад']])
    answer = '{0} Рассылка об отсутствии замен <b>отключена</b>'.format(const.emoji[
                                                                        'mailbox_off'])
    bot.edit_message_text(text=answer,
                          chat_id=call_back.message.chat.id,
                          message_id=call_back.message.message_id,
                          parse_mode='HTML',
                          reply_markup=back_from_podpis_handler)
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Статистика')
def statistics_handler(call_back):
    data = func.get_rate_statistics()
    if data is None:
        answer = 'Пока что нет оценок.'
    else:
        rate = const.emoji['star'] * round(data[0])
        answer = 'Средняя оценка: {0}\n{1} ({2})'.format(
            round(data[0], 1), rate, data[1])
    if str(call_back.message.chat.id) == conf.my_id:
        admin_data = func.get_statistics_for_admin()
        admin_answer = '\n\nКолличество пользователей: {0}'.format(
            admin_data)
        bot.send_message(conf.my_id, admin_answer)
    try:
        bot.edit_message_text(text=answer,
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='HTML')
    except tb.apihelper.ApiException:
        pass
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data == 'Связь')
def feedback_handler(call_back):
    force_reply = tb.types.ForceReply()
    feedback_answer = 'Обратная связь\nДля отмены используй /home'
    answer = ('Напиши мне что-нибудь\nРазработчик обязательно ответит на '
              'твоё сообщение (но лучше будет написать <a href="https://t.me/lee_kei">напрямую</a>):')

    bot.edit_message_text(feedback_answer, call_back.message.chat.id,
                          message_id=call_back.message.message_id)
    bot.send_message(call_back.message.chat.id, answer, True,
                     reply_markup=force_reply,
                     parse_mode='HTML')
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back:
                            call_back.data in ['1', '2', '3', '4', '5'])
def set_rate_handler(call_back):
    rate = call_back.data
    answer = ''
    func.set_rate(call_back.message.chat.id, rate)
    if rate == '5':
        answer += '{0} Пятёрка! Супер! Спасибо большое!'.format(const.emoji[
                                                                'smile'])
    elif rate == '4':
        answer += '{0} Стабильная четверочка. Спасибо!'.format(const.emoji[
                                                               'halo'])
    elif rate == '3':
        answer += ('{0} Удовлетворительно? Ничего\U00002026 тоже оценка. '
                   'Буду стараться лучше.'.format(const.emoji['cold_sweat']))
    elif rate == '2':
        answer += ('{0} Двойка? Быть может, я могу что-то исправить? '
                   'Сделать лучше?\n\nОпиши проблему '
                   '<a href="https://t.me/lee_kei">разработчику</a>, '
                   'и вместе мы ее решим!'.format(const.emoji['disappointed']))
    elif rate == '1':
        answer += ('{0} Единица? Быть может, я могу что-то исправить? '
                   'Сделать лучше?\n\nОпиши проблему '
                   '<a href="https://t.me/lee_kei">разработчику</a>, '
                   'и вместе мы ее решим!'.format(const.emoji['disappointed']))
    user_rate = func.get_user_rate(call_back.message.chat.id)
    rate_keyboard = tb.types.InlineKeyboardMarkup(row_width=5)
    rate_keyboard.add(*[tb.types.InlineKeyboardButton(
        text=const.emoji[
            'star2'] if user_rate < count_of_stars else const.emoji['star'],
        callback_data=str(count_of_stars))
        for count_of_stars in (1, 2, 3, 4, 5)])
    rate_keyboard.add(
        *[tb.types.InlineKeyboardButton(text=name,
                                        callback_data=name)
            for name in ['Связь', 'Статистика']])
    try:
        bot.edit_message_text(answer, call_back.message.chat.id,
                              call_back.message.message_id,
                              parse_mode='HTML',
                              disable_web_page_preview=True,
                              reply_markup=rate_keyboard)
    except tb.apihelper.ApiException:
        pass
    func.call_back_log_me(call_back)


@bot.callback_query_handler(func=lambda call_back: call_back.data)
def callback_query_text_handler(call_back):
    answer = 'Не понимаю\nИспользуй /help для просмотра всех команд'
    bot.edit_message_text(answer, call_back.message.chat.id,
                          call_back.message.message_id)
    func.call_back_log_me(call_back)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if str(message.chat.id) == conf.my_id:
        if message.text.split()[0].isdigit():
            text = message.text.split()
            chat_id = text[0]
            if chat_id.isdigit():
                message_text = message.text[len(chat_id):]
                try:
                    bot.send_message(chat_id, message_text,
                                     True, parse_mode='HTML')
                    if message.content_type != message_text:
                        bot.send_message(
                            message.chat.id, const.emoji['check_mark'])
                except Exception as err:
                    bot.send_message(message.chat.id, const.emoji[
                                     'cross_mark'] + '\n' + str(err))
        elif message.text[:3].lower() == 'ban' and message.text[3:].replace(' ', '') != conf.my_id:
            try:
                if func.is_user_not_banned(int(message.text[3:])):

                    func.ban_user(int(message.text[3:]))

                    remove_keyboard = tb.types.ReplyKeyboardRemove()
                    bot.send_message(int(message.text[3:]), const.emoji['cross_mark'] + ' Заблокирован',
                                     reply_markup=remove_keyboard)

                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                else:
                    bot.send_message(
                        message.chat.id, const.emoji['cross_mark'])
            except:
                bot.send_message(message.chat.id, const.emoji['cross_mark'])
                bot.send_message(message.chat.id, exc_info()[1])
        elif message.text[:5].lower() == 'unban':
            try:
                if func.is_user_banned(int(message.text[5:])):

                    func.unban_user(int(message.text[5:]))

                    bot.send_message(int(message.text[5:]), const.emoji['check_mark'] + ' Разблокирован',
                                     reply_markup=main_keyboard(message.chat.id))

                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                else:
                    bot.send_message(
                        message.chat.id, const.emoji['cross_mark'])
            except:
                bot.send_message(message.chat.id, const.emoji['cross_mark'])
                bot.send_message(message.chat.id, exc_info()[1])
        elif message.text.lower() == 'up':
            func.edit_week(True)
            bot.send_message(message.chat.id, const.emoji['check_mark'])
        elif message.text.lower() == 'down':
            func.edit_week(False)
            bot.send_message(message.chat.id, const.emoji['check_mark'])
        elif message.text.lower() == 'onlog':
            func.edit_sending_log(True)
            if func.get_sending_log() == 'ON':
                bot.send_message(message.chat.id, const.emoji['check_mark'])
            else:
                bot.send_message(message.chat.id, const.emoji['cross_mark'])
        elif message.text.lower() == 'offlog':
            func.edit_sending_log(False)
            if func.get_sending_log() == 'OFF':
                bot.send_message(message.chat.id, const.emoji['check_mark'])
            else:
                bot.send_message(message.chat.id, const.emoji['cross_mark'])
        elif message.text.lower() == 'online':
            func.edit_on_or_off_zam(True)
            if func.get_on_or_off_zam() == 'ONLINE':
                bot.send_message(message.chat.id, const.emoji['check_mark'])
            else:
                bot.send_message(message.chat.id, const.emoji['cross_mark'])
        elif message.text.lower() == 'offline':
            func.edit_on_or_off_zam(False)
            if func.get_on_or_off_zam() == 'OFFLINE':
                bot.send_message(message.chat.id, const.emoji['check_mark'])
            else:
                bot.send_message(message.chat.id, const.emoji['cross_mark'])
        elif message.text[:2].lower() == 're':
            try:
                if message.text.lower().replace(' ', '') == 'res':
                    func.rewrite_zam_data(
                        's', func.get_html(func.pay_url('s'), message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                elif message.text.lower().replace(' ', '') == 'rez':
                    func.rewrite_zam_data(
                        'z', func.get_html(func.pay_url('z'), message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                elif message.text.lower().replace(' ', '') == 'reall':
                    func.rewrite_zam_data('all')
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])

                elif int(message.text[2:]) == 1:
                    func.rewrite_zam_data(
                        1, func.get_html(const.ponedelnik, message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                elif int(message.text[2:]) == 2:
                    func.rewrite_zam_data(
                        2, func.get_html(const.vtornik, message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                elif int(message.text[2:]) == 3:
                    func.rewrite_zam_data(
                        3, func.get_html(const.sreda, message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                elif int(message.text[2:]) == 4:
                    func.rewrite_zam_data(
                        4, func.get_html(const.chetverg, message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                elif int(message.text[2:]) == 5:
                    func.rewrite_zam_data(
                        5, func.get_html(const.pyatnica, message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                elif int(message.text[2:]) == 6:
                    func.rewrite_zam_data(
                        6, func.get_html(const.subotta, message.chat.id))
                    bot.send_message(
                        message.chat.id, const.emoji['check_mark'])
                else:
                    bot.send_message(
                        message.chat.id, const.emoji['cross_mark'])
            except:
                bot.send_message(message.chat.id, str(datetime.now())[
                                 :-7] + ' | ' + str(exc_info()[1]))
        elif message.text[:2].lower() == 'pd':
            try:
                sql_con = connect(const.path + 'Parse.db')
                cursor = sql_con.cursor()
                cursor.execute('''UPDATE parsing_days
                                     SET pro_parsing_day = ?''', (int(message.text[2:]),))
                sql_con.commit()
                cursor.close()
                sql_con.close()
                bot.send_message(message.chat.id, const.emoji['check_mark'])
            except:
                bot.send_message(message.chat.id, str(datetime.now())[
                                 :-7] + ' | ' + str(exc_info()[1]))
        elif message.text.split()[0] in const.existing_groups:
            try:
                sql_con = connect(const.path + 'Bot.db')
                cursor = sql_con.cursor()
                cursor.execute('''SELECT id
                                    FROM user_data
                                   WHERE group_name = ?''', (message.text.split()[0],))
                send_ids = cursor.fetchall()
                cursor.close()
                sql_con.close()
                if send_ids:
                    if message.text.split()[1].lower() == 'len':
                        bot.send_message(message.chat.id, len(send_ids))
                    else:
                        sql_con = connect(const.path + 'Bot.db')
                        cursor = sql_con.cursor()
                        cursor.execute('''SELECT id_not_banned
                                            FROM banned_users''')
                        not_banned_users = cursor.fetchall()
                        cursor.close()
                        sql_con.close()

                        for si in send_ids:
                            if si in not_banned_users:
                                try:
                                    if str(si[0]).isdigit():
                                        bot.send_message(si[0], message.text[len(message.text.split()[0]):], True,
                                                         parse_mode='HTML')
                                except Exception as err:
                                    bot.send_message(message.chat.id, const.emoji[
                                                     'cross_mark'] + ' ' + str(si[0]) + '\n' + str(err))
                                    continue
                                sleep(0.04)
                        bot.send_message(
                            message.chat.id, const.emoji['check_mark'])
                else:
                    bot.send_message(
                        message.chat.id, const.emoji['cross_mark'])
            except:
                bot.send_message(message.chat.id, const.emoji['cross_mark'])
    else:

        answer = 'Не понимаю\nИспользуй /help для просмотра всех команд'
        bot.send_message(message.chat.id, answer)
    func.log_me(message)


if __name__ == '__main__':
    print('\n' + str(datetime.now())[:-7] + ' | ' + str(bot.get_me()) + '\n')
    bot.send_message(conf.my_id,
                     str(datetime.now())[:-7] + ' | ' + str(bot.get_me()))

    bot.remove_webhook()

    if 'generic' in uname()[2]:
        bot.polling(none_stop=True, interval=0)
    else:
        bot.set_webhook(url=conf.WEBHOOK_URL_BASE + conf.WEBHOOK_URL_PATH,
                        certificate=open(conf.WEBHOOK_SSL_CERT, 'r'))

        cherrypy.config.update({
            'server.socket_host': conf.WEBHOOK_LISTEN,
            'server.socket_port': conf.WEBHOOK_PORT,
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': conf.WEBHOOK_SSL_CERT,
            'server.ssl_private_key': conf.WEBHOOK_SSL_PRIV
        })

        cherrypy.quickstart(WebhookServer(), conf.WEBHOOK_URL_PATH, {'/': {}})
