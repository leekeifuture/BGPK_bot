# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import re
import os
import config as conf
from xlrd import open_workbook
from collections import Counter


path = os.environ['PATH_TO_BOT_DIRECTORY']

collage_folder = path + '/collage constants/'

admin_ids = [conf.my_id, '650459589']

types = [
    {'Alias': 'STUD',
     'Type': 'Студент'},
    {'Alias': 'PREP',
     'Type': 'Преподаватель'}
]

divisions = [
    {'Alias': 'STR',
     'Name': 'Строительное'},
    {'Alias': 'RAD',
     'Name': 'Радиотехническое'},
    {'Alias': 'MEH',
     'Name': 'Машиностроительное'},
    {'Alias': 'YUR',
     'Name': 'Юридическое'}
]

brly_aliases = {
    'с': 'STR',
    'м': 'MEH',
    'р': 'RAD',
    'ю': 'YUR'
}


courses = [
    {'Alias': '1',
     'Course': '1 курс'},
    {'Alias': '2',
     'Course': '2 курс'},
    {'Alias': '3',
     'Course': '3 курс'},
    {'Alias': '4',
     'Course': '4 курс'}
]

m50ids = [365801236, 506847762, 463689495, 582869971, 563494209, 381876582,
          491845617, 409009767, 464698301, 537814999, 399890621, 500579682,
          647609231, 453781809, 432291179, 425439946, 600882503, 464215311,
          428850916, 791896398, 792220753, 475086724, 617493936, 295057002]

student_groups = [
    {'STR1':
        [
            {'StudentGroupName': 'С88'},
            {'StudentGroupName': 'С89'},
            {'StudentGroupName': 'Ср24'}
        ]
     },
    {'STR2':
        [
            {'StudentGroupName': 'С86'},
            {'StudentGroupName': 'С87'},
            {'StudentGroupName': 'Ср23'}
        ]
     },
    {'STR3':
        [
            {'StudentGroupName': 'С84'},
            {'StudentGroupName': 'С85'},
            {'StudentGroupName': 'Ср22'}
        ]
     },
    {'STR4':
        [
            {'StudentGroupName': 'С81'},
            {'StudentGroupName': 'С82'},
            {'StudentGroupName': 'С83'},
            {'StudentGroupName': 'Ср21'}
        ]
     },
    {'RAD1':
        [
            {'StudentGroupName': 'Р55'},
            {'StudentGroupName': 'Р56'},
            {'StudentGroupName': 'Э1'}
        ]
     },
    {'RAD2':
        [
            {'StudentGroupName': 'Р53'},
            {'StudentGroupName': 'Р54'}
        ]
     },
    {'RAD3':
        [
            {'StudentGroupName': 'Р51'},
            {'StudentGroupName': 'Р52'}
        ]
     },
    {'RAD4':
        [
            {'StudentGroupName': 'Р49'},
            {'StudentGroupName': 'Р50'}
        ]
     },
    {'MEH1':
        [
            {'StudentGroupName': 'М59'},
            {'StudentGroupName': 'М60'}
        ]
     },
    {'MEH2':
        [
            {'StudentGroupName': 'М56'},
            {'StudentGroupName': 'М57'},
            {'StudentGroupName': 'Мс58'}
        ]
     },
    {'MEH3':
        [
            {'StudentGroupName': 'М53'},
            {'StudentGroupName': 'М54'},
            {'StudentGroupName': 'Мс55'}
        ]
     },
    {'MEH4':
        [
            {'StudentGroupName': 'М50'},
            {'StudentGroupName': 'М51'},
            {'StudentGroupName': 'Мс52'}
        ]
     },
    {'YUR1':
        [
            {'StudentGroupName': 'Ю46'}
        ]
     },
    {'YUR2':
        [
            {'StudentGroupName': 'Ю44'},
            {'StudentGroupName': 'Юс45'}
        ]
     },
    {'YUR3':
        [
            {'StudentGroupName': 'Ю43'}
        ]
     },
]


site_prefix = 'http://www.bspc.bstu.by/ru/uchashchimsya/zamena-zanyatij/'

