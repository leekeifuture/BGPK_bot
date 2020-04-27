# -*- coding: utf-8 -*-
# !/usr/bin/python3.6


import json
import re
import sqlite3 as sl3
from collections import Counter
from datetime import datetime

from bs4 import BeautifulSoup

import constants as const
from telebot import types


def set_next_step(user_id, next_step):
    sql_con = sl3.connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''UPDATE user_choice
                         SET step = ?
                       WHERE user_id = ?''', (next_step, user_id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()


def get_step(user_id):
    sql_con = sl3.connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT step
                        FROM user_choice
                       WHERE user_id = ?''', (user_id,))
    step = cursor.fetchone()
    cursor.close()
    sql_con.close()
    if step is None:
        return False
    else:
        return step[0]


def regex_matches(query):
    return re.match(const.pattern,
                    re.sub(const.sub_pattern, '',
                           query.replace('ё', 'е').replace(' ', '').lower()))


def check_teacher(teacher_names, full_teachers_name):
    names = []
    checked_indexes = []
    pre_checked_indexes = []
    teachers = const.existing_teachers.copy()

    for teacher in teacher_names:
        for i in const.cap_teachers:
            if teacher == i:
                index = const.cap_teachers.index(i)

                if const.teacher_name[index] not in names:
                    names.append(const.teacher_name[index])
                    pre_checked_indexes.append(index)

    checked_names = []

    not_in_shedule = []

    for name in names:
        if name in teachers:
            if name not in checked_names:
                checked_names.append(name)
                checked_indexes.append(pre_checked_indexes[names.index(name)])
        elif name not in not_in_shedule:
            not_in_shedule.append(name)

    if not_in_shedule:
        db_teachers = []

        for i in range(1, 7):
            sql_con = sl3.connect(const.path + 'Parse.db')
            cursor = sql_con.cursor()
            cursor.execute('''SELECT day_{0}
                                FROM zam_from_site'''.format(str(i)))
            data = cursor.fetchone()[0].split('][')
            cursor.close()
            sql_con.close()

            soup = BeautifulSoup(data[1], 'lxml')

            for tab in soup.find_all('table'):
                for row in tab.find_all('tr')[1:]:
                    if 'strong' in str(row):
                        continue
                    tmp = row.find_all('td')
                    teacher = tmp[4].text.strip().replace('\n', '')

                    if teacher not in db_teachers:
                        db_teachers.append(teacher)

        for ir in range(len(db_teachers)):
            for i in db_teachers:
                if '/' in i.replace(' ', ''):
                    index = db_teachers.index(i)
                    db_teachers.remove(db_teachers[index])
                    ready = i.split('/')
                    for i1 in ready:
                        if i1:
                            if i1.strip() not in db_teachers:
                                db_teachers.append(i1.strip())

        surnames = []

        for i in db_teachers:
            if i:
                short_name = i.replace(' ', '').replace('.', '').lower()

                if short_name == 'панасюксс':
                    surname = short_name
                elif short_name == 'панасюксвсв':
                    surname = short_name
                elif short_name == 'панасюквв':
                    surname = short_name
                elif short_name == 'носовасп':
                    surname = short_name
                elif short_name == 'носовата':
                    surname = short_name
                elif short_name == 'панасюкдю':
                    surname = short_name
                else:
                    surname = (i.split()[0].replace(' ', '')
                               .replace('.', '')
                               .lower().replace('ё', 'е'))

                surnames.append(surname)

        for i in not_in_shedule:
            if i:
                short_name = i.replace(' ', '').replace('.', '').lower()

                if short_name == 'панасюксергейстепанович':
                    surname = 'панасюксс'
                elif short_name == 'панасюксветланасвятославовна':
                    surname = 'панасюксвсв'
                elif short_name == 'панасюквикторвладимирович':
                    surname = 'панасюквв'
                elif short_name == 'носовасветланапетровна':
                    surname = 'носовасп'
                elif short_name == 'носовататьянаалександровна':
                    surname = 'носовата'
                elif short_name == 'панасюкдианаюрьевна':
                    surname = 'панасюкдю'
                else:
                    surname = i.split()[0].replace(
                        ' ', '').replace('.', '').lower()

                if surname in surnames:
                    if i not in checked_names:
                        checked_names.append(i)
                        checked_indexes.append(const.teacher_name.index(i))

    if len(checked_names) == 1:
        index = const.teacher_name.index(checked_names[0])
        return [const.cap_teachers[index]], checked_indexes
    else:
        if full_teachers_name:
            checked_teachers = []
            indexes = []

            for name in checked_names:
                index = const.teacher_name.index(name)
                checked_teachers.append(const.cap_teachers[index])
                indexes.append(index)
            return checked_teachers, indexes

    return checked_names, checked_indexes


