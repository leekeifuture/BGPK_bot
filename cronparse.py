# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


from re import sub
import datetime as dt
import config as conf
from time import sleep
from sys import exc_info
import constants as const
from sqlite3 import connect
from telebot import TeleBot
from bs4 import BeautifulSoup
from urllib.request import urlopen
from functions import get_replacements_ansewer


bot = TeleBot(conf.token)

have_repl = []
not_have_repl = []


def get_html(url):
    try:
        response = urlopen(url)
        return response.read()
    except:
        print('\n\n' + str(dt.datetime.now())[:-7] + ' | ' +
              str(exc_info()[1]) + '\n\n')
        bot.send_message(conf.my_id, str(dt.datetime.now())[:-7] + ' | ' +
                         str(exc_info()[1]))
        exit()


def day_of_parsing_week(request_day, parse_day):
    if parse_day == dt.datetime.isoweekday(dt.datetime.now() + dt.timedelta(days=+1)):
        return 'завтра'
    elif parse_day == dt.datetime.isoweekday(dt.datetime.now()):
        return 'сегодня'
    else:
        if 'ponedelnik' in request_day.lower():
            return 'понедельник'
        elif 'vtornik' in request_day.lower():
            return 'вторник'
        elif 'sreda' in request_day.lower():
            return 'среду'
        elif 'chetverg' in request_day.lower():
            return 'четверг'
        elif 'pyatnica' in request_day.lower():
            return 'пятницу'
        elif 'subotta' in request_day.lower():
            return 'субботу'


