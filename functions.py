# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import re
import telebot as tb
import datetime as dt
from json import loads
from config import my_id
from sys import exc_info
import constants as const
from flask_app import bot
from sqlite3 import connect
from bs4 import BeautifulSoup
from collections import Counter
from urllib.request import urlopen


def sql_select(db_name, fetch, request, *args):
    sql_con = connect(const.path + db_name)
    cursor = sql_con.cursor()

    if args:
        cursor.execute(request, args)
    else:
        cursor.execute(request)

    if fetch == 'one':
        data = cursor.fetchone()[0]
    elif fetch == 'all':
        data = cursor.fetchall()

    cursor.close()
    sql_con.close()
    return data


def sql_execute(db_name, request, *args):
    sql_con = connect(const.path + db_name)
    cursor = sql_con.cursor()

    if args:
        cursor.execute(request, args)
    else:
        cursor.execute(request)

    sql_con.commit()
    cursor.close()
    sql_con.close()


def log_me(message):
    if str(message.chat.id) != my_id:

        sql_con = connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT sending_log
                            FROM offer''')
        send = cursor.fetchone()[0]
        cursor.close()
        sql_con.close()
        if send:
            if message.chat.username != None:
                message.chat.username = ('https://t.me/' +
                                         str(message.chat.username))
            else:
                message.chat.username = '#'
            bot.send_message(my_id,
                             str('\n{4} | <a href="{7}">{0} '
                                 '{1}</a> | <b>{5}</b> ({2}) {6} :\n{3}'
                                 .format(message.chat.first_name,
                                         message.chat.last_name,
                                         str(message.chat.id),
                                         message.text,
                                         str(dt.datetime.now())[:-7],
                                         get_student_group(message.chat.id),
                                         message.message_id,
                                         message.chat.username)), True,
                             parse_mode='HTML',
                             disable_notification=True)


def call_back_log_me(call_back):
    if str(call_back.message.chat.id) != my_id:

        sql_con = connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT sending_log
                            FROM offer''')
        send = cursor.fetchone()[0]
        cursor.close()
        sql_con.close()
        if send:
            if call_back.message.chat.username != None:
                call_back.message.chat.username = ('https://t.me/' +
                                                   str(call_back.message.chat.username))
            else:
                call_back.message.chat.username = '#'
            bot.send_message(my_id,
                             str('\n{4} | <a href="{7}">{0} '
                                 '{1}</a> | <b>{5}</b> ({2}) {6} :\n{3}'
                                 .format(call_back.message.chat.first_name,
                                         call_back.message.chat.last_name,
                                         str(call_back.message.chat.id),
                                         call_back.data,
                                         str(dt.datetime.now())[:-7],
                                         get_student_group(
                                             call_back.message.chat.id),
                                         call_back.message.message_id,
                                         call_back.message.chat.username)), True,
                             parse_mode='HTML',
                             disable_notification=True)