def search_teacher(name_for_search, dot_except=False):
    matches = regex_matches(name_for_search)

    if matches != None:
        teacher_name = matches.group()
    else:
        return []

    teachers = []

    startswith_list = []
    for i in const.low_teachers:
        if i.startswith(teacher_name):
            index = const.low_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            startswith_list.append(full_teacher_name)
    startswith_list.sort()
    for i in startswith_list:
        if i not in teachers:
            teachers.append(i)
    first_name_lsit = []
    second_name_lsit = []
    for i in const.cap_teachers:
        splited = i.split()
        if splited[1].lower().startswith(teacher_name):
            index = const.cap_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            if full_teacher_name not in first_name_lsit:
                first_name_lsit.append(full_teacher_name)
        if splited[2].lower().startswith(teacher_name):
            index = const.cap_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            if full_teacher_name not in second_name_lsit:
                second_name_lsit.append(full_teacher_name)
    first_name_lsit.sort()
    for i in first_name_lsit:
        if i not in teachers:
            teachers.append(i)
    second_name_lsit.sort()
    for i in second_name_lsit:
        if i not in teachers:
            teachers.append(i)
    existing_list = []
    for i in const.low_teachers:
        if teacher_name in i:
            index = const.low_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            if full_teacher_name not in existing_list:
                existing_list.append(full_teacher_name)
    existing_list.sort()
    for i in existing_list:
        if i not in teachers:
            teachers.append(i)

    return check_teacher(teachers, dot_except)