ponedelnik = site_prefix + '169-zamena-ponedelnik'
vtornik = site_prefix + '170-zamena-vtornik'
sreda = site_prefix + '171-zamena-sreda'
chetverg = site_prefix + '172-zamena-chetverg'
pyatnica = site_prefix + '173-zamena-pyatnica'
subotta = site_prefix + '174-zamena-subotta'

emoji = {
    'info': u'\U00002139', 'star': u'\U00002B50',
    'settings': u'\U00002699', 'suburban': u'\U0001F689',
    'editor': u'\U0001F4DD', 'alarm_clock': u'\U000023F0',
    'calendar': u'\U0001F4C5', 'sleep': u'\U0001F634',
    'clock': u'\U0001F552', 'cross_mark': u'\U0000274C',
    'check_mark': u'\U00002705', 'mailbox_off': u'\U0001F4EA',
    'mailbox_on': u'\U0001F4EB', 'door': u'\U0001F6AA',
    'school': u'\U0001F3EB', 'disappointed': u'\U0001F61E',
    'cold_sweat': u'\U0001F613', 'halo': u'\U0001F607',
    'smile': u'\U0001F604', 'bullet': u'\U00002022',
    'horns': u'\U0001F608', 'orange_diamond': u'\U0001F538',
    'blue_diamond': u'\U0001F539', 'runner': u'\U0001F3C3',
    'arrow_up': u'\U00002B06', 'arrow_down': u'\U00002B07',
    'warning': u'\U000026A0', 'arrows_counterclockwise': u'\U0001F504',
    'bust_in_silhouette': u'\U0001F464', 'back': u'\U0001F519',
    'mag_right': u'\U0001F50E', 'arrow_backward': u'\U000025C0',
    'arrow_forward': u'\U000025B6', 'star2': u'\U00002728',
    'new': u'\U0001F195', 'bell': u'\U0001F514',
    'page_facing_up': u'\U0001F4C4', 'anticlockwise': u'\U0001F504',
    'no_entry': u'\U0001F6AB', 'negative_squared_cross_mark': u'\U0000274E',
    'black_arrow': u'\U00002B05', 'five_oclock': u'\U0001F554',
    'nine_oclock': u'\U0001F558', 'warning_sign': u'\U000026A0',
    'magnifying_glass': u'\U0001F50E', 'clock_8-9': u'\U0001F557',
    'clock_9-11': u'\U0001F558', 'clock_11-13': u'\U0001F55A',
    'clock_14-16': u'\U0001F551', 'clock_16-18': u'\U0001F553',
    'clock_18-19': u'\U0001F555', 'envelope': u'\U00002709'
}

briefly_info_answer = (
    'КРАТКАЯ ИНФОРМАЦИЯ\n\n'
    '<b>Раздел "{1} Замены"</b>\n'
    'Здесь ты можешь <i>узнать изменения в расписании</i> на любой день '
    'недели.\n\n'
    '<b>Раздел "{2}"</b>\n'
    'Здесь ты можешь <i>сменить группу</i> или <i>завершить работу</i> с '
    'ботом.\n\n'
    '<b>Раздел "{3}"</b>\n'
    'Здесь ты можешь <i>оценить бота</i> и посмотреть <i>средний балл</i> '
    'оценок пользователей.\n\n'
    '<b>Раздел "{4}"</b>\n'
    'Здесь ты можешь <i>подписаться</i> или <i>отписаться</i>  на ежедневную '
    'рассылку замен.\n\n'
    '<b>Раздел "{5}"</b>\n'
    'Здесь ты можешь <i>узнать расписание звонков</i> на ближайший '
    'учебный год.'
).format(emoji['page_facing_up'], emoji['anticlockwise'],
         emoji['settings'], emoji['star'],
         emoji['alarm_clock'], emoji['bell'])

