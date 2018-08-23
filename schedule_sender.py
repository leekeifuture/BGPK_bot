# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import sys
import time
import config
import telebot
import sqlite3
from functions import get_date
from datetime import datetime, timedelta
from constants import emoji, num_day, notify, lesson_time, up_week, down_week, \
    shedule, cap_teachers, teacher_name, teachers_shedule


# path = ''
path = '/home/ubuntu/bot/'

bot = telebot.TeleBot(config.token)

id_real_sendig = []


def get_week():
    sql_con = sqlite3.connect(path + 'Bot_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT week 
                      FROM offer''')
    week = cursor.fetchone()
    cursor.close()
    sql_con.close()

    if datetime.today().isocalendar()[1] % 2 == 0 and week[0] == True:
        return 'DOWN'
    elif datetime.today().isocalendar()[1] % 2 == 0 and week[0] == False:
        return 'UP'
    elif datetime.today().isocalendar()[1] % 2 != 0 and week[0] == True:
        return 'UP'
    elif datetime.today().isocalendar()[1] % 2 != 0 and week[0] == False:
        return 'DOWN'


def get_student_group(user_id):
    sql_con = sqlite3.connect(path + 'Bot_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT group_name 
                      FROM user_data 
                      WHERE id = ?''', (user_id,))
    data_group = cursor.fetchone()
    cursor.close()
    sql_con.close()
    try:
        return data_group[0]
    except:
        return ''


def get_alias(chat_id):
    sql_con = sqlite3.connect(path + 'Bot_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT alias
                        FROM user_data
                       WHERE id = ?''', (chat_id,))
    data = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()

    return data


def get_shedule_answer(day_info):
    answer = ''

    for lesson_info in day_info:
        time = lesson_info[1]
        lesson = lesson_info[2].strip()
        teacher = lesson_info[3].strip()
        audience = lesson_info[4].strip()
        valid_info = lesson_info[0]

        if lesson.strip():
            answer += emoji['clock'] + ' ' + time
            lesson_num = ''
            if time == lesson_time['1']:
                lesson_num = '1.'
            elif time == lesson_time['2']:
                lesson_num = '2.'
            elif (time == lesson_time['3'] or
                    time == lesson_time['3s']):
                lesson_num = '3.'
            elif (time == lesson_time['4'] or
                    time == lesson_time['4s']):
                lesson_num = '4.'
            elif (time == lesson_time['5'] or
                    time == lesson_time['5s']):
                lesson_num = '5.'
            elif (time == lesson_time['6'] or
                    time == lesson_time['6s']):
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


def schedule_sender(date):

    sql_con = sqlite3.connect(path + 'Bot_db')
    cursor = sql_con.cursor()
    if date == '21':
        cursor.execute('''SELECT id 
                            FROM user_data
                            WHERE sending_rasp = 1''')
    elif date == '17':
        cursor.execute('''SELECT id 
                            FROM user_data
                            WHERE sending_rasp_5 = 1''')
    sending_rasp_one = cursor.fetchall()
    cursor.close()
    sql_con.close()

    for sro in sending_rasp_one:
        if sro[0] not in id_real_sendig:
            id_real_sendig.append(sro[0])

    sql_con = sqlite3.connect(path + 'Bot_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT id_banned
                        FROM banned_users''')
    id_banned = cursor.fetchall()
    sql_con.commit()
    cursor.close()
    sql_con.close()

    for ib in id_banned:
        if ib[0] in id_real_sendig:
            id_real_sendig.remove(ib[0])

    if id_real_sendig:
        for irs in id_real_sendig:
            week = get_week()
            group = get_student_group(irs)
            day_of_week = datetime.isoweekday(datetime.now())

            answer = 'Расписание на завтра:\n\n'
            answer += emoji['calendar'] + ' '
            answer += num_day[str(datetime.isoweekday(datetime.now() +
                                                      timedelta(days=1)))] + \
                ', '
            answer += get_date(True)[0] + '\n'
            td = 1

            if day_of_week == 7:
                if week == 'DOWN':
                    answer += up_week
                    week = 'UP'
                elif week == 'UP':
                    answer += down_week
                    week = 'DOWN'
            else:
                if week == 'UP':
                    answer += up_week
                elif week == 'DOWN':
                    answer += down_week

            answer += notify

            if get_alias(irs) == 'PREP':
                try:
                    day_info = teachers_shedule[
                        teacher_name[cap_teachers.index(group)]]
                except:
                    bot.send_message(config.my_id,  str(datetime.now())[:-7] +
                                     ' | ' + 'Ошибка при рассылке расписания '
                                     'для {} "<b>({})</b>"\U00002026:'
                                     '\n\n'.format(str(irs),
                                                   group) +
                                     str(sys.exc_info()[1]))
            else:
                try:
                    day_info = shedule[group]
                except:
                    bot.send_message(config.my_id,  str(datetime.now())[:-7] +
                                     ' | ' + 'Ошибка при рассылке расписания '
                                     'для {} "<b>({})</b>"\U00002026:'
                                     '\n\n'.format(str(irs),
                                                   group) +
                                     str(sys.exc_info()[1]))

            day_info = day_info[week][datetime.isoweekday(datetime.now() +
                                                          timedelta(
                                                              days=td)) - 1]
            if day_info:
                answer += get_shedule_answer(day_info)
            else:
                continue

            try:
                bot.send_message(irs, answer, parse_mode='HTML')
            except Exception as err:
                print(err)
                bot.send_message(config.my_id, emoji['cross_mark'] +
                                 ' ' + str(irs) + '\n' + str(err))
                continue
            time.sleep(0.04)
    else:
        exit()


if __name__ == '__main__':
    schedule_sender(datetime.strftime(datetime.now(), '%H'))