def select_status(message, change_group=False):
    from flask_app import bot

    answer = ''

    sql_con = sl3.connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT types_json
                        FROM user_choice
                       WHERE user_id = ?''', (message.chat.id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()

    types_of_reg = json.loads(data[0])
    type_names = [type['Type'] for type in types_of_reg]
    aliases = [type['Alias'] for type in types_of_reg]

    if message.text == type_names[0]:
        answer = ''

        answer += 'Укажи свое направление:'
        divisions_keyboard = types.ReplyKeyboardMarkup(True, False)
        for division_name in const.existing_divisions:
            divisions_keyboard.row(division_name)
        if change_group:
            divisions_keyboard.row('« Назад')
        else:
            divisions_keyboard.row('Другой способ регистрации')
        data = json.dumps(const.divisions, ensure_ascii=False)

        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE user_choice
                             SET divisions_json = ?
                           WHERE user_id = ?''', (data, message.chat.id,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        bot.send_message(message.chat.id, answer,
                         reply_markup=divisions_keyboard)
        set_next_step(message.chat.id, 'select_division')
    elif message.text == type_names[1]:
        if change_group:
            back_command = ''
        else:
            back_command = '\n\nДля отмены используй /home'

        answer += ('Введи <i>Фамилию</i> преподавателя (и <i>И. О.</i>)\n'
                   'Это можно сделать <b>двумя</b> способами:\n'
                   '{0} <b>Прислать ФИО преподавателя (бот поддерживает 3 вида):</b>\n'
                   '      1) <i>Фамилия</i>\n'
                   '      2) <i>Фамилия И. О.</i>\n'
                   '      3) <i>Фамилия Имя Отчество</i>\n'
                   '{1} <b>Воспользоваться динамичным поиском:</b>\n'
                   '      Для этого введи "<code>@BGPK_bot </code>" и следуй дальнейшим '
                   'инструкциям.{2}'.format(const.emoji['bullet'],
                                            const.emoji['bullet'],
                                            back_command))
        remove_keyboard = types.ReplyKeyboardRemove()

        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE user_choice
                             SET alias = ?
                           WHERE user_id = ?''',
                       (aliases[1], message.chat.id,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        bot.send_message(message.chat.id, answer,
                         reply_markup=remove_keyboard,
                         parse_mode='HTML')
        set_next_step(message.chat.id, 'select_teacher')
    else:
        answer += 'Пожалуйста, выбери в качестве кого ты хочешь зайти:'
        bot.send_message(message.chat.id, answer)
        set_next_step(message.chat.id, 'select_status')


def select_teacher(message):
    from flask_app import bot

    answer = ''

    if message.text in const.cap_teachers:
        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE user_choice
                             SET student_group_name = ?
                           WHERE user_id = ?''',
                       (message.text, message.chat.id,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        text = '>> ' + message.text
        answer += 'Подтверди выбор преподавателя:\n' + '<b>' + text + '</b>'
        choice_keyboard = types.ReplyKeyboardMarkup(True, False)
        buttons = ['Все верно',
                   'Другой преподаватель',
                   'Другой способ регистрации']
        for button in buttons:
            choice_keyboard.row(button)
        bot.send_message(message.chat.id, answer,
                         parse_mode='HTML',
                         reply_markup=choice_keyboard)
        set_next_step(message.chat.id, 'confirm_choice_teacher')
    else:
        teachers = search_teacher(message.text)

        if len(teachers) == 0:
            answer += ('Преподаватель "<b>' + message.text + '</b>" '
                                                             'не найден.\nЕсли по какой-то причине отсусвует '
                                                             'какой либо преподаватель, просьба сразу сообщить '
                                                             '<a href="https://t.me/lee_kei">разработчику</a>.')

            bot.send_message(message.chat.id, answer, True,
                             parse_mode='HTML')
            return

        if teachers[0] and len(teachers[0]) <= 10:
            short_teachers = []
            if len(teachers[0]) > 1:
                for teacher in teachers[0]:
                    sp_te = teacher.split()
                    short_teachers.append(sp_te[0] + ' ' +
                                          sp_te[1][0] + '. ' +
                                          sp_te[2][0] + '.')

                duplicate = [item for item, count in Counter(
                    short_teachers).items() if count > 1]
                if duplicate:
                    seen = set()
                    result = []
                    for idx, item in enumerate(short_teachers):
                        if item not in seen:
                            seen.add(item)
                        else:
                            result.append(idx)

                    for i in duplicate:
                        index = short_teachers.index(i)
                        for ind in result:
                            if short_teachers[index] == short_teachers[ind]:
                                sp_te = teachers[0][ind].split()
                                short_teachers[ind] = (
                                        sp_te[0] + ' ' +
                                        sp_te[1][:2] + '. ' +
                                        sp_te[2][:2] + '.')
                        sp_te = teachers[0][index].split()
                        short_teachers[index] = (
                                sp_te[0] + ' ' +
                                sp_te[1][:2] + '. ' +
                                sp_te[2][:2] + '.')
            else:
                short_teachers = teachers[0]

            educators_keyboard = types.InlineKeyboardMarkup(
                row_width=2)

            if len(short_teachers) == 1:
                answer += (const.emoji['mag_right'] +
                           ' Найденный преподаватель:')
                if len(short_teachers[0].encode('utf-8')) >= 48:
                    if short_teachers[0] in const.teacher_name:
                        index = const.teacher_name.index(short_teachers[0])
                    elif short_teachers[0] in const.sht_teachers:
                        index = const.sht_teachers.index(short_teachers[0])
                    elif short_teachers[0] in const.cap_teachers:
                        index = const.cap_teachers.index(short_teachers[0])
                    short_teachers[0] = const.teacher_name[index]
            else:
                answer += (const.emoji['mag_right'] +
                           ' Найденные преподаватели:')

            educators = []
            i = 0
            for teacher in short_teachers:
                try:
                    educators.append(types.InlineKeyboardButton(
                        text=teacher,
                        callback_data=teacher + '|' + str(teachers[1][i])))
                    i += 1
                except:
                    continue
            educators_keyboard.add(*educators)
            educators_keyboard.row(types.InlineKeyboardButton(
                text='« Назад', callback_data='back_reg'))

            bot.send_message(message.chat.id, answer,
                             reply_markup=educators_keyboard)
        elif len(teachers[0]) > 10:
            answer += ('Слишком много преподавателей\n'
                       'Пожалуйста, <b>уточни</b>')

            bot.send_message(message.chat.id, answer,
                             parse_mode='HTML')
        else:
            if ('Никого не найдено' not in message.text and
                    'Введи ФИО преподавателя' not in message.text and
                    'Слишком много преподавателей' not in message.text):
                answer += ('Преподаватель "<b>' + message.text + '</b>" '
                                                                 'не найден.\nЕсли по какой-то причине отсусвует '
                                                                 'какой либо преподаватель, просьба сразу сообщить '
                                                                 '<a href="https://t.me/lee_kei">разработчику</a>.')

                bot.send_message(message.chat.id, answer, True,
                                 parse_mode='HTML')


def select_division(message):
    from flask_app import bot, start_handler

    answer = ''

    sql_con = sl3.connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT divisions_json
                        FROM user_choice
                       WHERE user_id = ?''', (message.chat.id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()

    divisions = json.loads(data[0])
    aliases = [division['Alias'] for division in divisions]
    if message.text in const.existing_divisions:
        answer += 'Выбери курс:'
        study_programs_keyboard = types.ReplyKeyboardMarkup(
            True, False)
        index = const.existing_divisions.index(message.text)
        alias = aliases[index]

        for study_program in const.existing_courses:
            study_programs_keyboard.row(study_program)
        study_programs_keyboard.row('Другое направление')

        data = json.dumps(const.courses, ensure_ascii=False)
        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE user_choice
                             SET div_alias = ?,
                                 division_name = ?,
                                 study_programs_json = ?
                           WHERE user_id = ?''',
                       (alias, message.text, data, message.chat.id,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        bot.send_message(message.chat.id, answer,
                         reply_markup=study_programs_keyboard)
        set_next_step(message.chat.id, 'select_admission_year')
    elif message.text == 'Другой способ регистрации':
        start_handler(message)
        return
    else:
        answer += 'Пожалуйста, укажи направление:'
        bot.send_message(message.chat.id, answer)
        set_next_step(message.chat.id, 'select_division')


def select_admission_year(message):
    from flask_app import bot

    answer = ''

    sql_con = sl3.connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT study_programs_json, div_alias
                        FROM user_choice
                       WHERE user_id = ?''', (message.chat.id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()

    courses = json.loads(data[0])
    div_alias = data[1]

    aliases = [course['Alias'] for course in courses]
    if message.text in const.existing_courses:
        answer += 'Укажи группу:'
        student_groups_keyboard = types.ReplyKeyboardMarkup(True, False)
        index = const.existing_courses.index(message.text)
        course_alias = aliases[index]

        alias = div_alias + course_alias
        student_group_names = []
        for i in const.student_groups:
            if alias in i:
                gr = i[alias]
                for student_group in gr:
                    student_group_names.append(
                        student_group['StudentGroupName'])
        student_groups_keyboard = types.ReplyKeyboardMarkup(
            True, False)
        for student_group_name in student_group_names:
            student_groups_keyboard.row(student_group_name)
        student_groups_keyboard.row('Другой курс')
        data = json.dumps(const.student_groups, ensure_ascii=False)

        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE user_choice
                             SET alias = ?, admission_year_name = ?,
                                 student_groups_json = ?
                           WHERE user_id = ?''',
                       (alias, message.text, data, message.chat.id,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        bot.send_message(message.chat.id, answer,
                         reply_markup=student_groups_keyboard)
        set_next_step(message.chat.id, 'select_student_group')
    elif message.text == 'Другое направление':
        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT types_json
                            FROM user_choice
                           WHERE user_id = ?''', (message.chat.id,))
        data = cursor.fetchone()[0]
        cursor.close()
        sql_con.close()

        message.text = json.loads(data)[0]['Type']
        select_status(message)
        return

    else:
        answer += 'Пожалуйста, укажи курс:'
        bot.send_message(message.chat.id, answer)
        set_next_step(message.chat.id, 'select_admission_year')


def select_student_group(message):
    from flask_app import bot

    answer = ''

    sql_con = sl3.connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT student_groups_json, alias
                        FROM user_choice
                       WHERE user_id = ?''', (message.chat.id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()

    student_groups = json.loads(data[0])
    alias = data[1]
    student_group_names = []
    for i in student_groups:
        if alias in i:
            gr = i[alias]
            for student_group in gr:
                student_group_names.append(student_group['StudentGroupName'])
    if message.text in student_group_names:
        edit_msg = bot.send_message(message.chat.id,
                                    'Почти готово! '
                                    'Запоминаю твой выбор\U00002026')

        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE user_choice
                             SET student_group_name = ?
                           WHERE user_id = ?''',
                       (message.text, message.chat.id,))
        sql_con.commit()
        cursor.execute('''SELECT division_name,
                                 admission_year_name,
                                 student_group_name
                            FROM user_choice
                           WHERE user_id = ?''', (message.chat.id,))
        data = cursor.fetchone()
        cursor.close()
        sql_con.close()

        text = '>> ' + '\n>> '.join(data)
        answer += 'Подтверди выбор:\n' + '<b>' + text + '</b>'
        choice_keyboard = types.ReplyKeyboardMarkup(True, False)
        buttons = ['Все верно',
                   'Другая группа',
                   'Другой курс',
                   'Другое направление',
                   'Другой способ регистрации']
        for button in buttons:
            choice_keyboard.row(button)
        bot.edit_message_text('Готово!',
                              message.chat.id,
                              edit_msg.message_id)
        bot.send_message(message.chat.id, answer,
                         parse_mode='HTML',
                         reply_markup=choice_keyboard)
        set_next_step(message.chat.id, 'confirm_choice')
    elif message.text == 'Другой курс':
        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT division_name
                            FROM user_choice
                           WHERE user_id = ?''', (message.chat.id,))
        data = cursor.fetchone()
        cursor.close()
        sql_con.close()

        message.text = data[0]
        select_division(message)
        return
    else:
        answer += 'Пожалуйста, укажи группу:'
        bot.send_message(message.chat.id, answer)
        set_next_step(message.chat.id, 'select_student_group')


def confirm_choice_teacher(message):
    from flask_app import bot, start_handler, main_keyboard

    answer = ''

    if message.text == 'Все верно':
        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT alias, student_group_name
                            FROM user_choice
                           WHERE user_id = ?''', (message.chat.id,))
        data = cursor.fetchone()
        alias = data[0]
        group_name = data[1]
        cursor.execute('''DELETE FROM banned_users
                                WHERE id_not_banned = ?''', (message.chat.id,))
        sql_con.commit()
        cursor.execute('''INSERT INTO banned_users (id_not_banned)
                               VALUES (?)''', (message.chat.id,))
        sql_con.commit()

        try:
            cursor.execute('''INSERT INTO user_data (id,
                                                     first_name,
                                                     last_name,
                                                     username,
                                                     alias,
                                                     group_name,
                                                     date_of_registrations)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (message.chat.id,
                            message.chat.first_name,
                            message.chat.last_name,
                            message.chat.username,
                            alias, group_name,
                            str(datetime.now())[:-7],))
        except sl3.IntegrityError:
            sql_con.rollback()
            cursor.execute('''UPDATE user_data
                                 SET alias = ?, group_name = ?
                               WHERE id = ?''',
                           (alias, group_name, message.chat.id,))
        finally:
            sql_con.commit()
            cursor.execute('''DELETE FROM user_choice
                                    WHERE user_id = ?''',
                           (message.chat.id,))
            sql_con.commit()
            cursor.close()
            sql_con.close()

        answer = ('Главное меню\n\n'
                  '{0} – информация о боте\n'
                  '{1} – оценить бота\n'
                  '{2} – настройки\n'
                  '{3} – параметры уведомлений\n'
                  '{4} – расписание звонков'.format(const.emoji['info'],
                                                    const.emoji['star'],
                                                    const.emoji['settings'],
                                                    const.emoji['alarm_clock'],
                                                    const.emoji['bell']))

        bot.send_message(message.chat.id, answer,
                         reply_markup=main_keyboard(message.chat.id),
                         parse_mode='HTML')
    elif message.text == 'Другой преподаватель':
        message.text = 'Преподаватель'
        select_status(message)
        return
    elif message.text == 'Другой способ регистрации':
        start_handler(message)
        return
    else:
        answer += ('Пожалуйста, проверь правильно ли ты всё указал и '
                   'подтверди свой выбор:')
        bot.send_message(message.chat.id, answer)
        set_next_step(message.chat.id, 'confirm_choice_teacher')


def confirm_choice(message):
    from flask_app import bot, start_handler, main_keyboard

    answer = ''

    if message.text == 'Все верно':
        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT alias, student_group_name
                            FROM user_choice
                           WHERE user_id = ?''', (message.chat.id,))
        data = cursor.fetchone()
        alias = data[0]
        group_name = data[1]
        cursor.execute('''DELETE FROM banned_users
                                WHERE id_not_banned = ?''', (message.chat.id,))
        sql_con.commit()
        cursor.execute('''INSERT INTO banned_users (id_not_banned)
                               VALUES (?)''', (message.chat.id,))
        sql_con.commit()

        try:
            cursor.execute('''INSERT INTO user_data (id,
                                                     first_name,
                                                     last_name,
                                                     username,
                                                     alias,
                                                     group_name,
                                                     date_of_registrations)
                                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (message.chat.id,
                            message.chat.first_name,
                            message.chat.last_name,
                            message.chat.username,
                            alias, group_name,
                            str(datetime.now())[:-7],))
        except sl3.IntegrityError:
            sql_con.rollback()
            cursor.execute('''UPDATE user_data
                                 SET alias = ?, group_name = ?
                               WHERE id = ?''',
                           (alias, group_name, message.chat.id,))
        finally:
            sql_con.commit()
            cursor.execute('''DELETE FROM user_choice
                                    WHERE user_id = ?''',
                           (message.chat.id,))
            sql_con.commit()
            cursor.close()
            sql_con.close()

        answer = ('Главное меню\n\n'
                  '{0} – информация о боте\n'
                  '{1} – оценить бота\n'
                  '{2} – настройки\n'
                  '{3} – параметры уведомлений\n'
                  '{4} – расписание звонков'.format(const.emoji['info'],
                                                    const.emoji['star'],
                                                    const.emoji['settings'],
                                                    const.emoji['alarm_clock'],
                                                    const.emoji['bell']))

        bot.send_message(message.chat.id, answer,
                         reply_markup=main_keyboard(message.chat.id),
                         parse_mode='HTML')
    elif message.text == 'Другая группа':
        sql_con = sl3.connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT admission_year_name
                            FROM user_choice
                           WHERE user_id = ?''', (message.chat.id,))
        data = cursor.fetchone()
        cursor.close()
        sql_con.close()

        message.text = data[0]
        select_admission_year(message)
        return
    elif message.text == 'Другой курс':
        select_student_group(message)
        return
    elif message.text == 'Другое направление':
        select_admission_year(message)
        return
    elif message.text == 'Другой способ регистрации':
        start_handler(message)
        return
    else:
        answer += ('Пожалуйста, проверь правильно ли ты всё указал и '
                   'подтверди свой выбор:')
        bot.send_message(message.chat.id, answer)
        set_next_step(message.chat.id, 'confirm_choice')