full_info_answer = (
    'ИНФОРМАЦИЯ\n\n'
    '<b>Раздел "{9} Замены"</b>\n\n'
    '{10} Информация об изменениях в расписании с <b>официального сайта '
    'БГПК</b> – http://www.bspc.brest.by\n'
    '{11} При отправке команды "Завтра" в субботу, а также '
    'при отправке "Сегодня" в воскресенье, бот пришлёт замены на '
    '<b>понедельник</b>.\n'
    '{12} Кнопка "{13}" позволит просматривать замены для определённого '
    '<b>направления/курса/группы/преподавателя</b>.'
    '{14} Так же можно <i>подписаться на рассылку</i> замен – {15}\n '
    'Рассылка производится каждый день в то же время когда замены вывесили '
    'на сайте. Максимальная задержка между сайтом и ботом – '
    '<b>1 минута</b>.\n\n'
    '<b>Раздел "{16}"</b>\n\n'
    '{17} Можно вызвать командой /settings.\n'
    '{18} Во время <i>смены группы</i> можно воспользоваться командой '
    '<b>Назад</b> (или /home) для возврата в <i>Главное меню</i>.\n'
    '{19} Если ты решишь прекратить пользоваться ботом, пожалуйста, '
    '<b>заверши работу</b> с ним (для этого необходимо написать /exit или '
    'выбрать <b>“Завершить работу”</b> в меню настроек. Просто удалить '
    'диалог недостаточно). Боту очень тяжело всех помнить, и ты, решив '
    'больше не использовать его, таким образом облегчишь ему работу.\n\n'
    '<b>Раздел "{20}"</b>\n\n'
    '{21} Можешь <b>оценить</b> бота по пятибалльной шкале (от "неуд" '
    'до "отлично")  или посмотреть <i>средний балл</i> оценок других '
    'пользователей.\n\n<b>Идейный вдохновитель</b> – @Spbu4UBot'
).format(emoji['page_facing_up'], emoji['bullet'], emoji['bullet'],
         emoji['bullet'], emoji['bust_in_silhouette'], emoji['bullet'],
         emoji['bullet'], emoji['alarm_clock'], emoji['bullet'],
         emoji['anticlockwise'], emoji['bullet'], emoji['bullet'],
         emoji['bullet'], emoji['magnifying_glass'], emoji['bullet'],
         emoji['alarm_clock'], emoji['settings'], emoji['bullet'],
         emoji['bullet'], emoji['bullet'], emoji['star'], emoji['bullet'])

up_week = emoji['arrow_up'] + ' Верхняя неделя\n\n'
down_week = emoji['arrow_down'] + ' Нижняя неделя\n\n'

week_day_number = {'Пн': 1, 'Вт': 2, 'Ср': 3, 'Чт': 4, 'Пт': 5, 'Сб': 6}

week_day_number_replacements = {
    1: ponedelnik,
    2: vtornik,
    3: sreda,
    4: chetverg,
    5: pyatnica,
    6: subotta,
    7: ponedelnik,
    8: ponedelnik
}

week_day_titles = {
    'понедельник': 'Пн', 'вторник': 'Вт', 'среду': 'Ср',
    'четверг': 'Чт', 'пятницу': 'Пт', 'субботу': 'Сб'
}

num_day = {
    '1': 'Понедельник', '2': 'Вторник', '3': 'Среда',
    '4': 'Четверг', '5': 'Пятница', '6': 'Суббота'
}

num_day_titles = {
    '1': 'Пн', '2': 'Вт', '3': 'Ср',
    '4': 'Чт', '5': 'Пт', '6': 'Сб'
}

week_days = ['понедельник', 'вторник', 'среда',
             'четверг',     'пятница', 'суббота']

day_list = [
    'первое', 'второе', 'третье', 'четвёртое', 'пятое', 'шестое', 'седьмое',
    'восьмое', 'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
    'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
    'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
    'двадцать первое', 'двадцать второе', 'двадцать третье',
    'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
    'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
    'тридцатое', 'тридцать первое'
]

month_list = [
    'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
    'августа', 'сентября', 'октября', 'ноября', 'декабря'
]

month_only_list = {
    1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь',
    7: 'июль', 8: 'август', 9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'
}

lesson_time = {
    '1': '08:00–09:40',
    '2': '09:50–11:30',
    '3': '11:50–13:30',
    '4': '14:25–16:05',
    '5': '16:25–18:05',
    '6': '18:15–19:55',
    '3s': '11:40–13:20',
    '4s': '13:35–15:15',
    '5s': '15:25–17:05',
    '6s': '17:15–18:55'
}