def get_student_group(user_id):
    sql_con = connect(const.path + 'Bot_db')
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
    sql_con = connect('Bot_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT alias
                        FROM user_data
                       WHERE id = ?''', (chat_id,))
    data = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()
    return data


def parse(html, parse_day, request_day):

    try:
        soup = BeautifulSoup(sub(' +', ' ', html), 'lxml')
    except:
        print('\n\n' + str(dt.datetime.now())[:-7] + ' | ' +
              str(exc_info()[1]) + '\n\n')
        bot.send_message(conf.my_id, str(dt.datetime.now())[:-7] + ' | ' +
                         str(exc_info()[1]))
        exit()

    data = soup.find('div', class_='item-page')
    dataa = data.find_all('h1')
    dataaa = dataa[0].text.strip()

    a = dataaa[-10:].split('.')
    b = str(dt.datetime.today())[:-16].split('-')

    c = dt.datetime(int(a[2]), int(a[1]), int(a[0]))
    d = dt.datetime(int(b[0]), int(b[1]), int(b[2]))

    weekday = c.weekday() + 1

    sql_con = connect(const.path + 'Parse_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT pro_parsing_date
                        FROM parsing_days''')
    send_parse = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()

    if send_parse:
        exit()

    elif weekday == parse_day and c >= d:
        sql_con = connect(const.path + 'Parse_db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE parsing_days
                             SET pro_parsing_date = 1''')
        sql_con.commit()
        cursor.close()
        sql_con.close()

        sql_con = connect(const.path + 'Parse_db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE parsing_days
                             SET pro_parsing_day = ?''', (parse_day,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        print('\n' + str(dt.datetime.now())[:-7] + ' | ' + '!!! PARSING '
                   + str(weekday) + ' !!!' + '\n')

        try:
            all_page = soup.find_all('table')
        except:
            print('\n\n' + str(dt.datetime.now())[:-7] + ' | ' +
                  str(exc_info()[1]) + '\n\n')
            bot.send_message(conf.my_id, str(dt.datetime.now())[:-7] + ' | ' +
                             str(exc_info()[1]))
            exit()

        sql_con = connect(const.path + 'Parse_db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE zam_from_site
                             SET day_{} = ?'''.format(str(parse_day)),
                       (str(dataa) + str(all_page),))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        real_sendig = []
        sending_groups = []
        id_yes_repl_sendig = []
        id_non_repl_sending = []
        all_teachers = const.cap_teachers.copy()
        all_groups = const.existing_groups.copy()

        sql_con = connect(const.path + 'Bot_db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT id 
                            FROM user_data
                           WHERE sending_zam = 1''')
        sending_zam_one = list(cursor.fetchall())
        cursor.close()
        sql_con.close()

        sql_con = connect(const.path + 'Bot_db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT id_banned
                            FROM banned_users''')
        id_banned = cursor.fetchall()
        cursor.close()
        sql_con.close()

        for ib in id_banned:
            if ib[0] in sending_zam_one:
                sending_zam_one.remove(ib[0])

        for szo in sending_zam_one:
            sql_con = connect(const.path + 'Bot_db')
            cursor = sql_con.cursor()
            cursor.execute('''SELECT group_name 
                                FROM user_data 
                               WHERE id = ?''', (szo[0],))
            group1 = cursor.fetchone()[0]
            cursor.close()
            sql_con.close()
            if group1 not in sending_groups:
                sending_groups.append(group1)

        for sg in sending_groups:
            for tab in all_page:
                for row in tab.find_all('tr')[1:]:
                    if 'strong' in str(row):
                        continue
                    tmp = row.find_all('td')
                    group = tmp[0].text.strip().replace('\n', '') \
                        .replace(' ', '').lower()
                    teacher = tmp[4].text.strip().replace('\n', '') \
                        .replace(' ', '').replace('.', '').lower()

                    if group or teacher:
                        if any(map(str.isdigit, sg)):
                            if sg.lower() in group:
                                if sg not in real_sendig:
                                    real_sendig.append(sg)
                                if sg in all_groups:
                                    all_groups.remove(sg)
                        else:
                            short_name = sg.replace(' ', '').lower()

                            if short_name == 'панасюксергейстепанович':
                                db_surname = 'панасюксс'
                            elif short_name == 'панасюксветланасвятославовна':
                                db_surname = 'панасюксвсв'
                            else:
                                db_surname = sg.split()[0].replace(' ', '') \
                                    .lower()

                            if '/' in teacher:
                                site_teacher = teacher.split('/')
                            else:
                                site_teacher = [teacher]

                            for teacher in site_teacher:
                                if teacher == 'панасюксс':
                                    site_surname = teacher
                                elif teacher == 'панасюксвсв':
                                    site_surname = teacher
                                else:
                                    site_surname = teacher.split()[0]

                                if db_surname == site_surname:
                                    if sg not in real_sendig:
                                        real_sendig.append(sg)
                                    if sg in all_teachers:
                                        all_teachers.remove(sg)

        for rs in real_sendig:
            sql_con = connect(const.path + 'Bot_db')
            cursor = sql_con.cursor()
            cursor.execute('''SELECT id 
                                FROM user_data
                               WHERE sending_zam = 1
                                 AND group_name = ?''', (rs,))
            send_ids = cursor.fetchall()
            cursor.close()
            sql_con.close()
            for i in send_ids:
                if i not in id_yes_repl_sendig:
                    id_yes_repl_sendig.append(i[0])

        sql_con = connect(const.path + 'Bot_db')
        cursor = sql_con.cursor()
        cursor.execute('''SELECT id_banned
                            FROM banned_users''')
        id_banned = cursor.fetchall()
        cursor.close()
        sql_con.close()

        for ib in id_banned:
            if ib[0] in id_yes_repl_sendig:
                id_yes_repl_sendig.remove(ib[0])

        if id_yes_repl_sendig:
            for id_send_repl in id_yes_repl_sendig:

                sql_con = connect(const.path + 'Bot_db')
                cursor = sql_con.cursor()
                cursor.execute('''SELECT group_name 
                                    FROM user_data 
                                   WHERE id = ?
                                     AND sending_zam = 1''', (id_send_repl,))
                rs = cursor.fetchone()[0]
                cursor.close()
                sql_con.close()

                answer = ''
                for tab in all_page:
                    for row in tab.find_all('tr')[1:]:
                        if 'strong' in str(row):
                            continue

                        answer += get_replacements_ansewer(row, id_send_repl)

                answer = const.emoji['anticlockwise'] + \
                    ' ' + dataaa.capitalize() + answer

                try:
                    bot.send_message(id_send_repl, answer, parse_mode='HTML')
                    have_repl.append(id_send_repl)
                except Exception as err:
                    print(err)
                    bot.send_message(conf.my_id, const.emoji['cross_mark'] + ' ' +
                                     str(id_send_repl) + '\n' + str(err))
                    continue

                sleep(0.04)

        for ag in all_groups:
            sql_con = connect(const.path + 'Bot_db')
            cursor = sql_con.cursor()
            cursor.execute('''SELECT id 
                                FROM user_data
                               WHERE sending_zam = 1
                                 AND group_name = ?''', (ag,))
            send_none_repl_ids = cursor.fetchall()
            cursor.close()
            sql_con.close()
            for i in send_none_repl_ids:
                if i[0] not in id_non_repl_sending:
                    id_non_repl_sending.append(i[0])

        for at in all_teachers:
            sql_con = connect(const.path + 'Bot_db')
            cursor = sql_con.cursor()
            cursor.execute('''SELECT id 
                                FROM user_data
                               WHERE sending_zam = 1
                                 AND group_name = ?''', (at,))
            send_none_repl_ids = cursor.fetchall()
            cursor.close()
            sql_con.close()
            for i in send_none_repl_ids:
                if i[0] not in id_non_repl_sending:
                    id_non_repl_sending.append(i[0])

        for ib in id_banned:
            if ib[0] in id_non_repl_sending:
                id_non_repl_sending.remove(ib[0])

        if id_non_repl_sending:
            for inzs in id_non_repl_sending:
                group = get_student_group(inzs)
                if get_alias(inzs) == 'PREP':
                    index = const.cap_teachers.index(group)
                    for_any = 'преподавателя'
                    group = const.sht_teachers[index]
                else:
                    for_any = 'группы'

                try:
                    bot.send_message(inzs, const.emoji['anticlockwise'] +
                                     ' Для ' + for_any +
                                     ' <b>{}</b> нет замен на {} ('
                                     .format(group,
                                             day_of_parsing_week(request_day,
                                                                 parse_day)) +
                                     dataaa[-10:] + ').', parse_mode='HTML')
                    not_have_repl.append(inzs)
                except Exception as err:
                    print(err)
                    bot.send_message(conf.my_id, const.emoji['cross_mark'] + ' ' +
                                     str(inzs) + '\n' + str(err))
                    continue

                sleep(0.04)

        sql_con = connect(const.path + 'Parse_db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE parsing_days
                             SET pro_parsing_date = 0''')
        sql_con.commit()
        cursor.close()
        sql_con.close()

        shipped = have_repl + not_have_repl
        difference = len(sending_zam_one) - len(shipped)

        print('\n\n' + str(have_repl) + '\n\n' + str(not_have_repl) + '\n\n')
        print(str(len(sending_zam_one)) + ' - ' + str(len(shipped)))
        print(difference)

        exit()

    elif dt.datetime.strftime(dt.datetime.now(), '%H:%M') == '23:50' and \
        ((dt.datetime.isoweekday(dt.datetime.now()) == 6 and
          dataaa.replace(' ', '')[-10:][:2] == (dt.datetime.strftime(dt.date.today() +
                                                                     dt.timedelta(days=-5), '%d') or
                                                dt.datetime.strftime(dt.date.today() + dt.timedelta(days=-12), '%d'))) or
         (dt.datetime.isoweekday(dt.datetime.now()) != 6 and
          dataaa.replace(' ', '')[-10:][:2] == (dt.datetime.strftime(dt.date.today() +
                                                                     dt.timedelta(days=-6), '%d') or
                                                dt.datetime.strftime(dt.date.today() + dt.timedelta(days=-13), '%d')))):

        sql_con = connect(const.path + 'Parse_db')
        cursor = sql_con.cursor()
        cursor.execute('''UPDATE parsing_days
                             SET pro_parsing_day = ?''', (parse_day,))
        sql_con.commit()
        cursor.close()
        sql_con.close()

        print('\n\n' + str(dt.datetime.now())[:-7] + ' | ' +
              'Замены до сих пор не вывесили ' + '\n\n')
        bot.send_message(conf.my_id, str(dt.datetime.now())[:-7] + ' | ' +
                         'Замены до сих пор не вывесили')

        exit()

    else:
        exit()


def main():

    sql_con = connect(const.path + 'Parse_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT pro_parsing_date
                        FROM parsing_days''')
    send_parse = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()

    if send_parse:
        exit()

    sql_con = connect(const.path + 'Parse_db')
    cursor = sql_con.cursor()
    cursor.execute('''SELECT pro_parsing_day 
                        FROM parsing_days''')
    pro_parsing_day = cursor.fetchone()[0]
    cursor.close()
    sql_con.close()

    if pro_parsing_day == '1':
        parse(get_html(const.vtornik), 2, const.vtornik)
    elif pro_parsing_day == '2':
        parse(get_html(const.sreda), 3, const.sreda)
    elif pro_parsing_day == '3':
        parse(get_html(const.chetverg), 4, const.chetverg)
    elif pro_parsing_day == '4':
        parse(get_html(const.pyatnica), 5, const.pyatnica)
    elif pro_parsing_day == '5':
        parse(get_html(const.subotta), 6, const.subotta)
    elif pro_parsing_day == '6':
        parse(get_html(const.ponedelnik), 1, const.ponedelnik)


if __name__ == '__main__':
    main()
