# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import sys
import config as conf
import datetime as dt
from time import sleep
import functions as func
import constants as const
from telebot import TeleBot
from sqlite3 import connect


bot = TeleBot(conf.token)


def main(date):
    id_real_sendig = []
    full_date = [False, False]

    sql_con = connect(const.path + 'Bot.db')
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

    sql_con = connect(const.path + 'Bot.db')
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
            week = func.get_week()
            group = func.get_student_group(irs)
            day_of_week = dt.datetime.isoweekday(dt.datetime.now())

            answer = 'Расписание на завтра:\n\n'
            answer += const.emoji['calendar'] + ' '
            answer += const.num_day[str(dt.datetime.isoweekday(dt.datetime.now() +
                                                               dt.timedelta(days=1)))] + \
                ', '
            full_date = func.get_date(True)
            answer += full_date[0] + '\n'
            td = 1

            if day_of_week == 7:
                if week == 'DOWN':
                    answer += const.up_week
                    week = 'UP'
                elif week == 'UP':
                    answer += const.down_week
                    week = 'DOWN'
            else:
                if week == 'UP':
                    answer += const.up_week
                elif week == 'DOWN':
                    answer += const.down_week

            answer += const.notify

            if func.get_alias(irs) == 'PREP':
                try:
                    day_info = const.teachers_shedule[
                        const.teacher_name[const.cap_teachers.index(group)]]
                except:
                    bot.send_message(conf.my_id,  str(dt.datetime.now())[:-7] +
                                     ' | ' + 'Ошибка при рассылке расписания '
                                     'для {} "<b>({})</b>"\U00002026:'
                                     '\n\n'.format(str(irs),
                                                   group) +
                                     str(sys.exc_info()[1]))
            else:
                try:
                    day_info = const.shedule[group]
                except:
                    bot.send_message(conf.my_id,  str(dt.datetime.now())[:-7] +
                                     ' | ' + 'Ошибка при рассылке расписания '
                                     'для {} "<b>({})</b>"\U00002026:'
                                     '\n\n'.format(str(irs),
                                                   group) +
                                     str(sys.exc_info()[1]))

            day_info = day_info[week][dt.datetime.isoweekday(dt.datetime.now() +
                                                             dt.timedelta(
                days=td)) - 1]
            if day_info:
                answer += func.get_shedule_answer(day_info, full_date[1])
            else:
                continue

            try:
                bot.send_message(irs, answer, parse_mode='HTML')
            except Exception as err:
                print(err)
                bot.send_message(conf.my_id, const.emoji['cross_mark'] +
                                 ' ' + str(irs) + '\n' + str(err))
                continue
            sleep(0.04)
    else:
        sys.exit()


if __name__ == '__main__':
    main(dt.datetime.strftime(dt.datetime.now(), '%H'))