abridged_lesson_time = {
    '1': '08:00–09:00',
    '2': '09:10–10:10',
    '3': '10:20–11:20',
    '4': '11:30–12:30',
    '5': '12:40–13:40',
    '6': '13:50–14:50'
}

calls_pnpt = '''
1 смена:               2 смена:

1                              \
4
08:00–08:45         14:25–15:10
08:55–09:40         15:20–16:05
2                              \
5
09:50–10:35         16:25–17:10
10:45–11:30         17:20–18:05
3                              \
6
11:50–12:35         18:15–19:00
12:45–13:30         19:10–19:55
'''

calls_sb = '''
1 смена:               2 смена:

1                              \
4
08:00–08:45         13:35–14:20
08:55–09:40         14:30–15:15
2                              \
5
09:50–10:35         15:25–16:10
10:45–11:30         16:20–17:05
3                              \
6
11:40–12:25         17:15–18:00
12:35–13:20         18:10–18:55
'''

calls_sokr = '''
1 смена:               2 смена:

1                              \
4
08:00–09:00         11:30–12:30
2                              \
5
09:10–10:10         12:40–13:40
3                              \
6
10:20–11:20         13:50–14:50
'''

calls_sokrs = '''
1 смена:               2 смена:

1                              \
4
10:00–11:00         13:30–14:30
2                              \
5
11:10–12:10         14:40–15:40
3                              \
6
12:20–13:20         15:50–16:50
'''

not_events = 'Нет событий'

not_events_for_teachers = 'Нет событий'

notify = ''


table_lessons = {}
lessons_workbook = open_workbook(collage_folder + '/lessons/Lessons.xls')
lessons_sheet = lessons_workbook.sheet_by_index(0)
for i in range(lessons_sheet.nrows):
    table_lessons[lessons_sheet.cell_value(i, 1).replace(' ', '').lower()] = (
        lessons_sheet.cell_value(i, 0).strip())


teachers = {}
teachers_workbook = open_workbook(collage_folder + '/teachers/Teachers.xls')
teachers_sheet = teachers_workbook.sheet_by_index(0)
for i in range(teachers_sheet.nrows):
    table_teacher = teachers_sheet.cell_value(i, 0).strip()

    if table_teacher:
        teachers[str(i + 1)] = table_teacher.replace('ё', 'е')

sub_pattern = r'[^\w+]'
pattern = re.compile(r'\w+')


cap_teachers = [teachers[str(i)] for i in teachers.keys()]

low_teachers = [teachers[str(i)].replace(' ', '').lower()
                for i in teachers.keys()]

sht_teachers = []
for i in teachers.keys():
    sp_te = teachers[str(i)].split()
    sht_teachers.append(sp_te[0] + ' ' +
                        sp_te[1][0] + '. ' +
                        sp_te[2][0] + '.')

teacher_name = []
for i in teachers.keys():
    sp_te = teachers[str(i)].split()
    teacher_name.append(sp_te[0] + ' ' +
                        sp_te[1][0] + '. ' +
                        sp_te[2][0] + '.')

duplicate = [item for item, count in Counter(
    teacher_name).items() if count > 1]
if duplicate:
    seen = set()
    result = []
    for idx, item in enumerate(teacher_name):
        if item not in seen:
            seen.add(item)
        else:
            result.append(idx)

    for i in duplicate:
        index = teacher_name.index(i)
        for ind in result:
            if teacher_name[index] == teacher_name[ind]:
                sp_te = cap_teachers[ind].split()
                teacher_name[ind] = (
                    sp_te[0] + ' ' +
                    sp_te[1][:2] + '. ' +
                    sp_te[2][:2] + '.')
        sp_te = cap_teachers[index].split()
        teacher_name[index] = (
            sp_te[0] + ' ' +
            sp_te[1][:2] + '. ' +
            sp_te[2][:2] + '.')

## TABLE ##

table_cap_teachers = [teachers[str(i)] for i in teachers.keys()]