def inline_log_me(query):
    if str(query.from_user.id) != my_id:

        sql_con = connect(const.path + 'Bot.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT sending_log
                            FROM offer''')
        send = cursor.fetchone()[0]
        cursor.close()
        sql_con.close()
        if send:
            if query.from_user.username != None:
                query.from_user.username = ('https://t.me/' +
                                            str(query.from_user.username))
            else:
                query.from_user.username = '#'
            bot.send_message(my_id,
                             str('\n{4} | <a href="{7}">{0} '
                                 '{1}</a> | <b>{5}</b> ({2}) {6} :\n{3}'
                                 .format(query.from_user.first_name,
                                         query.from_user.last_name,
                                         str(query.from_user.id),
                                         query.query,
                                         str(dt.datetime.now())[:-7],
                                         get_student_group(query.from_user.id),
                                         query.id,
                                         query.from_user.username)), True,
                             parse_mode='HTML',
                             disable_notification=True)


def get_html(url, chat_id=my_id, printing=False):
    try:
        response = urlopen(url)
        return response.read()
    except:
        if printing:
            print('\n\n' + str(dt.datetime.now())[:-7] + ' | ' +
                  str(exc_info()[1]) + '\n\n')
        bot.send_message(chat_id,
                         '<b>Упс, что-то пошло не так\U00002026</b>\n' +
                         str(exc_info()[1]),
                         parse_mode='HTML')


def get_student_group(chat_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT group_name 
                        FROM user_data 
                       WHERE id = ?''', (chat_id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    try:
        return data[0]
    except:
        return ''


def day_of_week_parsing_day(request_day, parse_day=False, week=False):
    if week:
        if parse_day == dt.datetime.isoweekday(dt.datetime.now() + dt.timedelta(days=+1)):
            parse_date = str(dt.datetime.today() +
                             dt.timedelta(days=1))[:-16].split('-')
            if week == parse_date[2] + '.' + parse_date[1] + '.' + parse_date[0]:
                return 'завтра'
        elif parse_day == dt.datetime.isoweekday(dt.datetime.now()):
            parse_date = str(dt.datetime.today())[:-16].split('-')
            if week == parse_date[2] + '.' + parse_date[1] + '.' + parse_date[0]:
                return 'сегодня'
    else:
        if parse_day == dt.datetime.isoweekday(dt.datetime.now() + dt.timedelta(days=+1)):
            return 'завтра'
        elif parse_day == dt.datetime.isoweekday(dt.datetime.now()):
            return 'сегодня'
    if 'понедельник' in str(request_day).lower() or request_day == 1:
        return 'понедельник'
    elif 'вторник' in str(request_day).lower() or request_day == 2:
        return 'вторник'
    elif 'среда' in str(request_day).lower() or request_day == 3:
        return 'среду'
    elif 'четверг' in str(request_day).lower() or request_day == 4:
        return 'четверг'
    elif 'пятница' in str(request_day).lower() or request_day == 5:
        return 'пятницу'
    elif 'суббота' in str(request_day).lower() or request_day == 6:
        return 'субботу'


def get_replacements_ansewer(row, chat_id=False, force_teacher=False,
                             force_group=False):
    answer = ''

    tmp = row.find_all('td')
    grp = tmp[0].text.strip().replace('\n', '')
    zan = tmp[1].text.strip().replace('\n', '')
    zam = tmp[2].text.strip().replace('\n', '')
    bud = tmp[3].text.strip().replace('\n', '')
    teacher = tmp[4].text.strip().replace('\n', '')
    aud = tmp[5].text.strip().replace('\n', '')
    site_group = grp.lower().replace(' ', '')

    if chat_id:
        alias = get_alias(chat_id)
        group = get_student_group(chat_id).lower()
    elif force_teacher:
        alias = 'PREP'
        group = force_teacher.lower()
    elif force_group:
        alias = 'GROUP'
        group = force_group.lower()

    if zan == '3':
        ending = '-ей'
    else:
        ending = '-ой'

    if (aud.lower().replace(' ', '') == 'с/з' or
            aud.lower().replace(' ', '') == 'с\\з'):
        aud = ' в спортивном зале.'
    elif aud.lower().replace(' ', '') == 'чит.зал':
        aud = ' в читальном зале.'
    elif aud.lower().replace(' ', '') == '-':
        aud = '.'
    else:
        if '/' in aud:
            aud = ' в ' + aud + ' аудиториях.'
        else:
            aud = ' в ' + aud + ' аудитории.'

    if alias == 'PREP':
        if '/' in teacher.replace(' ', ''):
            site_teacher = teacher.split('/')
        else:
            site_teacher = [teacher]

        surnames = []

        for i in site_teacher:
            if i:
                short_name = i.replace(' ', '').replace('.', '').lower()

                if short_name == 'панасюксс':
                    surname = short_name
                elif short_name == 'панасюксвсв':
                    surname = short_name
                elif short_name == 'панасюквв':
                    surname = short_name
                else:
                    surname = (i.split()[0].replace(' ', '')
                               .replace('.', '').lower()
                               .replace('ё', 'е'))

                surnames.append(surname)

        short_name = group.replace(' ', '').replace('.', '')

        if short_name == 'панасюксергейстепанович':
            surname = 'панасюксс'
        elif short_name == 'панасюксветланасвятославовна':
            surname = 'панасюксвсв'
        elif short_name == 'панасюквикторвладимирович':
            surname = 'панасюквв'
        else:
            surname = group.split()[0].replace(' ', '').replace('.', '')

        del_repl = ('\nОтменяется ' + zan + ' пара — <b>' +
                    zam + '</b> (<i>' + teacher + '</i>) у группы <b>' +
                    grp + '</b>.')
        aud_repl = ('\nЗаменяется аудитория <b>' + zam +
                    '</b> на <b>' + bud + '</b>, ' + zan +
                    ending + ' парой у группы <b>' + grp + '</b>.')
        add_repl = ('\nДобавляется ' + zan + ' пара — <b>' +
                    bud + '</b> (<i>' + teacher + '</i>)' + aud[:-1] +
                    ' у группы <b>' + grp + '</b>.')
        rep_repl = ('\nЗаменяется ' + zan + ' пара (<b>' +
                    zam + '</b>) на <b>' + bud + '</b> (<i>' +
                    teacher + '</i>)' + aud[:-1] + ' у группы <b>' +
                    grp + '</b>.')

        if surname in surnames and (bud == '-' or bud == ''):
            if del_repl not in answer:
                answer += '\n' + del_repl
        elif surname in surnames and zam.isdigit():
            if aud_repl not in answer:
                answer += '\n' + aud_repl
        elif surname in surnames and (zam == '-' or zam == ''):
            if add_repl not in answer:
                answer += '\n' + add_repl
        elif surname in surnames:
            if rep_repl not in answer:
                answer += '\n' + rep_repl
    else:
        del_repl = ('\nОтменяется ' + zan + ' пара — <b>' +
                    zam + '</b> (<i>' + teacher + '</i>).')
        aud_repl = ('\nЗаменяется аудитория <b>' + zam +
                    '</b> на <b>' + bud + '</b>, ' + zan +
                    ending + ' парой.')
        add_repl = ('\nДобавляется ' + zan + ' пара — <b>' +
                    bud + '</b> (<i>' + teacher + '</i>)' + aud)
        rep_repl = ('\nЗаменяется ' + zan + ' пара (<b>' +
                    zam + '</b>) на <b>' + bud + '</b> (<i>' +
                    teacher + '</i>)' + aud)

    if group in site_group and (bud == '-' or bud == ''):
        if del_repl not in answer:
            answer += '\n' + del_repl
    elif group in site_group and zam.isdigit():
        if aud_repl not in answer:
            answer += '\n' + aud_repl
    elif group in site_group and (zam == '-' or zam == ''):
        if add_repl not in answer:
            answer += '\n' + add_repl
    elif group in site_group:
        if rep_repl not in answer:
            answer += '\n' + rep_repl

    return answer


def replacements_today(chat_id):
    week_day = dt.datetime.isoweekday(dt.datetime.now())

    if week_day == 7:
        day_number = 1
    else:
        day_number = week_day
    sql_con = connect(const.path + 'Parse.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT day_{} 
                        FROM zam_from_site'''.format(str(day_number)))
    cfone = cursor.fetchone()[0].split('][')
    cursor.close()
    sql_con.close()
    soup = BeautifulSoup(cfone[1], 'lxml')
    data = BeautifulSoup(cfone[0], 'lxml').find_all('h1')[0].text.strip()

    if week_day == 7 and data.replace(' ', '')[-10:][:2] != (dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%d')):
        if is_sending_zam_on(chat_id):
            bot.send_message(chat_id, const.emoji['sleep'] + ' Выходной\n\n' + const.emoji['clock'] + ' Замены на понедельник (' + (dt.datetime.strftime(dt.date.today() + dt.timedelta(
                days=1), '%d.%m.%Y')) + ') ещё не вывесили.\nБот пришлёт тебе информацию если что-нибудь будет известно о них.')
        else:
            bot.send_message(chat_id, const.emoji['sleep'] + ' Выходной\n\n' + const.emoji['clock'] + ' Замены на понедельник (' + (
                dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%d.%m.%Y')) + ') ещё не вывесили.')
    elif week_day != 7 and data.replace(' ', '')[-10:][:2] != (dt.datetime.strftime(dt.date.today(), '%d')):
        bot.send_message(chat_id, const.emoji['warning_sign'] + ' Замены на сегодня (' + (
            dt.datetime.strftime(dt.date.today(), '%d.%m.%Y')) + ') до сих пор не вывесили.')
    elif data.replace(' ', '')[-10:][:2] == (dt.datetime.strftime(dt.date.today(), '%d')) or data.replace(' ', '')[-10:][:2] == (dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%d')):
        answer = ''
        group = get_student_group(chat_id)
        if get_alias(chat_id) == 'PREP':
            index = const.cap_teachers.index(group)
            for_any = 'преподавателя'
            group = const.sht_teachers[index]
        else:
            for_any = 'группы'

        week_end = (const.emoji['sleep'] + ' Выходной\nЗамены на следующий день:'
                    '\n\n' + const.emoji['anticlockwise'])
        not_repl_on_monday = (' Для ' + for_any +
                              ' <b>{}</b> нет замен на понедельник ('.format(group) +
                              data[-10:] + ').')
        not_repl_on = (const.emoji['anticlockwise'] + ' Для ' + for_any +
                       ' <b>{}</b> нет замен на сегодня ('.format(group) +
                       data[-10:] + ').')

        for tab in soup.find_all('table'):
            for row in tab.find_all('tr')[1:]:
                if 'strong' in str(row):
                    continue

                answer += get_replacements_ansewer(row, chat_id)

            if answer:
                if week_day == 7:
                    answer = week_end + ' ' + data.capitalize() + answer
                else:
                    answer = (const.emoji['anticlockwise'] +
                              ' ' + data.capitalize() + answer)

                bot.send_message(chat_id, answer, parse_mode='HTML')
            else:
                if week_day == 7:
                    bot.send_message(chat_id, week_end +
                                     not_repl_on_monday, parse_mode='HTML')
                else:
                    bot.send_message(chat_id, not_repl_on, parse_mode='HTML')


def replacements_tomorrow(chat_id):
    week_day = dt.datetime.isoweekday(dt.datetime.now())

    if week_day == 6:
        day_number = 1
    else:
        day_number = dt.datetime.isoweekday(
            dt.datetime.now() + dt.timedelta(days=1))
    sql_con = connect(const.path + 'Parse.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT day_{} 
                        FROM zam_from_site'''.format(str(day_number)))
    cfone = cursor.fetchone()[0].split('][')
    cursor.close()
    sql_con.close()
    soup = BeautifulSoup(cfone[1], 'lxml')
    data = BeautifulSoup(cfone[0], 'lxml').find_all('h1')[0].text.strip()

    if week_day == 6 and data.replace(' ', '')[-10:][:2] != (dt.datetime.strftime(dt.date.today() + dt.timedelta(days=2), '%d')):
        if is_sending_zam_on(chat_id):
            bot.send_message(chat_id, const.emoji['sleep'] + ' Выходной\n\n' + const.emoji['clock'] + ' Замены на понедельник (' + (dt.datetime.strftime(dt.date.today() + dt.timedelta(
                days=2), '%d.%m.%Y')) + ') ещё не вывесили.\nБот пришлёт тебе информацию если что-нибудь будет известно о них.')
        else:
            bot.send_message(chat_id, const.emoji['sleep'] + ' Выходной\n\n' + const.emoji['clock'] + ' Замены на понедельник (' + (
                dt.datetime.strftime(dt.date.today() + dt.timedelta(days=2), '%d.%m.%Y')) + ') ещё не вывесили.')
    elif week_day != 6 and data.replace(' ', '')[-10:][:2] != (dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%d')):
        if is_sending_zam_on(chat_id):
            bot.send_message(chat_id, const.emoji['clock'] + ' Замены на завтра (' + (dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1),
                                                                                                           '%d.%m.%Y')) + ') ещё не вывесили.\nБот пришлёт тебе информацию если что-нибудь будет известно о них.')
        else:
            bot.send_message(chat_id, const.emoji['clock'] + ' Замены на завтра (' + (dt.datetime.strftime(
                dt.date.today() + dt.timedelta(days=1), '%d.%m.%Y')) + ') ещё не вывесили.')
    elif data.replace(' ', '')[-10:][:2] == (dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%d')) or data.replace(' ', '')[-10:][:2] == (dt.datetime.strftime(dt.date.today() + dt.timedelta(days=2), '%d')):
        answer = ''
        group = get_student_group(chat_id)
        if get_alias(chat_id) == 'PREP':
            index = const.cap_teachers.index(group)
            for_any = 'преподавателя'
            group = const.sht_teachers[index]
        else:
            for_any = 'группы'

        week_end = const.emoji['sleep'] + (' Выходной\nЗамены на следующий день:'
                                           '\n\n' + const.emoji['anticlockwise'])
        not_repl_on_monday = (' Для ' + for_any +
                              ' <b>{}</b> нет замен на понедельник ('.format(group) +
                              data[-10:] + ').')
        not_repl_on = (const.emoji['anticlockwise'] + ' Для ' + for_any +
                       ' <b>{}</b> нет замен на завтра ('.format(group) +
                       data[-10:] + ').')

        for tab in soup.find_all('table'):
            for row in tab.find_all('tr')[1:]:
                if 'strong' in str(row):
                    continue

                answer += get_replacements_ansewer(row, chat_id)

            if answer:
                if week_day == 6:
                    answer = week_end + ' ' + data.capitalize() + answer
                else:
                    answer = (const.emoji['anticlockwise'] +
                              ' ' + data.capitalize() + answer)

                bot.send_message(chat_id, answer, parse_mode='HTML')
            else:
                if week_day == 6:
                    bot.send_message(chat_id, week_end +
                                     not_repl_on_monday, parse_mode='HTML')
                else:
                    bot.send_message(chat_id, not_repl_on, parse_mode='HTML')


def get_replace_of_day(day, chat_id=False, is_week=False, force_teacher=False,
                       force_group=False):
    if day == 'Понедельник' or day == 1:
        day_number = 1
    elif day == 'Вторник' or day == 2:
        day_number = 2
    elif day == 'Среда' or day == 3:
        day_number = 3
    elif day == 'Четверг' or day == 4:
        day_number = 4
    elif day == 'Пятница' or day == 5:
        day_number = 5
    elif day == 'Суббота' or day == 6:
        day_number = 6

    sql_con = connect(const.path + 'Parse.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT day_{} 
                        FROM zam_from_site'''.format(str(day_number)))
    cfone = cursor.fetchone()[0].split('][')
    cursor.close()
    sql_con.close()

    soup = BeautifulSoup(cfone[1], 'lxml')
    data = BeautifulSoup(cfone[0], 'lxml').find_all('h1')[0].text.strip()

    answer = ''

    for tab in soup.find_all('table'):
        for row in tab.find_all('tr')[1:]:
            if 'strong' in str(row):
                continue

            if chat_id:
                answer += get_replacements_ansewer(row, chat_id)
            elif force_teacher:
                answer += get_replacements_ansewer(row,
                                                   force_teacher=force_teacher)
            elif force_group:
                answer += get_replacements_ansewer(row,
                                                   force_group=force_group)

        a = data[-10:].split('.')
        b = str(dt.datetime.today())[:-16].split('-')

        c = dt.datetime(int(a[2]), int(a[1]), int(a[0]))
        d = dt.datetime(int(b[0]), int(b[1]), int(b[2]))

        not_repl_on = const.emoji['anticlockwise'] + ' Нет замен на {} ('.format(
            day_of_week_parsing_day(day, day_number, data[-10:])) + data[-10:] + ').'

        if c < d:
            cd = str(c + dt.timedelta(days=7))[:10].split('-')
            not_noty = cd[2] + '.' + cd[1] + '.' + cd[0]
            day_of_parsing_week = day_of_week_parsing_day(day, day_number)

            previous_relp = const.emoji['warning_sign'] + ' Это предыдущие замены\U00002026\nЗамены на {} ({}) ещё не вывесили:\n\n'.format(
                day_of_parsing_week, not_noty)
            not_repl_yet_on = const.emoji['warning_sign'] + ' Замены на {} ({}) ещё не вывесили:\n\n'.format(
                day_of_parsing_week, not_noty)

            if answer:
                if is_week:
                    return not_repl_yet_on + const.emoji['anticlockwise'] + ' ' + data.capitalize() + answer
                else:
                    return previous_relp + const.emoji['anticlockwise'] + ' ' + data.capitalize() + answer
            else:
                if is_week:
                    return not_repl_yet_on + not_repl_on
                else:
                    return previous_relp + not_repl_on
        else:
            if answer:
                answer = (const.emoji['anticlockwise'] +
                          ' ' + data.capitalize() + answer)
                return answer
            else:
                return not_repl_on


def get_active_replace_days(chat_id=False, force_teacher=False,
                            force_group=False):
    active_days = []
    if chat_id:
        alias = get_alias(chat_id)
        group = get_student_group(chat_id).lower()
    elif force_teacher:
        alias = 'PREP'
        group = force_teacher.lower()
    elif force_group:
        alias = 'GROUP'
        group = force_group.lower()

    for i in range(1, 7):
        sql_con = connect(const.path + 'Parse.db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT day_{} 
                            FROM zam_from_site'''.format(str(i)))
        cfone = cursor.fetchone()[0].split('][')
        cursor.close()
        sql_con.close()
        data = BeautifulSoup(cfone[0], 'lxml')
        soup = BeautifulSoup(cfone[1], 'lxml')
        all_page = soup.find_all('table')

        dataa = data.find_all('h1')
        dataaa = dataa[0].text.strip()

        groups = []

        for tab in all_page:
            for row in tab.find_all('tr')[1:]:
                if 'strong' in str(row):
                    continue
                tmp = row.find_all('td')
                grp = tmp[0].text.strip().replace('\n', '')
                teacher = tmp[4].text.strip().replace('\n', '')

                if alias == 'PREP':
                    if teacher:
                        if '/' in teacher.replace(' ', ''):
                            site_teacher = teacher.split('/')
                        else:
                            site_teacher = [teacher]

                        for teacher in site_teacher:
                            short_name = teacher.replace(
                                ' ', '').replace('.', '').lower()

                            if short_name == 'панасюксс':
                                surname = short_name
                            elif short_name == 'панасюксвсв':
                                surname = short_name
                            elif short_name == 'панасюквв':
                                surname = short_name
                            else:
                                surname = (teacher.split()[0].replace(' ', '')
                                           .replace('.', '')
                                           .lower().replace('ё', 'е'))

                            groups.append(surname)
                else:
                    if grp:
                        groups.append(grp.lower().replace(' ', ''))

        data10 = dataaa[-10:][:6] + dataaa[-10:][8:]

        yes = (const.emoji['check_mark'] + ' ' +
               const.num_day[str(i)] + ' (' + data10 + ')')
        no = (const.emoji['negative_squared_cross_mark'] +
              ' ' + const.num_day[str(i)] + ' (' + data10 + ')')

        yes_no = const.emoji['cross_mark'] + ' (' + const.emoji['check_mark'] + ') ' + const.num_day[
            str(i)] + ' (' + data10 + ')'
        no_no = const.emoji['cross_mark'] + ' (' + const.emoji['negative_squared_cross_mark'] + ') ' + const.num_day[
            str(i)] + ' (' + data10 + ')'

        a = dataaa[-10:].split('.')
        b = str(dt.datetime.today())[:-16].split('-')

        c = dt.datetime(int(a[2]), int(a[1]), int(a[0]))
        d = dt.datetime(int(b[0]), int(b[1]), int(b[2]))

        if alias == 'PREP':
            short_name = group.replace(' ', '').replace('.', '')

            if short_name == 'панасюксергейстепанович':
                surname = 'панасюксс'
            elif short_name == 'панасюксветланасвятославовна':
                surname = 'панасюксвсв'
            elif short_name == 'панасюквикторвладимирович':
                surname = 'панасюквв'
            else:
                surname = group.split()[0].replace(' ', '').replace('.', '')

            group = surname

        if c >= d:
            if group in groups:
                if yes not in active_days:
                    active_days.append(yes)
            elif group not in groups:
                if no not in active_days:
                    active_days.append(no)
        else:
            if group in groups:
                if yes_no not in active_days:
                    active_days.append(yes_no)
            elif group not in groups:
                if no_no not in active_days:
                    active_days.append(no_no)

    return active_days


def rewrite_zam_data(parse_day, html='NULL'):

    if parse_day == 's':
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find('div', class_='item-page')

        dataa = data.find_all('h1')
        all_page = soup.find_all('table')

        if dt.datetime.isoweekday(dt.datetime.now()) != 7:
            parse_day = dt.datetime.isoweekday(dt.datetime.now())
        elif dt.datetime.isoweekday(dt.datetime.now()) == 7:
            parse_day = dt.datetime.isoweekday(
                dt.datetime.now() + dt.timedelta(days=1))
        sql_con = connect(const.path + 'Parse.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE zam_from_site
                             SET day_{} = ?'''.format(str(parse_day)), (str(dataa) + str(all_page),))
        sql_con.commit()
        cursor.close()
        sql_con.close()
    elif parse_day == 'z':
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find('div', class_='item-page')

        dataa = data.find_all('h1')
        all_page = soup.find_all('table')

        if dt.datetime.isoweekday(dt.datetime.now()) != 6:
            parse_day = dt.datetime.isoweekday(
                dt.datetime.now() + dt.timedelta(days=1))
        elif dt.datetime.isoweekday(dt.datetime.now()) == 6:
            parse_day = dt.datetime.isoweekday(
                dt.datetime.now() + dt.timedelta(days=2))
        sql_con = connect(const.path + 'Parse.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE zam_from_site
                             SET day_{} = ?'''.format(str(parse_day)), (str(dataa) + str(all_page),))
        sql_con.commit()
        cursor.close()
        sql_con.close()
    elif parse_day == 'all':
        htmls = [const.ponedelnik, const.vtornik, const.sreda,
                 const.chetverg, const.pyatnica, const.subotta]

        for parse_day in range(1, 7):
            soup = BeautifulSoup(get_html(htmls[parse_day - 1]), 'lxml')
            data = soup.find('div', class_='item-page')

            dataa = data.find_all('h1')
            all_page = soup.find_all('table')

            sql_con = connect(const.path + 'Parse.db')
            cursor = sql_con.cursor()
            cursor.execute('''UPDATE zam_from_site
                                 SET day_{} = ?'''.format(str(parse_day)), (str(dataa) + str(all_page),))
            sql_con.commit()
            cursor.close()
            sql_con.close()
            parse_day += 1
    else:
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find('div', class_='item-page')

        dataa = data.find_all('h1')
        all_page = soup.find_all('table')

        sql_con = connect(const.path + 'Parse.db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE zam_from_site
                             SET day_{} = ?'''.format(str(parse_day)), (str(dataa) + str(all_page),))
        sql_con.commit()
        cursor.close()
        sql_con.close()


def pay_url(re):
    if re == 's':
        if dt.datetime.isoweekday(dt.datetime.now()) == 1:
            return const.ponedelnik
        elif dt.datetime.isoweekday(dt.datetime.now()) == 2:
            return const.vtornik
        elif dt.datetime.isoweekday(dt.datetime.now()) == 3:
            return const.sreda
        elif dt.datetime.isoweekday(dt.datetime.now()) == 4:
            return const.chetverg
        elif dt.datetime.isoweekday(dt.datetime.now()) == 5:
            return const.pyatnica
        elif dt.datetime.isoweekday(dt.datetime.now()) == 6:
            return const.subotta
        elif dt.datetime.isoweekday(dt.datetime.now()) == 7:
            return const.ponedelnik
    elif re == 'z':
        if dt.datetime.isoweekday(dt.datetime.now()) == 1:
            return const.vtornik
        elif dt.datetime.isoweekday(dt.datetime.now()) == 2:
            return const.sreda
        elif dt.datetime.isoweekday(dt.datetime.now()) == 3:
            return const.chetverg
        elif dt.datetime.isoweekday(dt.datetime.now()) == 4:
            return const.pyatnica
        elif dt.datetime.isoweekday(dt.datetime.now()) == 5:
            return const.subotta
        elif dt.datetime.isoweekday(dt.datetime.now()) == 6:
            return const.ponedelnik
        elif dt.datetime.isoweekday(dt.datetime.now()) == 7:
            return const.ponedelnik


def get_date(tomorrow=False, tomorrow_tomorrow=False, force_day_of_week=False, week_td=False):
    if tomorrow_tomorrow:
        return str(int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=2), '%d'))) + ' ' + const.month_list[int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=2), '%m')) - 1], dt.datetime.strftime(dt.date.today() + dt.timedelta(days=2), '%d.%m.%Y')
    elif tomorrow:
        return str(int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%d'))) + ' ' + const.month_list[int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%m')) - 1], dt.datetime.strftime(dt.date.today() + dt.timedelta(days=1), '%d.%m.%Y')
    elif force_day_of_week:
        return str(int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=int(force_day_of_week)), '%d'))) + ' ' + const.month_list[int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=int(force_day_of_week)), '%m')) - 1], dt.datetime.strftime(dt.date.today() + dt.timedelta(days=int(force_day_of_week)), '%d.%m.%Y')
    elif week_td:
        return str(int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=int(week_td) + 1), '%d'))) + ' ' + const.month_list[int(dt.datetime.strftime(dt.date.today() + dt.timedelta(days=int(week_td) + 1), '%m')) - 1], dt.datetime.strftime(dt.date.today() + dt.timedelta(days=int(week_td) + 1), '%d.%m.%Y')
    else:
        return str(int(dt.datetime.strftime(dt.date.today(), '%d'))) + ' ' + const.month_list[int(dt.datetime.strftime(dt.date.today(), '%m')) - 1], dt.datetime.strftime(dt.date.today(), '%d.%m.%Y')


def delta_seconds(hour, minute):
    year = dt.datetime.strftime(dt.date.today(), '%Y')
    mounth = int(dt.datetime.strftime(dt.date.today(), '%m'))
    day = int(dt.datetime.strftime(dt.date.today(), '%d'))
    then = dt.datetime(int(year), int(mounth),
                       int(day), int(hour), int(minute))
    now = dt.datetime.now()
    delta = then - now
    return delta.seconds // 60 + 1


def appendd(delta_h, delta_m, time, next_time):
    times = []

    times.append(delta_seconds(delta_h, delta_m))
    times.append(time)
    times.append(next_time)
    return times


def get_different_between(valid_date):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT abridged_calls
                        FROM offer''')
    abridged_calls = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()

    if abridged_calls == None:
        abridged_calls = '11.11.1111'

    abridged_date = [call.split('.')
                     for call in abridged_calls.split('\n')]
    datetime_date = valid_date.split('.')
    abridged_call = [dt.datetime(int(abr_date[2]),
                                 int(abr_date[1]),
                                 int(abr_date[0]))
                     for abr_date in abridged_date]
    datetime_call = dt.datetime(int(datetime_date[2]),
                                int(datetime_date[1]),
                                int(datetime_date[0]))
    return datetime_call, abridged_call


def blzv():
    time_now = dt.datetime.now()
    valid_date = dt.datetime.strftime(dt.date.today(), '%d.%m.%Y')
    different = get_different_between(valid_date)

    if different[0] in different[1]:
        if dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '08:00:00':
            return appendd(8, 0, '08:00', '09:00')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '09:00:00':
            return appendd(9, 0, '09:00', '09:10')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '09:10:00':
            return appendd(9, 10, '09:10', '10:10')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '10:10:00':
            return appendd(10, 10, '10:10', '10:20')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '10:20:00':
            return appendd(10, 20, '10:20', '11:20')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '11:20:00':
            return appendd(11, 20, '11:20', '11:30')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '11:30:00':
            return appendd(11, 30, '11:30', '12:30')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '12:30:00':
            return appendd(12, 30, '12:30', '12:40')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '12:40:00':
            return appendd(12, 40, '12:40', '13:40')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '13:40:00':
            return appendd(13, 40, '13:40', '13:50')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '13:50:00':
            return appendd(13, 50, '13:50', '14:50')
        elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '14:50:00':
            return appendd(14, 50, '14:50', '08:00')
        else:
            return appendd(8, 0, '08:00', '08:45')
    else:
        if dt.datetime.isoweekday(time_now) != 6:
            if dt.datetime.isoweekday(time_now) == 7:
                return appendd(8, 0, '08:00', '08:45')
            if dt.datetime.isoweekday(time_now) != 7:
                if dt.datetime.strftime(time_now, '%H:%M:%S') <= '08:00:00':
                    return appendd(8, 0, '08:00', '08:45')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '08:45:00':
                    return appendd(8, 45, '08:45', '08:55')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '08:55:00':
                    return appendd(8, 55, '08:55', '09:40')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '09:40:00':
                    return appendd(9, 40, '09:40', '09:50')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '09:50:00':
                    return appendd(9, 50, '09:50', '10:35')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '10:35:00':
                    return appendd(10, 35, '10:35', '10:45')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '10:45:00':
                    return appendd(10, 45, '10:45', '11:30')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '11:30:00':
                    return appendd(11, 30, '11:30', '11:50')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '11:50:00':
                    return appendd(11, 50, '11:50', '12:35')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '12:35:00':
                    return appendd(12, 35, '12:35', '12:45')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '12:45:00':
                    return appendd(12, 45, '12:45', '13:30')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '13:30:00':
                    return appendd(13, 30, '13:30', '14:25')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '14:25:00':
                    return appendd(14, 25, '14:25', '15:10')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '15:10:00':
                    return appendd(15, 10, '15:10', '15:20')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '15:20:00':
                    return appendd(15, 20, '15:20', '16:05')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '16:05:00':
                    return appendd(16, 5, '16:05', '16:25')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '16:25:00':
                    return appendd(16, 25, '16:25', '17:10')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '17:10:00':
                    return appendd(17, 10, '17:10', '17:20')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '17:20:00':
                    return appendd(17, 20, '17:20', '18:05')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '18:05:00':
                    return appendd(18, 5, '18:05', '18:15')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '18:15:00':
                    return appendd(18, 15, '18:15', '19:00')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '19:00:00':
                    return appendd(19, 0, '19:00', '19:10')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '19:10:00':
                    return appendd(19, 10, '19:10', '19:55')
                elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '19:55:00':
                    return appendd(19, 55, '19:55', '08:00')
                else:
                    return appendd(8, 0, '08:00', '08:45')

        elif dt.datetime.isoweekday(time_now) == 6:
            if dt.datetime.strftime(time_now, '%H:%M:%S') <= '08:00:00':
                return appendd(8, 0, '08:00', '08:45')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '08:45:00':
                return appendd(8, 45, '08:45', '08:55')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '08:55:00':
                return appendd(8, 55, '08:55', '09:40')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '09:40:00':
                return appendd(9, 40, '09:40', '09:50')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '09:50:00':
                return appendd(9, 50, '09:50', '10:35')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '10:35:00':
                return appendd(10, 35, '10:35', '10:45')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '10:45:00':
                return appendd(10, 45, '10:45', '11:30')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '11:30:00':
                return appendd(11, 30, '11:30', '11:50')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '11:40:00':
                return appendd(11, 40, '11:40', '12:25')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '12:25:00':
                return appendd(12, 25, '12:25', '12:35')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '12:35:00':
                return appendd(12, 35, '12:35', '13:20')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '13:20:00':
                return appendd(13, 20, '13:20', '13:35')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '13:35:00':
                return appendd(13, 35, '13:35', '14:20')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '14:20:00':
                return appendd(14, 20, '14:20', '14:30')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '14:30:00':
                return appendd(14, 30, '14:30', '15:15')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '15:15:00':
                return appendd(15, 15, '15:15', '15:25')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '15:25:00':
                return appendd(15, 25, '15:25', '16:10')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '16:10:00':
                return appendd(16, 10, '16:10', '16:20')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '16:20:00':
                return appendd(16, 20, '16:20', '17:05')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '17:05:00':
                return appendd(17, 5, '17:05', '17:15')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '17:15:00':
                return appendd(17, 15, '17:15', '18:00')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '18:00:00':
                return appendd(18, 0, '18:00', '18:10')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '18:10:00':
                return appendd(18, 10, '18:10', '18:55')
            elif dt.datetime.strftime(time_now, '%H:%M:%S') <= '18:55:00':
                return appendd(18, 55, '18:55', '08:00')
            else:
                return appendd(8, 0, '08:00', '08:45')


def blzvs():
    if dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '10:00:00':
        return appendd(10, 0, '10:00', '11:00')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '11:00:00':
        return appendd(11, 0, '11:00', '11:10')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '11:10:00':
        return appendd(11, 10, '11:10', '12:10')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '12:10:00':
        return appendd(12, 10, '12:10', '12:20')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '12:20:00':
        return appendd(12, 20, '12:20', '13:20')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '13:20:00':
        return appendd(13, 20, '13:20', '13:30')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '13:30:00':
        return appendd(13, 30, '13:30', '14:30')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '14:30:00':
        return appendd(14, 30, '14:30', '14:40')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '14:40:00':
        return appendd(14, 40, '14:40', '15:40')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '15:40:00':
        return appendd(15, 40, '15:40', '15:50')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '15:50:00':
        return appendd(15, 50, '15:50', '16:50')
    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M:%S') <= '16:50:00':
        return appendd(16, 50, '16:50', '10:00')
    else:
        return appendd(8, 0, '08:00', '08:45')


def delete_user(user_id, only_choice=False):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''DELETE FROM user_choice 
                            WHERE user_id = ?''', (user_id,))
    sql_con.commit()
    if not only_choice:
        cursor.execute('''DELETE FROM banned_users 
                                WHERE id_not_banned = ?''', (user_id,))
        sql_con.commit()
        cursor.execute('''DELETE FROM user_data 
                                WHERE id = ?''', (user_id,))
        sql_con.commit()
    cursor.close()
    sql_con.close()


def delete_all_user_info(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''DELETE FROM user_choice 
                            WHERE user_id = ?''', (user_id,))
    sql_con.commit()
    cursor.execute('''DELETE FROM banned_users 
                            WHERE id_not_banned = ?''', (user_id,))
    sql_con.commit()
    cursor.execute('''DELETE FROM banned_users 
                            WHERE id_banned = ?''', (user_id,))
    sql_con.commit()
    cursor.execute('''DELETE FROM user_data 
                            WHERE id = ?''', (user_id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()


def send_long_message(bot, text, user_id, markup=False):
    try:
        if markup:
            bot.send_message(user_id, text, parse_mode='HTML',
                             reply_markup=markup)
        else:
            bot.send_message(user_id, text, parse_mode='HTML')
    except tb.apihelper.ApiException as ApiExcept:
        json_err = loads(ApiExcept.result.text)
        if json_err['description'] == 'Bad Request: message is too long':
            event_count = len(text.split('\n\n'))
            first_part = '\n\n'.join(text.split('\n\n')[:event_count // 2])
            second_part = '\n\n'.join(text.split('\n\n')[event_count // 2:])
            send_long_message(bot, first_part, user_id)
            send_long_message(bot, second_part, user_id)


def get_data_from_replacements(teacher=False, group=False):
    repls = []
    if teacher:
        active_days = get_active_replace_days(force_teacher=teacher)
        for day in active_days:
            if const.emoji['cross_mark'] not in day:
                repls.append(get_replace_of_day(active_days.index(day) + 1,
                                                force_teacher=teacher))
    elif group:
        active_days = get_active_replace_days(force_group=group)
        for day in active_days:
            if const.emoji['cross_mark'] not in day:
                repls.append(get_replace_of_day(active_days.index(day) + 1,
                                                force_group=group))

    if repls:
        return repls


def regex_matches(query):
    return re.match(const.pattern,
                    re.sub(const.sub_pattern, '',
                           query.replace('ё', 'е').replace(' ', '').lower()))


def check_teacher(teacher_names, full_teachers_name=False):
    names = []
    checked_indexes = []
    pre_checked_indexes = []
    teachers = const.existing_teachers.copy()

    for teacher in teacher_names:
        for i in const.cap_teachers:
            if teacher == i:
                if full_teachers_name:
                    index = const.cap_teachers.index(i)
                    if const.teacher_name[index] not in names:
                        names.append(const.teacher_name[index])
                        pre_checked_indexes.append(index)
                else:
                    if teacher not in names:
                        names.append(teacher)

    checked_names = []

    not_in_shedule = []

    if full_teachers_name:
        for name in names:
            if name in teachers:
                if name not in checked_names:
                    checked_names.append(name)
                    checked_indexes.append(
                        pre_checked_indexes[names.index(name)])
            elif name not in not_in_shedule:
                not_in_shedule.append(name)
    else:
        for name in names:
            index = const.cap_teachers.index(name)
            if const.teacher_name[index] in teachers:
                if name not in checked_names:
                    checked_names.append(name)
            elif name not in not_in_shedule:
                not_in_shedule.append(name)

    if not_in_shedule:
        db_teachers = []

        for i in range(1, 7):
            sql_con = connect(const.path + 'Parse.db')
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
                else:
                    surname = i.split()[0].replace(
                        ' ', '').replace('.', '').lower()

                if surname in surnames:
                    if i not in checked_names:
                        checked_names.append(i)
                        checked_indexes.append(const.teacher_name.index(i))

    if full_teachers_name:
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
    else:
        return checked_names


def search_teacher(name_for_search, dot_except=False, from_menu=False):
    matches = regex_matches(name_for_search)

    if matches != None:
        teacher_name = matches.group()
    else:
        return []

    teachers = []

    for i in const.low_teachers:
        if i.startswith(teacher_name):
            index = const.low_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            teachers.append(full_teacher_name)
    for i in const.cap_teachers:
        if i.split()[1].lower().startswith(teacher_name):
            index = const.cap_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            if full_teacher_name not in teachers:
                teachers.append(full_teacher_name)
    for i in const.cap_teachers:
        if i.split()[2].lower().startswith(teacher_name):
            index = const.cap_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            if full_teacher_name not in teachers:
                teachers.append(full_teacher_name)
    for i in const.low_teachers:
        if teacher_name in i:
            index = const.low_teachers.index(i)
            full_teacher_name = const.cap_teachers[index]
            if full_teacher_name not in teachers:
                teachers.append(full_teacher_name)

    if '.' in name_for_search:
        match_teachers = [regex_matches(i).group() for i in const.sht_teachers]
        dot_except = True
        if teacher_name in match_teachers:
            full_teacher_name = search_teacher(
                name_for_search.split('.')[0], dot_except)
            for i in full_teacher_name:
                if i not in teachers:
                    teachers.append(i)

    if from_menu:
        return check_teacher(teachers, from_menu)
    else:
        return check_teacher(teachers)


def shorting_teachers(teachers):
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

    return short_teachers


def edit_week(up=True):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    if up:
        cursor.execute('''UPDATE offer
                             SET week = 1''')
        sql_con.commit()
    else:
        cursor.execute('''UPDATE offer
                             SET week = 0''')
        sql_con.commit()
    cursor.close()
    sql_con.close()


def edit_sending_log(up=True):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    if up:
        cursor.execute('''UPDATE offer
                             SET sending_log = 1''')
        sql_con.commit()
    else:
        cursor.execute('''UPDATE offer
                             SET sending_log = 0''')
        sql_con.commit()
    cursor.close()
    sql_con.close()


def edit_on_or_off_zam(online=True):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    if online:
        cursor.execute('''UPDATE offer
                             SET on_or_off_zam = 1''')
        sql_con.commit()
    else:
        cursor.execute('''UPDATE offer
                             SET on_or_off_zam = 0''')
        sql_con.commit()
    cursor.close()
    sql_con.close()


def get_sending_log():
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT sending_log 
                        FROM offer''')
    sending_log = cursor.fetchone()
    cursor.close()
    sql_con.close()
    if sending_log[0]:
        return 'ON'
    else:
        return 'OFF'


def get_on_or_off_zam():
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT on_or_off_zam 
                        FROM offer''')
    on_or_off_zam = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()
    if on_or_off_zam:
        return 'ONLINE'
    else:
        return 'OFFLINE'


def get_week():
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT week 
                        FROM offer''')
    week = cursor.fetchone()
    cursor.close()
    sql_con.close()

    if dt.datetime.today().isocalendar()[1] % 2 == 0 and week[0] == True:
        return 'DOWN'
    elif dt.datetime.today().isocalendar()[1] % 2 == 0 and week[0] == False:
        return 'UP'
    elif dt.datetime.today().isocalendar()[1] % 2 != 0 and week[0] == True:
        return 'UP'
    elif dt.datetime.today().isocalendar()[1] % 2 != 0 and week[0] == False:
        return 'DOWN'


def get_alias(chat_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT alias
                        FROM user_data
                       WHERE id = ?''', (chat_id,))
    data = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()
    return data


def get_shedule_answer(day_info, valid_date=False):
    answer = ''

    for lesson_info in day_info:
        time = lesson_info[1]
        lesson = lesson_info[2].strip()
        teacher = lesson_info[3].strip()
        audience = lesson_info[4].strip()
        valid_info = lesson_info[0]

        if lesson.strip():
            if valid_date:
                different = get_different_between(valid_date)

                if different[0] in different[1]:
                    time = const.abridged_lesson_time[str(list(const.lesson_time.values())
                                                          .index(time) + 1)]
            answer += const.emoji['clock'] + ' ' + time
            lesson_num = ''

            if (time == const.lesson_time['1'] or
                    time == const.abridged_lesson_time['1']):
                lesson_num = '1.'
            elif (time == const.lesson_time['2'] or
                  time == const.abridged_lesson_time['2']):
                lesson_num = '2.'
            elif (time == const.lesson_time['3'] or
                  time == const.lesson_time['3s'] or
                  time == const.abridged_lesson_time['3']):
                lesson_num = '3.'
            elif (time == const.lesson_time['4'] or
                  time == const.lesson_time['4s'] or
                  time == const.abridged_lesson_time['4']):
                lesson_num = '4.'
            elif (time == const.lesson_time['5'] or
                  time == const.lesson_time['5s'] or
                  time == const.abridged_lesson_time['5']):
                lesson_num = '5.'
            elif (time == const.lesson_time['6'] or
                  time == const.lesson_time['6s'] or
                  time == const.abridged_lesson_time['6']):
                lesson_num = '6.'

            if (valid_info != '' and len(lesson.split('/')) - 1 >=
                    valid_info):
                valid_lesson = ''
                div_lessons = lesson.split('/')

                for div_lesson in div_lessons:
                    if div_lesson == div_lessons[valid_info]:
                        valid_lesson += '<b>' + div_lesson + '</b>'
                    else:
                        valid_lesson += div_lesson

                    if len(div_lessons) == valid_lesson.count('/'):
                        break
                    else:
                        valid_lesson += '/'

                answer += '\n' + lesson_num + ' ' + valid_lesson
            else:
                answer += '\n' + lesson_num + ' <b>' + lesson + '</b>'

            if audience:
                if (valid_info != '' and len(audience.split('/')) - 1 >=
                        valid_info):
                    valid_lesson = ''
                    div_audiences = audience.split('/')

                    for div_lesson in div_audiences:
                        if div_lesson == div_audiences[valid_info]:
                            valid_lesson += '<b>' + div_lesson + '</b>'
                        else:
                            valid_lesson += div_lesson

                        if len(div_audiences) == valid_lesson.count('/'):
                            break
                        else:
                            valid_lesson += '/'

                    answer += ' (' + valid_lesson + ')\n'
                else:
                    answer += ' (' + audience + ')\n'
            else:
                answer += '\n'

            if teacher:
                answer += '<i>' + teacher + '</i>\n\n'
            else:
                answer += '\n'

    return answer


def create_schedule_answer(user_id, tomorrow=False):
    full_date = [False, False]
    week = get_week()
    alias = get_alias(user_id)
    group = get_student_group(user_id)
    day_of_week = dt.datetime.isoweekday(dt.datetime.now())

    if tomorrow:
        if day_of_week == 7:
            date = str(dt.datetime.isoweekday(
                dt.datetime.now() + dt.timedelta(days=1)))
            answer = const.emoji['calendar'] + ' '
            answer += const.num_day[date] + ', '
            full_date = get_date(True)
            answer += full_date[0] + '\n'
            td = 1
            if week == 'DOWN':
                answer += const.up_week
                week = 'UP'
            elif week == 'UP':
                answer += const.down_week
                week = 'DOWN'
        elif day_of_week == 6:
            date = str(dt.datetime.isoweekday(
                dt.datetime.now() + dt.timedelta(days=2)))
            answer = const.emoji['sleep'] + ' Выходной'
            answer += '\nРасписание на следующий день:\n\n'
            answer += const.emoji['calendar'] + ' '
            answer += const.num_day[date] + ', '
            full_date = get_date(tomorrow_tomorrow=True)
            answer += full_date[0] + '\n'
            td = 2
            if week == 'DOWN':
                answer += const.up_week
                week = 'UP'
            elif week == 'UP':
                answer += const.down_week
                week = 'DOWN'
        else:
            date = str(dt.datetime.isoweekday(
                dt.datetime.now() + dt.timedelta(days=1)))
            answer = const.emoji['calendar'] + ' '
            answer += const.num_day[date] + ', '
            full_date = get_date(True)
            answer += full_date[0] + '\n'
            td = 1
            if week == 'UP':
                answer += const.up_week
            elif week == 'DOWN':
                answer += const.down_week
    else:
        if day_of_week != 7:
            date = str(day_of_week)
            answer = const.emoji['calendar'] + ' '
            answer += const.num_day[date] + ', '
            full_date = get_date()
            answer += full_date[0] + '\n'
            td = 0
            if week == 'UP':
                answer += const.up_week
            elif week == 'DOWN':
                answer += const.down_week
        elif day_of_week == 7:
            date = str(dt.datetime.isoweekday(
                dt.datetime.now() + dt.timedelta(days=1)))
            answer = const.emoji['sleep'] + ' Выходной'
            answer += '\nРасписание на следующий день:\n\n'
            answer += const.emoji['calendar'] + ' '
            answer += const.num_day[date] + ', '
            full_date = get_date(True)
            answer += full_date[0] + '\n'
            td = 1
            if week == 'DOWN':
                answer += const.up_week
                week = 'UP'
            elif week == 'UP':
                answer += const.down_week
                week = 'DOWN'

    answer += const.notify

    if alias == 'PREP':
        try:
            day_info = const.teachers_shedule[
                const.teacher_name[const.cap_teachers.index(group)]]
        except:
            return ('Расписание для преподавателя "<b>' + group +
                    '</b>" не найдено\U00002026')
    else:
        try:
            day_info = const.shedule[group]
        except:
            return ('Расписание для группы "<b>' + group +
                    '</b>" не найдено\U00002026')

    day_info = day_info[week][dt.datetime.isoweekday(dt.datetime.now() +
                                                     dt.timedelta(days=td)) - 1]
    if day_info or alias != 'PREP':
        answer += get_shedule_answer(day_info, full_date[1])
    else:
        answer += '<i>%s</i>' % const.not_events_for_teachers

    if not day_info and alias != 'PREP':
        answer += '<i>%s</i>' % const.not_events

    return answer


def create_schedule_week_answer(user_id, td, force_day_of_week=0):
    full_date = [False, False]
    week = get_week()
    alias = get_alias(user_id)
    group = get_student_group(user_id)
    day_of_week = dt.datetime.isoweekday(dt.datetime.now())

    if day_of_week != 7:
        day_date = day_of_week
    elif day_of_week == 7:
        day_date = dt.datetime.isoweekday(
            dt.datetime.now() + dt.timedelta(days=8))
    answer = const.emoji['calendar'] + ' '
    answer += const.num_day[str(td)]

    if force_day_of_week == 0:
        if day_of_week != 7:
            full_date = get_date(force_day_of_week=str(-(day_date - td)))
            answer += ', ' + full_date[0] + '\n'
            if week == 'UP':
                answer += const.up_week
                week = 'UP'
            elif week == 'DOWN':
                answer += const.down_week
                week = 'DOWN'
        elif day_of_week == 7:
            full_date = get_date(week_td=str(-(day_date - td)))
            answer += ', ' + full_date[0] + '\n'
            if week == 'UP':
                answer += const.down_week
                week = 'DOWN'
            elif week == 'DOWN':
                answer += const.up_week
                week = 'UP'
    elif force_day_of_week == 1:
        answer += '\n' + const.down_week
        week = 'DOWN'
    elif force_day_of_week == 2:
        answer += '\n' + const.up_week
        week = 'UP'

    answer += const.notify

    if alias == 'PREP':
        try:
            day_info = const.teachers_shedule[
                const.teacher_name[const.cap_teachers.index(group)]]
        except:
            return ('Расписание для преподавателя "<b>' + group +
                    '</b>" не найдено\U00002026')
    else:
        try:
            day_info = const.shedule[group]
        except:
            return ('Расписание для группы "<b>' + group +
                    '</b>" не найдено\U00002026')

    day_info = day_info[week][td - 1]
    if day_info or alias != 'PREP':
        answer += get_shedule_answer(day_info, full_date[1])
    else:
        answer += '<i>%s</i>' % const.not_events_for_teachers

    if not day_info and alias != 'PREP':
        answer += '<i>%s</i>' % const.not_events

    return answer


def send_schedule_force_week_answer(message, force_day_of_week=0):
    td = 1
    valid_days = []
    week = get_week()
    alias = get_alias(message.chat.id)
    group = get_student_group(message.chat.id)
    day_of_week = dt.datetime.isoweekday(dt.datetime.now())

    back_from_week = tb.types.InlineKeyboardMarkup()
    back_from_schedule = tb.types.InlineKeyboardMarkup()

    back_from_week.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Нaзад']])
    back_from_schedule.row(
        *[tb.types.InlineKeyboardButton(text=name, callback_data=name) for
            name in ['« Haзад']])

    if day_of_week != 7:
        day_date = day_of_week
    elif day_of_week == 7:
        day_date = dt.datetime.isoweekday(
            dt.datetime.now() + dt.timedelta(days=8))

    if force_day_of_week == 0:
        if day_of_week != 7:
            if week == 'UP':
                shedule_week = 'UP'
            elif week == 'DOWN':
                shedule_week = 'DOWN'
        elif day_of_week == 7:
            if week == 'UP':
                shedule_week = 'DOWN'
            elif week == 'DOWN':
                shedule_week = 'UP'
    elif force_day_of_week == 1:
        shedule_week = 'DOWN'
    elif force_day_of_week == 2:
        shedule_week = 'UP'

    if alias == 'PREP':
        try:
            day_info = const.teachers_shedule[
                const.teacher_name[const.cap_teachers.index(group)]]
        except:
            return bot.edit_message_text(
                text='Расписание для преподавателя "<b>'
                + group + '</b>" не найдено\U00002026',
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode='HTML')

        xday = 1
        for i in range(6):
            if bool(len(day_info[shedule_week][i])) == True:
                valid_days.append(xday)
            xday += 1
    else:
        try:
            day_info = const.shedule[group]
        except:
            return bot.edit_message_text(
                text='Расписание для группы "<b>' +
                group + '</b>" не найдено\U00002026',
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode='HTML')

    for day in range(6):
        if td < 8:
            full_date = [False, False]
            answer = const.emoji['calendar'] + ' '
            answer += const.num_day[str(td)]

            if force_day_of_week == 0:
                if day_of_week != 7:
                    full_date = get_date(
                        force_day_of_week=str(-(day_date - td)))
                    answer += ', ' + full_date[0] + '\n'
                    if week == 'UP':
                        answer += const.up_week
                    elif week == 'DOWN':
                        answer += const.down_week
                elif day_of_week == 7:
                    full_date = get_date(week_td=str(-(day_date - td)))
                    answer += ', ' + full_date[0] + '\n'
                    if week == 'UP':
                        answer += const.down_week
                    elif week == 'DOWN':
                        answer += const.up_week
            elif force_day_of_week == 1:
                answer += '\n' + const.down_week
            elif force_day_of_week == 2:
                answer += '\n' + const.up_week

            if td < 7:
                week_info = day_info[shedule_week][td - 1]
                td += 1

                answer += const.notify

                len_valid_days = len(valid_days)

                if week_info or alias != 'PREP':
                    answer += get_shedule_answer(week_info, full_date[1])

                    if not week_info and alias != 'PREP':
                        answer += '<i>%s</i>' % const.not_events

                    if alias == 'PREP':
                        if len_valid_days == 1:
                            bot.edit_message_text(answer,
                                                  message.chat.id,
                                                  message.message_id,
                                                  parse_mode='HTML',
                                                  reply_markup=back_from_week)
                        else:
                            if td - 1 == valid_days[0]:
                                bot.edit_message_text(answer,
                                                      message.chat.id,
                                                      message.message_id,
                                                      parse_mode='HTML')
                            elif td - 1 == valid_days[-1]:
                                bot.send_message(message.chat.id, answer,
                                                 parse_mode='HTML',
                                                 reply_markup=back_from_schedule)
                            else:
                                bot.send_message(message.chat.id, answer,
                                                 parse_mode='HTML',
                                                 disable_notification=True)
                    else:
                        if td == 2:
                            bot.edit_message_text(answer,
                                                  message.chat.id,
                                                  message.message_id,
                                                  parse_mode='HTML')
                        elif td == 7:
                            bot.send_message(message.chat.id, answer,
                                             parse_mode='HTML',
                                             reply_markup=back_from_schedule)
                        else:
                            bot.send_message(message.chat.id, answer,
                                             parse_mode='HTML',
                                             disable_notification=True)
                elif len_valid_days == 0:
                    bot.edit_message_text(const.emoji['sleep'] +
                                          ' Выходная неделя',
                                          message.chat.id,
                                          message.message_id,
                                          parse_mode='HTML',
                                          reply_markup=back_from_week)


def send_teacher_week_answer(message, teacher, free_week=False,
                             hold_week=False):
    td = 1
    week = get_week()
    day_of_week = dt.datetime.isoweekday(dt.datetime.now())

    if day_of_week != 7:
        day_date = day_of_week
    elif day_of_week == 7:
        day_date = dt.datetime.isoweekday(
            dt.datetime.now() + dt.timedelta(days=8))

    if day_of_week != 7:
        if week == 'UP':
            shedule_week = 'UP'
        elif week == 'DOWN':
            shedule_week = 'DOWN'
    elif day_of_week == 7:
        if week == 'UP':
            shedule_week = 'DOWN'
        elif week == 'DOWN':
            shedule_week = 'UP'

    try:
        day_info = const.teachers_shedule[teacher]
    except:
        return bot.edit_message_text(
            text='Расписание для преподавателя "<b>'
            + teacher + '</b>" не найдено\U00002026',
            chat_id=message.chat.id,
            message_id=message.message_id,
            parse_mode='HTML')

    week_day_info = day_info[shedule_week]

    weekend_day = []
    xday = 1
    for day in week_day_info[::-1]:
        if len(day) == 0:
            weekend_day.append(xday)
            xday += 1
        else:
            break

    if shedule_week == 'UP':
        shedule_next_week = 'DOWN'
    elif shedule_week == 'DOWN':
        shedule_next_week = 'UP'
    weekend_next_week = []
    for day in day_info[shedule_next_week]:
        weekend_next_week.append(len(day))
    if sum(weekend_next_week) == 0:
        next_week_empty = True
    else:
        next_week_empty = False

    if weekend_day:
        last_weekend = weekend_day[-1]
        last_valid_day = len(week_day_info) - last_weekend
    else:
        last_valid_day = False

    first_of_days = []
    first_of_dates = []
    for day in range(6):
        if td < 8:
            valid_days = []
            is_next_week = ''
            full_date = [False, False]
            answer = const.emoji['calendar'] + ' '
            answer += const.num_day[str(td)]

            xday = 1
            for i in week_day_info:
                if bool(len(i)) == True:
                    valid_days.append(xday)
                xday += 1

            if day_of_week == 7 and hold_week:
                full_date = get_date(week_td=str(-(day_date - td)))
                answer += ', ' + full_date[0] + '\n'

                if week == 'UP':
                    answer += const.up_week
                    shedule_week = 'UP'
                elif week == 'DOWN':
                    answer += const.down_week
                    shedule_week = 'DOWN'
                week_day_info = day_info[shedule_week]
            elif day_of_week == 7:
                full_date = get_date(week_td=str(-(day_date - td)))
                answer += ', ' + full_date[0] + '\n'

                if week == 'UP':
                    answer += const.down_week
                elif week == 'DOWN':
                    answer += const.up_week
            elif (day_of_week != 7 and not free_week and next_week_empty and
                  (last_valid_day and day_of_week >= last_valid_day + 1)):
                full_date = get_date(
                    force_day_of_week=str(-(day_date - td)))
                answer += ', ' + full_date[0] + '\n'

                if week == 'UP':
                    answer += const.up_week
                elif week == 'DOWN':
                    answer += const.down_week
            elif ((last_valid_day and day_of_week >= last_valid_day + 1) or
                  free_week):
                full_date = get_date(week_td=str(-(dt.datetime.isoweekday(dt.datetime.now() +
                                                                          dt.timedelta(days=8 + last_weekend)) -
                                                   (td + last_weekend))))
                answer += ', ' + full_date[0] + '\n'

                if week == 'UP':
                    answer += (const.down_week.replace('\n', '') +
                               ' (<b>следующая</b>)' + '\n\n')
                    shedule_week = 'DOWN'
                    end_of_warn = ' (нижнюю неделю):\n\n'
                elif week == 'DOWN':
                    answer += (const.up_week.replace('\n', '') +
                               ' (<b>следующая</b>)' + '\n\n')
                    shedule_week = 'UP'
                    end_of_warn = ' (верхнюю неделю):\n\n'

                if free_week:
                    is_next_week = (
                        const.emoji['warning_sign'] +
                        ' В связи с тем что <b>эта '
                        'неделя выходная</b>, будет показано <b>расписание '
                        'на следующую</b>' + end_of_warn)
                else:
                    is_next_week = (
                        const.emoji['warning_sign'] +
                        ' В связи с тем что <b>на этой '
                        'неделе больше нету пар</b>, будет показано <b>расписание '
                        'на следующую</b>' + end_of_warn)
                week_day_info = day_info[shedule_week]
            elif day_of_week != 7:
                full_date = get_date(
                    force_day_of_week=str(-(day_date - td)))
                answer += ', ' + full_date[0] + '\n'

                if week == 'UP':
                    answer += const.up_week
                elif week == 'DOWN':
                    answer += const.down_week

            xday = 1
            for i in week_day_info:
                if bool(len(i)) == True:
                    valid_days.append(xday)
                xday += 1

            if td < 7:
                len_valid_days = len(valid_days)
                week_info = day_info[shedule_week][td - 1]
                td += 1

                answer += const.notify

                if week_info:
                    answer += get_shedule_answer(week_info, full_date[1])

                    if const.emoji['arrow_up'] in answer:
                        range_of_days = (answer.split(',')[1]
                                         .split(const.emoji['arrow_up'])[0].replace('\n', ''))
                    elif const.emoji['arrow_down'] in answer:
                        range_of_days = (answer.split(',')[1]
                                         .split(const.emoji['arrow_down'])[0].replace('\n', ''))

                    head_answer = (
                        const.emoji['bust_in_silhouette'] +
                        ' Расписание преподавателя: '
                        '<b>' +
                        const.cap_teachers[const.teacher_name.index(teacher)] +
                        '</b>')
                    year = full_date[1].split('.')[-1]

                    if td - 1 == valid_days[0]:
                        if is_next_week:
                            head_answer += '\n\n' + is_next_week
                        first_date = bot.edit_message_text(head_answer,
                                                           message.chat.id,
                                                           message.message_id,
                                                           parse_mode='HTML')
                        first_of_days.append(first_date)
                        first_of_dates.append(range_of_days)
                    elif (td - 1 == valid_days[-1] and
                          (is_next_week or len_valid_days != 1)):
                        head_answer += ('\n\n' + is_next_week +
                                        const.emoji['calendar'] +
                                        first_of_dates[0] + ' ' + year +
                                        ' –' + range_of_days + ' ' + year)
                        bot.edit_message_text(head_answer,
                                              message.chat.id,
                                              first_of_days[0].message_id,
                                              parse_mode='HTML')

                    if td - 1 == valid_days[0] or td - 1 == valid_days[-1]:
                        bot.send_message(message.chat.id, answer,
                                         parse_mode='HTML')
                    else:
                        bot.send_message(message.chat.id, answer,
                                         parse_mode='HTML',
                                         disable_notification=True)
                elif len_valid_days == 0:
                    if day_of_week == 7 and not hold_week:
                        send_teacher_week_answer(message, teacher,
                                                 hold_week=True)
                    elif day_of_week != 7 and not free_week:
                        send_teacher_week_answer(message, teacher, True)
                    break


def is_user_in_all_users(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT count(id) 
                        FROM all_users
                       WHERE id = ?''', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    return data[0]


def is_user_exist(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT count(id) 
                        FROM user_data
                       WHERE id = ?''', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    return data[0]


def is_user_banned(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT count(id_banned) 
                        FROM banned_users
                       WHERE id_banned = ?''', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    return data[0]


def is_user_not_banned(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT count(id_not_banned) 
                        FROM banned_users
                       WHERE id_not_banned = ?''', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    return data[0]


def get_not_banned_users(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT id_not_banned
                        FROM banned_users''')
    data = cursor.fetchall()
    cursor.close()
    sql_con.close()
    return data


def banned_users(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT id_banned
                        FROM banned_users''')
    data = cursor.fetchall()
    sql_con.commit()
    cursor.close()
    sql_con.close()
    return data


def ban_user(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''DELETE FROM banned_users 
                            WHERE id_not_banned = ?''', (user_id,))
    sql_con.commit()
    cursor.execute('''INSERT INTO banned_users (id_banned)
                           VALUES (?)''', (user_id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()


def unban_user(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''DELETE FROM banned_users 
                            WHERE id_banned = ?''', (user_id,))
    sql_con.commit()
    cursor.execute('''INSERT INTO banned_users (id_not_banned)
                           VALUES (?)''', (user_id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()


def is_sending_rasp_on(user_id, rasp5=False):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    if rasp5:
        cursor.execute('''SELECT sending_rasp_5 
                            FROM user_data
                           WHERE id = ?''', (user_id,))
    else:
        cursor.execute('''SELECT sending_rasp 
                            FROM user_data
                           WHERE id = ?''', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    return data[0]


def is_sending_zam_on(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT sending_zam 
                        FROM user_data
                       WHERE id = ?''', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    return data[0]


def set_sending_rasp(user_id, on=True, rasp5=False):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    if rasp5:
        cursor.execute('''UPDATE user_data
                             SET sending_rasp_5 = ?
                           WHERE id = ?''',
                       (int(on), user_id,))
    else:
        cursor.execute('''UPDATE user_data
                             SET sending_rasp = ?
                           WHERE id = ?''',
                       (int(on), user_id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()


def set_sending_zam(user_id, on=True):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''UPDATE user_data
                         SET sending_zam = ?
                       WHERE id = ?''',
                   (int(on), user_id,))
    sql_con.commit()
    cursor.close()
    sql_con.close()


def get_rate_statistics():
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT sum(rate), count(id) 
                        FROM user_data
                       WHERE rate != 0''')
    data = cursor.fetchone()
    cursor.close()
    sql_con.close()
    if data[0] is None:
        return None
    else:
        return [data[0] / data[1], data[1]]


def set_rate(user_id, count_of_stars):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''UPDATE user_data
                         SET rate = ?
                       WHERE id = ?''',
                   (int(count_of_stars), user_id))
    sql_con.commit()
    cursor.close()
    sql_con.close()


def get_statistics_for_admin():
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()

    cursor.execute('''SELECT count(id)
                        FROM user_data''')
    data = cursor.fetchone()[0]

    cursor.close()
    sql_con.close()
    return data


def get_user_rate(user_id):
    sql_con = connect(const.path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT rate
                        FROM user_data
                       WHERE id = ?''', (user_id,))
    rate = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()
    return rate