table_low_teachers = [teachers[str(i)].replace(' ', '').lower()
                      for i in teachers.keys()]

table_sht_teachers = []
for i in teachers.keys():
    sp_te = teachers[str(i)].split()
    table_sht_teachers.append(sp_te[0] + ' ' +
                              sp_te[1][0] + '. ' +
                              sp_te[2][0] + '.')

table_teacher_name = []
for i in teachers.keys():
    sp_te = teachers[str(i)].split()
    table_teacher_name.append(sp_te[0] + ' ' +
                              sp_te[1][0] + '. ' +
                              sp_te[2][0] + '.')

duplicate = [item for item, count in Counter(
    table_teacher_name).items() if count > 1]
if duplicate:
    seen = set()
    result = []
    for idx, item in enumerate(table_teacher_name):
        if item not in seen:
            seen.add(item)
        else:
            result.append(idx)

    for i in duplicate:
        index = table_teacher_name.index(i)
        for ind in result:
            if table_teacher_name[index] == table_teacher_name[ind]:
                sp_te = table_cap_teachers[ind].split()
                table_teacher_name[ind] = (
                    sp_te[0] + ' ' +
                    sp_te[1][:2] + '. ' +
                    sp_te[2][:2] + '.')
        sp_te = table_cap_teachers[index].split()
        table_teacher_name[index] = (
            sp_te[0] + ' ' +
            sp_te[1][:2] + '. ' +
            sp_te[2][:2] + '.')


existing_groups = []
for student_group in student_groups:
    for alias in student_group:
        for group in student_group[alias]:
            existing_groups.append(group['StudentGroupName'])

existing_courses = [course['Course'] for course in courses]

existing_divisions = [division['Name'] for division in divisions]

existing_types = [type['Type'] for type in types]


def resub(data):
    return re.sub(' +', ' ', data.strip())


def cls(data):
    return str(data).replace(' ', '').lower()


schedule = {}

for _, _, files in os.walk(collage_folder + '/groups/'):
    files = [f for f in files if not f[0] == '.']

for file in files:
    groups_workbook = open_workbook(
        '%s%s' % (collage_folder + '/groups/', file))
    groups_sheet = groups_workbook.sheet_by_index(0)

    if groups_sheet.ncols >= 3 and groups_sheet.nrows >= 2:
        table_grp = (cls(groups_sheet.cell_value(1, 2))
                     .replace('c', 'с')
                     .replace('s', 'с')
                     .replace('p', 'р')
                     .replace('m', 'м')
                     .replace('u', 'ю'))
        num_group = ''.join([i for i in table_grp if i.isdigit()])
        group = (table_grp.replace(num_group, '') + num_group).capitalize()

        if group in existing_groups:
            schedule[group] = {'UP': [[], [], [], [], [], []],
                               'DOWN': [[], [], [], [], [], []]}

for file in files:
    groups_workbook = open_workbook(
        '%s%s' % (collage_folder + '/groups/', file))
    groups_sheet = groups_workbook.sheet_by_index(0)

    table_grp = (cls(groups_sheet.cell_value(1, 2))
                 .replace('c', 'с')
                 .replace('s', 'с')
                 .replace('p', 'р')
                 .replace('m', 'м')
                 .replace('u', 'ю'))
    num_group = ''.join([i for i in table_grp if i.isdigit()])
    group = (table_grp.replace(num_group, '') + num_group).capitalize()

    day = 0
    for i in range(3, groups_sheet.nrows):
        day_of_week = cls(str(groups_sheet.cell_value(i, 1)).split('.')[0])

        if day_of_week in week_days:
            day += 1
        else:
            if day:
                if day_of_week.isdigit():
                    for row in [0, 2]:
                        lesson_row = cls(
                            groups_sheet.cell_value(i + row, 2))
                        teacher_row = cls(
                            groups_sheet.cell_value(i + 1 + row, 2))
                        half_lesson = cls(
                            lesson_row[1:]).split('/')
                        if groups_sheet.ncols >= 4:
                            audience = cls(str(groups_sheet.cell_value(
                                i + row, 3)).replace('.0', '').replace('с/з', 'спорт. зал'))
                        else:
                            audience = ''

                        if lesson_row:
                            if lesson_row[0] == '1':
                                week = 'UP'
                            elif lesson_row[0] == '2':
                                week = 'DOWN'

                            if day == 6 and (day_of_week != '1' and day_of_week != '2'):
                                lesson_day = str(day_of_week) + 's'
                            else:
                                lesson_day = str(day_of_week)

                            all_teachers = ''
                            for tchrs in cls(teacher_row).split('/'):
                                teacher_id = ''
                                for id in tchrs:
                                    if id.isdigit():
                                        teacher_id += id
                                    else:
                                        break

                                all_teachers += ' %s' % teacher_id

                            time = (
                                lesson_time[lesson_day])
                            lesson = (
                                '/'.join(set([resub(table_lessons[lssns]) for lssns in half_lesson])))
                            teachers = (
                                [resub(table_teacher_name[int(tchr_id) - 1]) for tchr_id in all_teachers[1:].split()])
                            if len(teachers) == len(set(teachers)):
                                teacher = '/'.join(teachers)
                            else:
                                teacher = '/'.join(set(teachers))
                                lesson += ' (делёжка)'
                            reserv = ''

                            day_student_shedule = (
                                reserv,
                                time,
                                lesson,
                                teacher,
                                audience,)

                            (schedule[group][week][day - 1]
                             .append(day_student_shedule))


teachers_shedule = {}

for teacher in teacher_name:
    teachers_shedule[teacher] = {'UP': [[], [], [], [], [], []],
                                 'DOWN': [[], [], [], [], [], []]}


existing_teachers = []

for group in existing_groups:
    for week in schedule[group]:
        for day in schedule[group][week]:
            for lesson_info in day:
                time = re.sub(' +', ' ', lesson_info[1].strip())
                lesson = re.sub(' +', ' ', lesson_info[2].strip())
                name_of_teacher = re.sub(' +', ' ', lesson_info[3].strip())
                audience = re.sub(' +', ' ', lesson_info[4].strip())

                for teacher in teacher_name:
                    valid_info = ''
                    div_teachers = name_of_teacher.split('/')

                    if audience.replace(' ', '').lower() != 'с/з':
                        if ('/' in audience and
                                '/' in name_of_teacher):
                            if (audience.count('/') ==
                                    name_of_teacher.count('/')):
                                consid = 0

                                for dived_teacher in div_teachers:
                                    if teacher == dived_teacher:
                                        valid_info = consid

                                    consid += 1

                    day_shedule = (valid_info,
                                   time,
                                   lesson,
                                   group,
                                   audience,)

                    if '/' in name_of_teacher:
                        if name_of_teacher in existing_teachers:
                            index = existing_teachers.index(name_of_teacher)
                            existing_teachers.remove(existing_teachers[index])

                        for dived_teacher in div_teachers:
                            if dived_teacher.strip() not in existing_teachers:
                                existing_teachers.append(dived_teacher.strip())

                            if teacher == dived_teacher:
                                (teachers_shedule[teacher][week]
                                 [schedule[group][week]
                                  .index(day)]
                                    .append(day_shedule))

                    if (name_of_teacher.strip() not in existing_teachers and
                            '/' not in name_of_teacher):
                        existing_teachers.append(name_of_teacher.strip())

                    if (teacher == name_of_teacher and
                            '/' not in name_of_teacher):
                        (teachers_shedule[teacher][week]
                         [schedule[group][week]
                          .index(day)]
                            .append(day_shedule))

remove_teachers = []

for teacher in teachers_shedule:
    week_status = []
    teacher_shedule = teachers_shedule[teacher]

    for week in teacher_shedule:
        day_of_week = teacher_shedule[week]
        week_len = [len(day) for day in day_of_week]

        if sum(week_len) == 0:
            week_status.append(0)

        if week == list(teacher_shedule.keys())[-1]:
            if week_status:
                if len(week_status) == 2 and sum(week_status) == 0:
                    remove_teachers.append(teacher)

        for day in day_of_week:
            day.sort(key=lambda lesson: lesson[1])

for teacher in remove_teachers:
    del teachers_shedule[teacher]
