# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import re
from os import walk
from os import environ
from platform import version
from xlrd import open_workbook
from collections import Counter


def cls(data):
    return str(data).replace(' ', '').lower()


vers = version()

path = environ['path_to_bot_directory']

collage_folder = path + '/collage constants/'

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

# gep_workbook = open_workbook(collage_folder + '/gep/gep.xls')
# gep_sheet = gep_workbook.sheet_by_index(0)

# student_groups = []

# for row in range(9, gep_sheet.nrows):
#     gep_group = gep_sheet.cell_value(row, 1)

#     als = ''
#     crse_grps = []
#     if gep_group:
#         gep_cource = str(gep_sheet.cell_value(row, 2)).replace('.0', '')
#         alias = brly_aliases[cls(gep_group)[0]] + gep_cource

#         print({alias: [{'StudentGroupName': i} for i in crse_grps]})
#         print({brly_aliases[gep_group.lower()[0]] + str(gep_cource).replace('.0', ''): [for i in crse_grps]})


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

student_groups = [
    {'STR1':
        [
            {'StudentGroupName': 'С86'},
            {'StudentGroupName': 'С87'},
            {'StudentGroupName': 'Ср23'}
        ]
     },
    {'STR2':
        [
            {'StudentGroupName': 'С84'},
            {'StudentGroupName': 'С85'},
            {'StudentGroupName': 'Ср22'}
        ]
     },
    {'STR3':
        [
            {'StudentGroupName': 'С81'},
            {'StudentGroupName': 'С82'},
            {'StudentGroupName': 'С83'},
            {'StudentGroupName': 'Ср21'}
        ]
     },
    {'RAD1':
        [
            {'StudentGroupName': 'Р53'},
            {'StudentGroupName': 'Р54'}
        ]
     },
    {'RAD2':
        [
            {'StudentGroupName': 'Р51'},
            {'StudentGroupName': 'Р52'}
        ]
     },
    {'RAD3':
        [
            {'StudentGroupName': 'Р49'},
            {'StudentGroupName': 'Р50'}
        ]
     },
    {'RAD4':
        [
            {'StudentGroupName': 'Р47'},
            {'StudentGroupName': 'Р48'}
        ]
     },
    {'MEH1':
        [
            {'StudentGroupName': 'М56'},
            {'StudentGroupName': 'М57'}
        ]
     },
    {'MEH2':
        [
            {'StudentGroupName': 'М53'},
            {'StudentGroupName': 'М54'},
            {'StudentGroupName': 'Мс55'}
        ]
     },
    {'MEH3':
        [
            {'StudentGroupName': 'М50'},
            {'StudentGroupName': 'М51'},
            {'StudentGroupName': 'Мс52'}
        ]
     },
    {'YUR1':
        [
            {'StudentGroupName': 'Ю44'}
        ]
     },
    {'YUR2':
        [
            {'StudentGroupName': 'Ю43'}
        ]
     },
    {'YUR3':
        [
            {'StudentGroupName': 'Ю41'},
            {'StudentGroupName': 'Юс42'}
        ]
     }
]

teachers = {
    '1': 'Андросюк Виктор Валерьевич',
    '2': 'Антонюк Александр Иванович',
    '3': 'Барбачева Валентина Владимировна',
    '4': 'Басалаев Альберт Николаевич',
    '5': 'Басова Ирина Константиновна',
    '6': 'Панасюк Диана Юрьевна',
    '7': 'Бешанова Наталья Юрьевна',
    '8': 'Бойко Любовь Павловна',
    '9': 'Василевская Елена Алексеевна',
    '10': 'Васильев Иван Сергеевич',
    '11': 'Вацкель Ольга Ивановна',
    '12': 'Винников Валерий Ильич',
    '13': 'Вишняков Ростислав Владимирович',
    '14': 'Войтович Татьяна Григорьевна',
    '15': 'Гарах Татьяна Алексеевна',
    '16': 'Гордейчук Инна Викторовна',
    '17': 'Громишук Светлана Васильевна',
    '18': 'Деркач Евгений Александрович',
    '19': 'Дмитрук Петр Николаевич',
    '20': 'Дубяга Валентина Григорьевна',
    '21': 'Дунькович Сергей Анатольевич',
    '22': 'Дусенок Светлана Васильевна',
    '23': 'Жаден Наталья Ивановна',
    '24': 'Замковец Людмила Сергеевна',
    '25': 'Изотко Валентина Семеновна',
    '26': 'Кирилюк Александр Сергеевич',
    '27': 'Клухина Галина Николаевна',
    '28': 'Клюкач Виталий Николаевич',
    '29': 'Ковалько Сергей Владимирович',
    '30': 'Корделюк Анна Анатольевна',
    '31': 'Корнилович Инна Вячеславовна',
    '32': 'Корнилюк Дмитрий Анатольевич',
    '33': 'Приходько Валентина Генриковна',
    '34': 'Коротынский Федор Петрович',
    '35': 'Корсак Елена Ивановна',
    '36': 'Кузнецова Елена Тадеушевна',
    '37': 'Кузьмицкий Филипп Степанович',
    '38': 'Лапин Владимир Владимирович',
    '39': 'Левданский Юрий Маратович',
    '40': 'Лукьянова Людмила Мечиславовна',
    '41': 'Марзан Светлана Викторовна',
    '42': 'Маркина Светлана Владимировна',
    '43': 'Мартышевич Татьяна Николаевна',
    '44': 'Масловская Людмила Ростиславовна',
    '45': 'Мельникова Ольга Анатольевна',
    '46': 'Мемех Николай Павлович',
    '47': 'Мигель Наталья Ивановна',
    '48': 'Миласердов Александр Иванович',
    '49': 'Миронюк Елена Александровна',
    '50': 'Мирошниченко Дмитрий Иванович',
    '51': 'Нестерович Евгений Николаевич',
    '52': 'Новик Александра Сергеевна',
    '53': 'Носова Светлана Петровна',
    '54': 'Носова Татьяна Александровна',
    '55': 'Омеленецкая Жанна Петровна',
    '56': 'Осинченко Мария Николаевна',
    '57': 'Осипенко Ирина Павловна',
    '58': 'Осипук Галина Михайловна',
    '59': 'Панасюк Виктор Владимирович',
    '60': 'Панасюк Светлана Святославовна',
    '61': 'Панасюк Сергей Степанович',
    '62': 'Пархоменкова Анастасия Васильевна',
    '63': 'Радкевич Марина Валерьевна',
    '64': 'Ратникова Нина Викторовна',
    '65': 'Седлавский Степан Иванович',
    '66': 'Тарима Виталий Александрович',
    '67': 'Тельминов Леонид Корнилович',
    '68': 'Топоренко Елена Константиновна',
    '69': 'Трубей Татьяна Ивановна',
    '70': 'Тухто Николай Иванович',
    '71': 'Тысевич Светлана Сергеевна',
    '72': 'Уланова Наталья Петровна',
    '73': 'Хмарук Дина Викторовна',
    '74': 'Хоменко Анна Игоревна',
    '75': 'Храпунова Марина Олеговна',
    '76': 'Черенович Дмитрий Вяечславович',
    '77': 'Чудук Виктор Александрович',
    '78': 'Шамарина Елена Александровна',
    '79': 'Шахнюк Ольга Александровна',
    '80': 'Ширинга Иван Иванович',
    '81': 'Шпиганович Жанна Николаевна',
    '82': 'Щеперка Валерий Николаевич',
    '83': 'Ямпольская Надежда Дмитриевна',
    '84': 'Янкович Александр Леонидович',
    '85': 'Гац Екатерина Александровна',
    '86': 'Карпяк Татьяна Александровна',
    '87': 'Кульба Алексей Владимирович',
    '88': 'Кульбачинская Лилия Александровна',
    '89': 'Куровский Дмитрий Геннадьевич',
    '90': 'Селевоник Юлия Сергеевна',
    '91': 'Сергуцкая Светлана Сергеевна',
    '92': 'Сергуцкий Дмитрий Степанович',
    '93': 'Дакало Юрий Александрович',
    '94': 'Табала Александра Васильевна',
    '95': 'Кипень Марина Николаевна',
    '96': 'Басов Виктор Степанович',
    '97': 'Рачко Татьяна Леонидовна',
    '98': 'Старун Кирилл Николаевич',
    '99': 'Лукша Юлия Николаевна',
    '100': 'Петручик Игорь Александрович',
    '101': 'Марциновский Сергей Анатольевич',
    '102': 'Небелюк Анастасия Игоревна'
}


table_lessons = {}
lessons_workbook = open_workbook(collage_folder + '/lessons/Lessons.xls')
lessons_sheet = lessons_workbook.sheet_by_index(0)
for i in range(lessons_sheet.nrows):
    table_lessons[lessons_sheet.cell_value(i, 1).replace(' ', '').lower()] = (
        lessons_sheet.cell_value(i, 0).strip())


table_teachers = {}
teachers_workbook = open_workbook(collage_folder + '/teachers/Teachers.xls')
teachers_sheet = teachers_workbook.sheet_by_index(0)
for i in range(teachers_sheet.nrows):
    table_teacher = teachers_sheet.cell_value(i, 0).strip()

    if table_teacher:
        table_teachers[str(i + 1)] = table_teacher.replace('ё', 'е')

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

table_cap_teachers = [table_teachers[str(i)] for i in table_teachers.keys()]

table_low_teachers = [table_teachers[str(i)].replace(' ', '').lower()
                      for i in table_teachers.keys()]

table_sht_teachers = []
for i in table_teachers.keys():
    sp_te = table_teachers[str(i)].split()
    table_sht_teachers.append(sp_te[0] + ' ' +
                              sp_te[1][0] + '. ' +
                              sp_te[2][0] + '.')

table_teacher_name = []
for i in table_teachers.keys():
    sp_te = table_teachers[str(i)].split()
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

site_prefix = 'http://www.bspc.brest.by/ru/uchashchimsya/zamena-zanyatij/'

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
    '<b>Раздел "{0} Расписание"</b>\n'
    'Здесь ты можешь <i>узнать расписание</i> на любой день недели.\n\n'
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
    'рассылку расписания и замен.\n\n'
    '<b>Раздел "{5}"</b>\n'
    'Здесь ты можешь <i>узнать расписание звонков</i> на ближайший '
    'учебный год.'
).format(emoji['page_facing_up'], emoji['anticlockwise'],
         emoji['settings'], emoji['star'],
         emoji['alarm_clock'], emoji['bell'])

full_info_answer = (
    'ИНФОРМАЦИЯ\n\n'
    '<b>Раздел "{0} Расписание"</b>\n\n'
    '{1} Меню расписания позволит посмотреть расписание на любой день недели '
    'или на неделю полностью. После выбора дня бот пришлёт расписание для '
    '<b>текущей</b> недели, а также предложит посмотреть расписание для '
    '<b>верхней</b> и <b>нижней</b>.\n'
    '{2} Информация о паре формируется следующим образом:\n'
    '    Время\n'
    '    Порядковый номер пары. <b>Название пары</b> (кабинет)\n'
    '    <i>Фамилия И. О</i>. преподавателя или <i>Группа</i>\n'
    '    и т. д.\n'
    '{3} Кнопка "{4}" позволит просматривать <b>расписание для любого '
    'преподавателя на ''всю неделю</b>.\n'
    '{5} В любой день расписание смотрится по <b>текущей</b> неделе до '
    'ВОСКРЕСЕНЬЯ. В воскресенье расписание будет показано для следующей '
    'недели.\n'
    '{6} Так же можно <i>подписаться на рассылку</i> расписания – {7}\n '
    'Рассылка производится каждый день в 17:00 или 21:00. О выходных днях '
    'бот не уведомляет.\n'
    '{8} Если найдена ошибка в расписании просьба сразу сообщить об этом '
    '<a href="https://t.me/lee_kei">разработчику</a>.\n\n'
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

# shedule = {
#   'group': {
#       'UP': [
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3s'], '', teacher_name[], '')]
#         ],
#     'DOWN': [
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], ''),
#            ('', lesson_time['3'], '', teacher_name[], '')],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3'], '', teacher_name[], '',)],
#           [('', lesson_time['1'], '', teacher_name[], '',),
#            ('', lesson_time['2'], '', teacher_name[], '',),
#            ('', lesson_time['3s'], '', teacher_name[], '')]
#         ]
#     }
# }

# shedule = {
#   'group': {
#       'UP': [
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4s'], '', teacher_name[], ''),
#            ('', lesson_time['5s'], '', teacher_name[], ''),
#            ('', lesson_time['6s'], '', teacher_name[], '')]
#         ],
#     'DOWN': [
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4'], '', teacher_name[], '',),
#            ('', lesson_time['5'], '', teacher_name[], '',),
#            ('', lesson_time['6'], '', teacher_name[], '',)],
#           [('', lesson_time['4s'], '', teacher_name[], ''),
#            ('', lesson_time['5s'], '', teacher_name[], ''),
#            ('', lesson_time['6s'], '', teacher_name[], '')]
#         ]
#     }
# }


shedule = {
  'М56': {
      'UP': [
          [('', lesson_time['1'], 'Математика ', teacher_name[45], '202',),
           ('', lesson_time['2'], 'Биология', teacher_name[38], '212',),
           ('', lesson_time['3'], 'Белорусский язык', teacher_name[60], '20',)],
          [('', lesson_time['1'], 'Физика', teacher_name[16], '202',),
           ('', lesson_time['2'], 'Обществоведение', teacher_name[75], '202',),
           ('', lesson_time['3'], 'Допризывная подготовка', teacher_name[9], '119',)],
          [('', lesson_time['1'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[77], '315/314',),
           ('', lesson_time['2'], 'Астрономия', teacher_name[76], '207',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[2], '120',)],
          [('', lesson_time['1'], 'Физкультура и здоровье', teacher_name[31] + '/' + teacher_name[93], 'с/з',),
           ('', lesson_time['2'], 'Математика ', teacher_name[45], '202',),
           ('', lesson_time['3'], 'Химия', teacher_name[44], '212',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Русский язык', teacher_name[2], '120',),
           ('', lesson_time['3'], 'Всемирная история ', teacher_name[28], '121',)],
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Математика ', teacher_name[45], '111',),
           ('', lesson_time['3s'], 'Обществоведение ', teacher_name[75], '119')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Математика ', teacher_name[45], '202',),
           ('', lesson_time['2'], 'Биология', teacher_name[38], '212',),
           ('', lesson_time['3'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['4'], 'Физкультура и здоровье', teacher_name[31] + '/' + teacher_name[94], 'с/з',)],
          [('', lesson_time['1'], 'Физика', teacher_name[16], '202',),
           ('', lesson_time['2'], 'Обществоведение', teacher_name[75], '202',),
           ('', lesson_time['3'], 'Допризывная подготовка', teacher_name[9], '119',)],
          [('', lesson_time['1'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[77], '315/314',),
           ('', lesson_time['2'], 'Всемирная история ', teacher_name[28], '121',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[2], '120',)],
          [('', lesson_time['1'], 'Физкультура и здоровье', teacher_name[31] + '/' + teacher_name[93], 'с/з',),
           ('', lesson_time['2'], 'Математика ', teacher_name[45], '202',),
           ('', lesson_time['3'], 'Химия', teacher_name[44], '212',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Русский язык', teacher_name[2], '120',),
           ('', lesson_time['3'], 'Химия  ', teacher_name[44], '212',)],
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Математика ', teacher_name[45], '111',),
           ('', lesson_time['3s'], 'Всемирная история ', teacher_name[28], '121')]
        ]
    },
  'М57': {
      'UP': [
          [('', lesson_time['1'], 'Иностранный язык', teacher_name[21] + '/' + teacher_name[80], '318/321',),
           ('', lesson_time['2'], 'Обществоведение', teacher_name[28], '200',),
           ('', lesson_time['3'], 'Математика ', teacher_name[45], '202',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Допризывная подготовка', teacher_name[9], '119',),
           ('', lesson_time['3'], 'Химия', teacher_name[44], '212',)],
          [('', lesson_time['1'], 'Физкультура и здоровье', teacher_name[66] + '/' + teacher_name[57], 'с/з',),
           ('', lesson_time['2'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[56], '307',)],
          [('', lesson_time['1'], 'Математика ', teacher_name[45], '202',),
           ('', lesson_time['2'], 'Всемирная история ', teacher_name[28], '121',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[56], '307',)],
          [('', lesson_time['1'], 'Физика', teacher_name[16], '202',),
           ('', lesson_time['2'], 'Биология', teacher_name[38], '302',),
           ('', lesson_time['3'], 'Химия ', teacher_name[44], '212',)],
          [('', lesson_time['1'], 'Математика ', teacher_name[45], '120',),
           ('', lesson_time['2'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['3s'], 'Всемирная история ', teacher_name[28], '121')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Иностранный язык', teacher_name[21] + '/' + teacher_name[80], '318/321',),
           ('', lesson_time['2'], 'Обществоведение', teacher_name[28], '200',),
           ('', lesson_time['3'], 'Математика ', teacher_name[45], '202',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Допризывная подготовка', teacher_name[9], '119',),
           ('', lesson_time['3'], 'Химия', teacher_name[44], '212',)],
          [('', lesson_time['1'], 'Физкультура и здоровье', teacher_name[66] + '/' + teacher_name[57], 'с/з',),
           ('', lesson_time['2'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[56], '307',)],
          [('', lesson_time['1'], 'Математика ', teacher_name[45], '202',),
           ('', lesson_time['2'], 'Всемирная история ', teacher_name[28], '121',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[56], '307',)],
          [('', lesson_time['1'], 'Астрономия', teacher_name[76], '207',),
           ('', lesson_time['2'], 'Биология', teacher_name[38], '302',),
           ('', lesson_time['3'], 'Обществоведение ', teacher_name[28], '121',),
           ('', lesson_time['4'], 'Физкультура и здоровье', teacher_name[66] + '/' + teacher_name[57], 'с/з',)],
          [('', lesson_time['1'], 'Математика ', teacher_name[45], '120',),
           ('', lesson_time['2'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['3s'], 'Физика ', teacher_name[16], '202')]
        ]
    },
  'М53': {
      'UP': [
          [('', lesson_time['1'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['2'], 'Материалов.и техн.материал', teacher_name[82], '312',),
           ('', lesson_time['3'], 'Нормир.точн. и тех.измерен', teacher_name[26], '309',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['3'], 'Защита нас.и террит. от ЧС', teacher_name[40], '210',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['3'], 'Материалов.и техн.материал', teacher_name[82], '310',)],
          [('', lesson_time['1'], 'Русская литература', teacher_name[2], '120',),
           ('', lesson_time['2'], 'Физкультура и здоровье', teacher_name[66], 'с/з',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[21], '315/318',)],
          [('', lesson_time['1'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['2'], 'Нормир.точн. и тех.измерен/Техн.мех.', teacher_name[26] + '/' + teacher_name[25], '309/114',),
           ('', lesson_time['3'], 'САПР', teacher_name[25] + '/' + teacher_name[20], '114/205',)],
          [('', lesson_time['1'], 'Материал.и техн.материал', teacher_name[82], '319',),
           ('', lesson_time['2'], 'Белорусская литература', teacher_name[55], '309',),
           ('', lesson_time['3s'], 'Техническая механика', teacher_name[25], '111')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['2'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[21], '315/318',),
           ('', lesson_time['3'], 'Нормир.точн. и тех.измерен', teacher_name[26], '309',)],
          [('', lesson_time['1'], 'Материалов.и техн.мат/Техн.мех.', teacher_name[82] + '/' + teacher_name[25], '312/114',),
           ('', lesson_time['2'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['3'], 'ОСГН', teacher_name[63], '121',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['3'], 'Материалов.и техн.материал', teacher_name[82], '310',)],
          [('', lesson_time['1'], 'Русская литература', teacher_name[2], '120',),
           ('', lesson_time['2'], 'Физкультура и здоровье', teacher_name[66], 'с/з',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[21], '315/318',)],
          [('', lesson_time['1'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['2'], 'Нормир.точн. и тех.измерен/Техн.мех.', teacher_name[26] + '/' + teacher_name[25], '309/114',),
           ('', lesson_time['3'], 'Техническая механика', teacher_name[25], '111',)],
          [('', lesson_time['1'], 'Белорусская литература', teacher_name[55], '309',),
           ('', lesson_time['2'], 'Физкультура и здоровье', teacher_name[66], 'с/з',),
           ('', lesson_time['3s'], 'Техническая механика', teacher_name[25], '111')]
        ]
    },
  'М54': {
      'UP': [
          [('', lesson_time['1'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['2'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[21], '315/318',),
           ('', lesson_time['3'], 'Материалов.и техн.материал', teacher_name[82], '312',),
           ('', lesson_time['4'], 'Физическая культура', teacher_name[59], 'с/з',)],
          [('', lesson_time['1'], 'Материал.и техн.материал', teacher_name[82], '312',),
           ('', lesson_time['2'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[21], '315/318',)],
          [('', lesson_time['1'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['2'], 'Нормир.точн. и тех.измерен', teacher_name[26], '309',),
           ('', lesson_time['3'], 'Нормир.точн. и тех.измерен/Техн.мех.', teacher_name[26] + '/' + teacher_name[25], '309/114',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[56], '312',),
           ('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[59], 'с/з',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'САПР', teacher_name[1] + '/' + teacher_name[20], '205/311',),
           ('', lesson_time['3'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',)],
          [('', lesson_time['1'], 'ОСГН', teacher_name[75], '200',),
           ('', lesson_time['2'], 'Материал.и техн.материал', teacher_name[82], '319',),
           ('', lesson_time['3s'], 'Белорусская литература', teacher_name[55], '309')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['2'], 'Защита нас.и террит. от ЧС', teacher_name[40] + '/' + teacher_name[21], '312',),
           ('', lesson_time['3'], 'Материалов.и техн.материал', teacher_name[82], '312',)],
          [('', lesson_time['2'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[21], '315/318',)],
          [('', lesson_time['1'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',),
           ('', lesson_time['2'], 'Нормир.точн. и тех.измерен', teacher_name[26], '309',),
           ('', lesson_time['3'], 'Нормир.точн. и тех.измерен/Техн.мех.', teacher_name[26] + '/' + teacher_name[25], '309/114',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[56], '312',),
           ('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[59], 'с/з',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'ОСГН', teacher_name[75], '124',),
           ('', lesson_time['3'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[35], '319/200',)],
          [('', lesson_time['1'], 'ОСГН', teacher_name[75], '200',),
           ('', lesson_time['2'], 'Материалов.и техн.мат/Техн.мех.', teacher_name[82] + '/' + teacher_name[25], '319/114',),
           ('', lesson_time['3s'], 'Белорусская литература', teacher_name[55], '309')]
        ]
    },
  'Мс55': {
      'UP': [
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Нормир.точн. и тех.измерен/Техн.мех.', teacher_name[26] + '/' + teacher_name[25], '309/114',),
           ('', lesson_time['3'], 'Информационные технологии', teacher_name[49], '315',)],
          [('', lesson_time['1'], 'Материалов.и техн.материал', teacher_name[35], '210',),
           ('', lesson_time['2'], 'Защ.нас.и террит', teacher_name[40], '209',),
           ('', lesson_time['3'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[23], '319/321',)],
          [('', lesson_time['1'], 'Электротехн.с осн.электр.', teacher_name[29], '102',),
           ('', lesson_time['2'], 'САПР', teacher_name[20] + '/' + teacher_name[25], '311/114',),
           ('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[57], 'с/з',),
           ('', lesson_time['4'], 'Информационные технологии', teacher_name[58], '205',)],
          [('', lesson_time['1'], 'Охр.окр.среды и энергосб.', teacher_name[62], '307',),
           ('', lesson_time['2'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['3'], 'Электротехн.с осн.электр.', teacher_name[29], '102',)],
          [('', lesson_time['1'], 'Нормир.точн. и тех.измерен', teacher_name[26], '309',),
           ('', lesson_time['2'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[23], '319/321',),
           ('', lesson_time['3'], 'Электрооб.мет.станков', teacher_name[1], '120',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Электрооб.мет.станков', teacher_name[1], '120',),
           ('', lesson_time['3s'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[23], '319/321'),
           ('', lesson_time['4s'], 'Физическая культура', teacher_name[59] + '/' + teacher_name[57], 'с/з',)]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Нормир.точн. и тех.измерен/Техн.мех.', teacher_name[26] + '/' + teacher_name[25], '309/114',),
           ('', lesson_time['3'], 'Информационные технологии', teacher_name[49], '315',)],
          [('', lesson_time['1'], 'Материалов.и техн.материал', teacher_name[35], '210',),
           ('', lesson_time['2'], 'Охр.окр.среды и энергосб', teacher_name[62], '307',),
           ('', lesson_time['3'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[23], '319/321',)],
          [('', lesson_time['1'], 'Электротехн.с осн.электр.', teacher_name[29], '102',),
           ('', lesson_time['2'], 'САПР', teacher_name[20] + '/' + teacher_name[25], '311/114',),
           ('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[57], 'с/з',),
           ('', lesson_time['4'], 'Информационные технологии', teacher_name[58], '205',)],
          [('', lesson_time['1'], 'Охр.окр.среды и энергосб.', teacher_name[62], '307',),
           ('', lesson_time['2'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['3'], 'Электротех.с осн.эл/Материаловед.', teacher_name[35], '114/312',)],
          [('', lesson_time['1'], 'Нормир.точн. и тех.измерен', teacher_name[26], '309',),
           ('', lesson_time['2'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[23], '319/321',),
           ('', lesson_time['3'], 'Информационные технологии', teacher_name[49], '205/311',)],
          [('', lesson_time['1'], 'Техническая механика', teacher_name[25], '111',),
           ('', lesson_time['2'], 'Электрооб.мет.станков', teacher_name[1], '120',),
           ('', lesson_time['3s'], 'Инженерная графика', teacher_name[82] + '/' + teacher_name[23], '319/321')]
        ]
    },
  'Р53': {
      'UP': [
          [('', lesson_time['1'], 'Физическая культура ', teacher_name[68] + '/' + teacher_name[31], 'с/з',),
           ('', lesson_time['2'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[56], '307',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[39] + '/' + teacher_name[77], '319/314',)],
          [('', lesson_time['1'], 'Физика', teacher_name[76], '302',),
           ('', lesson_time['2'], 'Астрономия', teacher_name[76], '302',),
           ('', lesson_time['3'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['4'], 'Медицинская подготовка', teacher_name[24], '202',)],
          [('', lesson_time['1'], 'Допризывная подготовка', teacher_name[9], '119',),
           ('', lesson_time['2'], 'Всемирная история ', teacher_name[28], '121',),
           ('', lesson_time['3'], 'Математика', teacher_name[13], '124',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['3'], 'Информатика', teacher_name[58] + '/' + teacher_name[18], '205/210',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[53], '315',)],
          [('', lesson_time['1'], 'Русский язык', teacher_name[56], '312',),
           ('', lesson_time['2'], 'Всемирная история ', teacher_name[28], '121',),
           ('', lesson_time['3'], 'Биология', teacher_name[24], '207',)],
          [('', lesson_time['2'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['3s'], 'Химия', teacher_name[44], '212')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Физическая культура ', teacher_name[68] + '/' + teacher_name[31], 'с/з',),
           ('', lesson_time['2'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[56], '307',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[39] + '/' + teacher_name[77], '319/314',)],
          [('', lesson_time['1'], 'Физика', teacher_name[76], '302',),
           ('', lesson_time['2'], 'Всемирная история', teacher_name[28], '121',),
           ('', lesson_time['3'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['4'], 'Медицинская подготовка', teacher_name[24], '202',)],
          [('', lesson_time['1'], 'Допризывная подготовка', teacher_name[9], '305',),
           ('', lesson_time['2'], 'Физика', teacher_name[76], '207',),
           ('', lesson_time['3'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['4'], 'Физическая культура ', teacher_name[68] + '/' + teacher_name[31], 'с/з',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['3'], 'Информатика', teacher_name[58] + '/' + teacher_name[18], '205/210',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[53], '315',)],
          [('', lesson_time['1'], 'Русский язык', teacher_name[56], '312',),
           ('', lesson_time['2'], 'Химия  ', teacher_name[44], '212',),
           ('', lesson_time['3'], 'Биология', teacher_name[24], '207',)],
          [('', lesson_time['2'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['3s'], 'Химия', teacher_name[44], '212')]
        ]
    },
  'Р54': {
      'UP': [
          [('', lesson_time['1'], 'География', teacher_name[52], '207',),
           ('', lesson_time['2'], 'Допризывная подготовка', teacher_name[9], '119',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[77] + '/' + teacher_name[21], '314/318',)],
          [('', lesson_time['1'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['2'], 'Биология', teacher_name[38], '210',),
           ('', lesson_time['3'], 'Физика', teacher_name[76], '302',),
           ('', lesson_time['4'], 'Медицинская подготовка', teacher_name[24], '202',)],
          [('', lesson_time['1'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['2'], 'Физическая культура ', teacher_name[68] + '/' + teacher_name[31], 'с/з',),
           ('', lesson_time['3'], 'Информатика', teacher_name[58] + '/' + teacher_name[18], '205/210',)],
          [('', lesson_time['1'], 'Русский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Астрономия', teacher_name[76], '209',),
           ('', lesson_time['3'], 'Всемирная история ', teacher_name[28], '200',)],
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Химия ', teacher_name[44], '212',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[60], '20',),
           ('', lesson_time['4'], 'Физическая культура ', teacher_name[68] + '/' + teacher_name[31], 'с/з',)],
          [('', lesson_time['1'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['2'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['3s'], 'Белорусский язык', teacher_name[60], '20')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'География', teacher_name[52], '207',),
           ('', lesson_time['2'], 'Допризывная подготовка', teacher_name[9], '119',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[77] + '/' + teacher_name[21], '314/318',)],
          [('', lesson_time['1'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['2'], 'Биология', teacher_name[38], '210',),
           ('', lesson_time['3'], 'Физика', teacher_name[76], '302',),
           ('', lesson_time['4'], 'Медицинская подготовка', teacher_name[24], '202',)],
          [('', lesson_time['1'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['2'], 'Физическая культура ', teacher_name[68] + '/' + teacher_name[31], 'с/з',),
           ('', lesson_time['3'], 'Информатика', teacher_name[58] + '/' + teacher_name[18], '205/210',)],
          [('', lesson_time['1'], 'Русский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Физика', teacher_name[76], '209',),
           ('', lesson_time['3'], 'Всемирная история ', teacher_name[28], '200',)],
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Всемирная история  ', teacher_name[28], '121',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[60], '20',)],
          [('', lesson_time['1'], 'Математика', teacher_name[13], '124',),
           ('', lesson_time['2'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['3s'], 'Белорусский язык', teacher_name[60], '20')]
        ]
    },
  'Р49': {
      'UP': [
          [('', lesson_time['4'], 'Радиотехника/ Микропроц.техника ', teacher_name[81] + '/' + teacher_name[18], '311/210',),
           ('', lesson_time['5'], 'Охрана труда', teacher_name[72], '305',),
           ('', lesson_time['6'], 'САПР', teacher_name[18], '210',)],
          [('', lesson_time['4'], 'Физкультура и здоровье', teacher_name[93], 'с/з',),
           ('', lesson_time['5'], 'Радиотехника', teacher_name[81], '311',),
           ('', lesson_time['6'], 'ЭРЭ и УФЭ', teacher_name[64], '307',)],
          [('', lesson_time['4'], 'Радиотехника/ Микропроц.техника ', teacher_name[81] + '/' + teacher_name[18], '311/210',),
           ('', lesson_time['5'], 'РЭУ/ЭРЭ и УФЭ', teacher_name[11] + '/' + teacher_name[64], '305/300',),
           ('', lesson_time['6'], 'ЭРИ/САПР', teacher_name[64] + '/' + teacher_name[18], '300/210',)],
          [('', lesson_time['4'], 'РЭУ', teacher_name[11], '305',),
           ('', lesson_time['5'], 'Охрана труда', teacher_name[72], '302',),
           ('', lesson_time['6'], 'Микропроцессорная техника', teacher_name[18], '210',)],
          [('', lesson_time['3'], 'САПР', teacher_name[18], '210',),
           ('', lesson_time['4'], 'Защита нас.и террит. от ЧС', teacher_name[40], '302',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[93], 'с/з',),
           ('', lesson_time['6'], 'ЭРИ', teacher_name[64], '300',)],
          [('', lesson_time['4s'], 'РЭУ', teacher_name[11], '305'),
           ('', lesson_time['5s'], 'ЭРИ ', teacher_name[64], '307')]
        ],
    'DOWN': [
          [('', lesson_time['3'], 'Микропроцессорная техника', teacher_name[18], '210',),
           ('', lesson_time['4'], 'Радиотехника/ Микропроц.техника ', teacher_name[81] + '/' + teacher_name[18], '311/210',),
           ('', lesson_time['5'], 'Охрана труда', teacher_name[72], '305',),
           ('', lesson_time['6'], 'САПР', teacher_name[18], '210',)],
          [('', lesson_time['4'], 'РЭУ', teacher_name[11], '305',),
           ('', lesson_time['5'], 'Радиотехника', teacher_name[81], '311',),
           ('', lesson_time['6'], 'ЭРЭ и УФЭ', teacher_name[64], '307',)],
          [('', lesson_time['4'], 'ЭРЭ и УФЭ  ', teacher_name[64], '307',),
           ('', lesson_time['5'], 'РЭУ/ЭРЭ и УФЭ', teacher_name[11] + '/' + teacher_name[64], '305/300',),
           ('', lesson_time['6'], 'ЭРИ/САПР', teacher_name[64] + '/' + teacher_name[18], '300/210',)],
          [('', lesson_time['4'], 'РЭУ', teacher_name[11], '305',),
           ('', lesson_time['5'], 'Охрана труда', teacher_name[72], '302',),
           ('', lesson_time['6'], 'Микропроцессорная техника', teacher_name[18], '210',)],
          [('', lesson_time['4'], 'Защита нас.и террит. от ЧС', teacher_name[40], '302',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[93], 'с/з',),
           ('', lesson_time['6'], 'РЭУ', teacher_name[11], '305',)],
          [('', lesson_time['4s'], 'РЭУ', teacher_name[11], '305'),
           ('', lesson_time['5s'], 'ЭРИ ', teacher_name[64], '307')]
        ]
    },
  'Р50': {
      'UP': [
          [('', lesson_time['3'], 'Микропроцессорная техника', teacher_name[18], '210',),
           ('', lesson_time['4'], 'Охрана труда ', teacher_name[72], '305',),
           ('', lesson_time['5'], 'Радиотехника/ Микропроц.техника ', teacher_name[81] + '/' + teacher_name[18], '311/210',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[93], 'с/з',)],
          [('', lesson_time['4'], 'ЭРЭ и УФЭ', teacher_name[64], '307',),
           ('', lesson_time['5'], 'ЭРИ/САПР', teacher_name[64] + '/' + teacher_name[18], '300/210',),
           ('', lesson_time['6'], 'Радиотехника', teacher_name[81], '311',)],
          [('', lesson_time['4'], 'ЭРЭ и УФЭ ', teacher_name[64], '307',),
           ('', lesson_time['5'], 'Защита нас.и террит. от ЧС', teacher_name[40], '210',),
           ('', lesson_time['6'], 'РЭУ', teacher_name[11], '305',)],
          [('', lesson_time['4'], 'Охрана труда', teacher_name[72], '302',),
           ('', lesson_time['5'], 'РЭУ', teacher_name[11], '305',)],
          [('', lesson_time['4'], 'САПР', teacher_name[18], '210',),
           ('', lesson_time['5'], 'РЭУ/ЭРЭ и УФЭ', teacher_name[11] + '/' + teacher_name[64], '305/300',),
           ('', lesson_time['6'], 'Микропроцессорная техника', teacher_name[18], '210',)],
          [('', lesson_time['4s'], 'ЭРИ ', teacher_name[64], '307'),
           ('', lesson_time['5s'], 'РЭУ', teacher_name[11], '305')]
        ],
    'DOWN': [
          [('', lesson_time['4'], 'Охрана труда ', teacher_name[72], '305',),
           ('', lesson_time['5'], 'Радиотехника/ Микропроц.техника ', teacher_name[81] + '/' + teacher_name[18], '311/210',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[93], 'с/з',)],
          [('', lesson_time['4'], 'ЭРЭ и УФЭ', teacher_name[64], '307',),
           ('', lesson_time['5'], 'ЭРИ/САПР', teacher_name[64] + '/' + teacher_name[18], '300/210',),
           ('', lesson_time['6'], 'Радиотехника', teacher_name[81], '311',)],
          [('', lesson_time['4'], 'Радиотехника/ Микропроц.техника', teacher_name[81] + '/' + teacher_name[18], '311/210',),
           ('', lesson_time['5'], 'Защита нас.и террит. от ЧС', teacher_name[40], '210',),
           ('', lesson_time['6'], 'РЭУ', teacher_name[11], '305',)],
          [('', lesson_time['4'], 'Охрана труда', teacher_name[72], '302',),
           ('', lesson_time['5'], 'РЭУ', teacher_name[11], '305',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[93], 'с/з',)],
          [('', lesson_time['3'], 'ЭРИ /САПР', teacher_name[18], '300/210',),
           ('', lesson_time['4'], 'САПР', teacher_name[18], '210',),
           ('', lesson_time['5'], 'РЭУ/ЭРЭ и УФЭ', teacher_name[11] + '/' + teacher_name[64], '305/300',),
           ('', lesson_time['6'], 'Микропроцессорная техника', teacher_name[18], '210',)],
          [('', lesson_time['4s'], 'ЭРИ ', teacher_name[64], '307'),
           ('', lesson_time['5s'], 'РЭУ', teacher_name[11], '305')]
        ]
    },
  'Р47': {
      'UP': [
          [('', lesson_time['4'], 'Основы права', teacher_name[41], '212',),
           ('', lesson_time['5'], 'Аудио и видеотехн/ КП Эконом.орг', teacher_name[7] + '/' + teacher_name[4], '308/24',),
           ('', lesson_time['6'], 'Аудио и видеотехника', teacher_name[7], '307',)],
          [('', lesson_time['4'], 'Осн.алгор.и прогр/ Исп.и контр.РЭС', teacher_name[18] + '/' + teacher_name[33], '210/311',),
           ('', lesson_time['5'], 'ТАП РЭС/Экономика организации', teacher_name[11] + '/' + teacher_name[4], '305/23',),
           ('', lesson_time['6'], 'Осн.алгор.и программир..', teacher_name[18], '210',)],
          [('', lesson_time['4'], 'Основы менеджмента', teacher_name[56], '124',),
           ('', lesson_time['5'], 'Исп.и контр.РЭС', teacher_name[33], '307',),
           ('', lesson_time['6'], 'КРЭС', teacher_name[3], '302',)],
          [('', lesson_time['4'], 'Аудио и видеотехн/ Лок.сист. автомат', teacher_name[7] + '/' + teacher_name[33], '308/311',),
           ('', lesson_time['5'], 'Аудиовидеотехника и телевидение', teacher_name[7], '307',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[66], 'с/з',)],
          [('', lesson_time['4'], 'Аудио и видеотехн/КП ТАП РЭС ', teacher_name[7] + '/' + teacher_name[11], '308/305',),
           ('', lesson_time['5'], 'Осн.алгор.и прогр/ Охранные системы', teacher_name[18] + '/' + teacher_name[3], '210/302',),
           ('', lesson_time['6'], 'Охранные системы', teacher_name[3], '302',)],
          [('', lesson_time['4s'], 'Охранные системы', teacher_name[3], '302'),
           ('', lesson_time['5s'], 'Лок.системы автоматики', teacher_name[33], '311'),
           ('', lesson_time['6s'], 'ТАП РЭС/ Конструирование РЭС', teacher_name[11] + '/' + teacher_name[3], '305/302')]
        ],
    'DOWN': [
          [('', lesson_time['4'], 'Основы права', teacher_name[41], '212',),
           ('', lesson_time['5'], 'Аудио и видеотехн/ КП Эконом.орг', teacher_name[7] + '/' + teacher_name[4], '308/24',),
           ('', lesson_time['6'], 'Аудио и видеотехн/ ТАП РЭС', teacher_name[7] + '/' + teacher_name[11], '308/305',)],
          [('', lesson_time['4'], 'Осн.алгор.и прогр/ Исп.и контр.РЭС', teacher_name[18] + '/' + teacher_name[33], '210/311',),
           ('', lesson_time['5'], 'Экономика организации', teacher_name[4], '23',),
           ('', lesson_time['6'], 'Осн.алгор.и программир..', teacher_name[18], '210',)],
          [('', lesson_time['4'], 'Основы менеджмента', teacher_name[56], '124',),
           ('', lesson_time['5'], 'Исп.и контр.РЭС', teacher_name[33], '307',),
           ('', lesson_time['6'], 'Лок.системы автоматики', teacher_name[33], '307',)],
          [('', lesson_time['4'], 'Аудио и видеотехн/ Лок.сист. автомат', teacher_name[7] + '/' + teacher_name[33], '308/311',),
           ('', lesson_time['5'], 'Аудиовидеотехника и телевидение', teacher_name[7], '307',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[66], 'с/з',)],
          [('', lesson_time['4'], 'Аудио и видеотехн/КП ТАП РЭС ', teacher_name[7] + '/' + teacher_name[11], '308/305',),
           ('', lesson_time['5'], 'Осн.алгор.и прогр/ Охранные системы', teacher_name[18] + '/' + teacher_name[3], '210/302',),
           ('', lesson_time['6'], 'Аудио и видеотехника', teacher_name[7], '307',)],
          [('', lesson_time['4s'], 'Охранные системы', teacher_name[3], '302'),
           ('', lesson_time['5s'], 'Лок.системы автоматики', teacher_name[33], '311'),
           ('', lesson_time['6s'], 'Физкультура и здоровье', teacher_name[66], 'с/з')]
        ]
    },
  'Р48': {
      'UP': [
          [('', lesson_time['4'], 'Аудио и видеотехн/ КП Эконом.орг', teacher_name[7] + '/' + teacher_name[4], '308/24',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[66], 'с/з',),
           ('', lesson_time['6'], 'Основы менеджмента', teacher_name[56], '119',)],
          [('', lesson_time['4'], 'ТАП РЭС/Экономика организации', teacher_name[11] + '/' + teacher_name[4], '305/23',),
           ('', lesson_time['5'], 'Аудио и видеотехн', teacher_name[7], '307',),
           ('', lesson_time['6'], 'Аудио и видеотехн/ КП ТАП РЭС', teacher_name[7] + '/' + teacher_name[11], '308/305',)],
          [('', lesson_time['4'], 'Охранные системы', teacher_name[3], '302',),
           ('', lesson_time['5'], 'Осн.алгор.и прогр/ Охранные системы', teacher_name[18] + '/' + teacher_name[3], '210/302',),
           ('', lesson_time['6'], 'Лок.системы автоматики', teacher_name[33], '307',)],
          [('', lesson_time['4'], 'Осн.алгор.и программир.', teacher_name[18], '210',),
           ('', lesson_time['5'], 'Осн.алгор.и прогр/ Исп.и контр.РЭС', teacher_name[18] + '/' + teacher_name[33], '210/311',),
           ('', lesson_time['6'], 'Аудио и видеотехн/ Лок.сист. автомат', teacher_name[7] + '/' + teacher_name[33], '308/111',)],
          [('', lesson_time['4'], 'Основы права', teacher_name[41], '212',),
           ('', lesson_time['5'], 'Аудиовидеотехника и телевидение', teacher_name[7], '307',),
           ('', lesson_time['6'], 'Аудио и видеотехн/КП ТАП РЭС ', teacher_name[7] + '/' + teacher_name[11], '308/305',)],
          [('', lesson_time['4s'], 'Исп.и контр.РЭС', teacher_name[33], '311'),
           ('', lesson_time['5s'], 'КРЭС', teacher_name[3], '302'),
           ('', lesson_time['6s'], 'Лок.системы автоматики', teacher_name[33], '307')]
        ],
    'DOWN': [
          [('', lesson_time['4'], 'Аудио и видеотехн/ КП Эконом.орг', teacher_name[7] + '/' + teacher_name[4], '308/24',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[66], 'с/з',),
           ('', lesson_time['6'], 'Основы менеджмента', teacher_name[56], '119',)],
          [('', lesson_time['4'], 'Экономика организации', teacher_name[4], '23',),
           ('', lesson_time['5'], 'Аудио и видеотехн', teacher_name[7], '307',),
           ('', lesson_time['6'], 'Аудио и видеотехн/ КП ТАП РЭС', teacher_name[7] + '/' + teacher_name[11], '308/305',)],
          [('', lesson_time['4'], 'Лок.системы автоматики', teacher_name[33], '302',),
           ('', lesson_time['5'], 'Осн.алгор.и прогр/ Охранные системы', teacher_name[18] + '/' + teacher_name[3], '210/302',),
           ('', lesson_time['6'], 'Охранные системы', teacher_name[3], '302',)],
          [('', lesson_time['4'], 'Осн.алгор.и программир.', teacher_name[18], '210',),
           ('', lesson_time['5'], 'Осн.алгор.и прогр/ Исп.и контр.РЭС', teacher_name[18] + '/' + teacher_name[33], '210/311',),
           ('', lesson_time['6'], 'Аудио и видеотехн/ Лок.сист. автомат', teacher_name[7] + '/' + teacher_name[33], '308/111',)],
          [('', lesson_time['4'], 'Основы права', teacher_name[41], '212',),
           ('', lesson_time['5'], 'Аудиовидеотехника и телевидение', teacher_name[7], '307',),
           ('', lesson_time['6'], 'Охранные системы ', teacher_name[3], '302',)],
          [('', lesson_time['4s'], 'Исп.и контр.РЭС', teacher_name[33], '311'),
           ('', lesson_time['5s'], 'Физкультура и здоровье', teacher_name[66], 'с/з'),
           ('', lesson_time['6s'], 'ТАП РЭС/ Конструирование РЭС', teacher_name[11] + '/' + teacher_name[3], '305/302')]
        ]
    },
  'Ср23': {
      'UP': [
          [('', lesson_time['1'], 'Математика', teacher_name[71], '124',),
           ('', lesson_time['2'], 'История Беларуси', teacher_name[63], '121',),
           ('', lesson_time['3'], 'Белорусский язык', teacher_name[55], '310',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[39], '319',)],
          [('', lesson_time['1'], 'Допризывная/Медицинская подготовка', teacher_name[9] + '/' + teacher_name[24], '212',),
           ('', lesson_time['2'], 'Русский язык', teacher_name[2], '120',),
           ('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[57] + '/' + teacher_name[94], 'с/з',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Иностранный язык', teacher_name[80] + '/' + teacher_name[21], '321/318',),
           ('', lesson_time['3'], 'Математика', teacher_name[71], '202',)],
          [('', lesson_time['1'], 'Математика', teacher_name[71], '119',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[2], '120',),
           ('', lesson_time['3'], 'История Беларуси', teacher_name[63], '121',)],
          [('', lesson_time['1'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['2'], 'Белорусская литература', teacher_name[55], '305',),
           ('', lesson_time['3'], 'Физика', teacher_name[76], '209',)],
          [('', lesson_time['2'], 'Всемирная история', teacher_name[75], '119',),
           ('', lesson_time['3s'], 'Биология', teacher_name[38], '200',)]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Математика', teacher_name[71], '124',),
           ('', lesson_time['2'], 'История Беларуси', teacher_name[63], '121',),
           ('', lesson_time['3'], 'Белорусский язык', teacher_name[55], '310',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[39], '319',)],
          [('', lesson_time['1'], 'Допризывная/Медицинская подготовка', teacher_name[9] + '/' + teacher_name[24], '119/207',),
           ('', lesson_time['2'], 'Русский язык', teacher_name[2], '120',),
           ('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[57] + '/' + teacher_name[94], 'с/з',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Иностранный язык', teacher_name[80] + '/' + teacher_name[21], '312/318',),
           ('', lesson_time['3'], 'Математика', teacher_name[71], '202',),
           ('', lesson_time['4'], 'Физика', teacher_name[76], '209',)],
          [('', lesson_time['1'], 'Математика', teacher_name[71], '119',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[2], '120',),
           ('', lesson_time['3'], 'История Беларуси', teacher_name[63], '121',)],
          [('', lesson_time['1'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['2'], 'Белорусская литература', teacher_name[55], '305',),
           ('', lesson_time['3'], 'Физика', teacher_name[76], '209',),
           ('', lesson_time['4'], 'Всемирная история', teacher_name[75], '121',)],
          [('', lesson_time['2'], 'Всемирная история', teacher_name[75], '119',),
           ('', lesson_time['3s'], 'Биология', teacher_name[38], '200',),
           ('', lesson_time['4s'], 'Физкультура и здоровье', teacher_name[57] + '/' + teacher_name[94], 'с/з')]
        ]
    },
  'С86': {
      'UP': [
          [('', lesson_time['1'], 'Допризывная  подготовка', teacher_name[9], '314',),
           ('', lesson_time['2'], 'Математика', teacher_name[45], '202',),
           ('', lesson_time['3'], 'История Беларуси', teacher_name[63], '121',)],
          [('', lesson_time['1'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[93], 'с/з',),
           ('', lesson_time['2'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['3'], 'Всемирная история', teacher_name[75], '121',)],
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[30], '207',),
           ('', lesson_time['2'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[77], '315/314',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[60], '20',)],
          [('', lesson_time['1'], 'История Беларуси', teacher_name[63], '121',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[60], '20',),
           ('', lesson_time['3'], 'Математика', teacher_name[45], '202',),
           ('', lesson_time['4'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[93], 'с/з',)],
          [('', lesson_time['1'], 'Всемирная история ', teacher_name[75], '302',),
           ('', lesson_time['2'], 'Физика', teacher_name[16], '202',),
           ('', lesson_time['3'], 'Белорусская литература', teacher_name[55], '305',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Биология ', teacher_name[38], '200',),
           ('', lesson_time['3s'], 'Математика', teacher_name[45], '124')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Биология', teacher_name[38], '212',),
           ('', lesson_time['2'], 'Математика', teacher_name[45], '202',),
           ('', lesson_time['3'], 'История Беларуси', teacher_name[63], '121',)],
          [('', lesson_time['1'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[93], 'с/з',),
           ('', lesson_time['2'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['3'], 'Физика ', teacher_name[16], '202',)],
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[30], '207',),
           ('', lesson_time['2'], 'Иностранный язык', teacher_name[53] + '/' + teacher_name[77], '315/314',),
           ('', lesson_time['3'], 'Русский язык', teacher_name[60], '20',)],
          [('', lesson_time['1'], 'История Беларуси', teacher_name[63], '121',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[60], '20',),
           ('', lesson_time['3'], 'Математика', teacher_name[45], '202',)],
          [('', lesson_time['1'], 'Всемирная история ', teacher_name[75], '302',),
           ('', lesson_time['2'], 'Физика', teacher_name[16], '202',),
           ('', lesson_time['3'], 'Белорусская литература', teacher_name[55], '305',),
           ('', lesson_time['4'], 'Медицинская подготовка ', teacher_name[24], '207',)],
          [('', lesson_time['1'], 'География', teacher_name[52], '209',),
           ('', lesson_time['2'], 'Биология ', teacher_name[38], '200',),
           ('', lesson_time['3s'], 'Математика', teacher_name[45], '124')]
        ]
    },
  'С87': {
      'UP': [
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Математика', teacher_name[71], '124',),
           ('', lesson_time['3'], 'Всемирная история', teacher_name[28], '119',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[39], '319',)],
          [('', lesson_time['1'], 'История Беларуси', teacher_name[28], '121',),
           ('', lesson_time['2'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[94], 'с/з',),
           ('', lesson_time['3'], 'Физика ', teacher_name[16], '202',)],
          [('', lesson_time['1'], 'Математика', teacher_name[71], '202',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[56], '307',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[80] + '/' + teacher_name[21], '312/318',)],
          [('', lesson_time['1'], 'Всемирная история', teacher_name[28], '200',),
           ('', lesson_time['2'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['3'], 'Белорусская литература', teacher_name[60], '20',)],
          [('', lesson_time['1'], 'Математика', teacher_name[71], '119',),
           ('', lesson_time['2'], 'Русский язык', teacher_name[56], '312',),
           ('', lesson_time['3'], 'Биология', teacher_name[38], '302',)],
          [('', lesson_time['1'], 'История Беларуси', teacher_name[28], '119',),
           ('', lesson_time['2'], 'Физика', teacher_name[16], '202',),
           ('', lesson_time['3s'], 'География', teacher_name[52], '207')]
        ],
    'DOWN': [
          [('', lesson_time['1'], 'Белорусский язык', teacher_name[60], '20',),
           ('', lesson_time['2'], 'Математика', teacher_name[71], '124',),
           ('', lesson_time['3'], 'Допризывная  подготовка ', teacher_name[9], '119',),
           ('', lesson_time['4'], 'Иностранный язык', teacher_name[39], '319',)],
          [('', lesson_time['1'], 'История Беларуси', teacher_name[28], '121',),
           ('', lesson_time['2'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[94], 'с/з',),
           ('', lesson_time['3'], 'Биология ', teacher_name[16], '210',)],
          [('', lesson_time['1'], 'Математика', teacher_name[71], '202',),
           ('', lesson_time['2'], 'Русская литература', teacher_name[56], '307',),
           ('', lesson_time['3'], 'Иностранный язык', teacher_name[80] + '/' + teacher_name[21], '312/318',)],
          [('', lesson_time['1'], 'Всемирная история', teacher_name[28], '200',),
           ('', lesson_time['2'], 'Химия', teacher_name[44], '212',),
           ('', lesson_time['3'], 'Белорусская литература', teacher_name[60], '20',),
           ('', lesson_time['4'], 'Физкультура и здоровье', teacher_name[59] + '/' + teacher_name[94], 'с/з',)],
          [('', lesson_time['1'], 'Математика', teacher_name[71], '119',),
           ('', lesson_time['2'], 'Русский язык', teacher_name[56], '312',),
           ('', lesson_time['3'], 'Биология', teacher_name[38], '302',),
           ('', lesson_time['4'], 'Медицинская подготовка ', teacher_name[24], '207',)],
          [('', lesson_time['1'], 'История Беларуси', teacher_name[28], '119',),
           ('', lesson_time['2'], 'Физика', teacher_name[16], '202',),
           ('', lesson_time['3s'], 'География', teacher_name[52], '207')]
        ]
    },
  'Ср21': {
      'UP': [
          [('', lesson_time['4'], 'КП ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[19], '106/20',),
           ('', lesson_time['5'], 'ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[19], '106/20',),
           ('', lesson_time['6'], 'Охрана труда', teacher_name[79], '207',)],
          [('', lesson_time['5'], 'ТСП/КП СТК', teacher_name[42] + '/' + teacher_name[19] + '/' + teacher_name[54], '109/106',),
           ('', lesson_time['6'], 'ТСП', teacher_name[42], '106',)],
          [('', lesson_time['4'], 'ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[54], '106/109',),
           ('', lesson_time['5'], 'ГПЗ', teacher_name[15], '106',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[59], 'с/з',)],
          [('', lesson_time['4'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['5'], 'ТСП', teacher_name[42], '212',)],
          [('', lesson_time['3'], 'ГПЗ', teacher_name[15], '106',),
           ('', lesson_time['4'], 'КП ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[54], '106/205',),
           ('', lesson_time['5'], 'ТСП', teacher_name[42], '104',),
           ('', lesson_time['6'], 'СТК', teacher_name[19], '20',)],
          [('', lesson_time['4s'], 'СТК', teacher_name[19], '106'),
           ('', lesson_time['5s'], 'Физкультура и здоровье', teacher_name[59], 'с/з'),
           ('', lesson_time['6s'], 'Охрана труда', teacher_name[79], '106')]
        ],
    'DOWN': [
          [('', lesson_time['4'], 'КП ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[19], '106/20',),
           ('', lesson_time['5'], 'ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[19], '106/20',),
           ('', lesson_time['6'], 'Охрана труда', teacher_name[79], '207',)],
          [('', lesson_time['4'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['5'], 'ТСП/КП СТК', teacher_name[42] + '/' + teacher_name[19] + '/' + teacher_name[54], '109/106',),
           ('', lesson_time['6'], 'Охрана труда', teacher_name[79], '106',)],
          [('', lesson_time['4'], 'ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[54], '106/109',),
           ('', lesson_time['5'], 'ГПЗ', teacher_name[15], '106',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[59], 'с/з',)],
          [('', lesson_time['4'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['5'], 'ТСП', teacher_name[42], '212',),
           ('', lesson_time['6'], 'ГПЗ', teacher_name[15], '106',)],
          [('', lesson_time['3'], 'ГПЗ', teacher_name[15], '106',),
           ('', lesson_time['4'], 'КП ГПЗ/СТК', teacher_name[15] + '/' + teacher_name[54], '106/205',),
           ('', lesson_time['5'], 'ТСП/КП СТК', teacher_name[42] + '/' + teacher_name[19] + '/' + teacher_name[54], '109/205',),
           ('', lesson_time['6'], 'СТК', teacher_name[19], '20',)],
          [('', lesson_time['4s'], 'СТК', teacher_name[19], '106'),
           ('', lesson_time['5s'], 'ТСП', teacher_name[42], '106'),
           ('', lesson_time['6s'], 'Охрана труда', teacher_name[79], '106')]
        ]
    },
  'С81': {
      'UP': [
          [('', lesson_time['4'], 'ТСП/ СТК', teacher_name[50] + '/' + teacher_name[46], '102/109',),
           ('', lesson_time['5'], 'СТК', teacher_name[46], '121',),
           ('', lesson_time['6'], 'ТСП', teacher_name[50], '102',)],
          [('', lesson_time['4'], 'Экономика строительства', teacher_name[43], '119',),
           ('', lesson_time['5'], 'Информ.технологии в строит. произв ', teacher_name[48] + '/' + teacher_name[97], '209/114',),
           ('', lesson_time['6'], 'Экономика строительства', teacher_name[43], '200',)],
          [('', lesson_time['4'], 'ТСП/СТК', teacher_name[50] + '/' + teacher_name[46], '102',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[59], 'с/з',),
           ('', lesson_time['6'], 'ТСП', teacher_name[50], '102',)],
          [('', lesson_time['4'], 'Инженерн.сети и оборудов ', teacher_name[14], '102',),
           ('', lesson_time['5'], 'СТК', teacher_name[46], '104',),
           ('', lesson_time['6'], 'ОСГН', teacher_name[75], '121',)],
          [('', lesson_time['4'], 'ОСГН', teacher_name[75], '121',),
           ('', lesson_time['5'], 'ТСП/СТК', teacher_name[50] + '/' + teacher_name[46], '102/124',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[59], 'с/з',)],
          [('', lesson_time['3s'], 'Инженерн.сети и оборудов  ', teacher_name[14], '104',),
           ('', lesson_time['4s'], 'КП ТСП/ Инженерн.сети и оборудов ', teacher_name[50] + '/' + teacher_name[14], '102/119',),
           ('', lesson_time['5s'], 'ТСП', teacher_name[50], '102',),
           ('', lesson_time['6s'], 'КП ТСП/ Инженерн.сети и оборудов', teacher_name[50] + '/' + teacher_name[14], '102/119')]
        ],
    'DOWN': [
          [('', lesson_time['4'], 'ТСП/ СТК', teacher_name[50] + '/' + teacher_name[46], '102/109',),
           ('', lesson_time['5'], 'СТК', teacher_name[46], '121',),
           ('', lesson_time['6'], 'ТСП', teacher_name[50], '102',)],
          [('', lesson_time['4'], 'Экономика строительства', teacher_name[43], '119',),
           ('', lesson_time['5'], 'Информ.технологии в строит. произв ', teacher_name[48] + '/' + teacher_name[97], '209/114',),
           ('', lesson_time['6'], 'Экономика строительства', teacher_name[43], '200',)],
          [('', lesson_time['4'], 'ТСП/СТК', teacher_name[50] + '/' + teacher_name[46], '102',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[59], 'с/з',),
           ('', lesson_time['6'], 'ТСП', teacher_name[50], '102',)],
          [('', lesson_time['4'], 'Инженерн.сети и оборудов ', teacher_name[14], '102',),
           ('', lesson_time['5'], 'СТК', teacher_name[46], '104',),
           ('', lesson_time['6'], 'ОСГН', teacher_name[75], '121',)],
          [('', lesson_time['4'], 'Экономика строительства', teacher_name[43], '200',),
           ('', lesson_time['5'], 'ТСП/СТК', teacher_name[50] + '/' + teacher_name[46], '102/124',),
           ('', lesson_time['6'], 'Информ.технологии в строит. произв', teacher_name[48] + '/' + teacher_name[97], '209/114',)],
          [('', lesson_time['3s'], 'Инженерн.сети и оборудов  ', teacher_name[14], '104',),
           ('', lesson_time['4s'], 'КП ТСП/ Инженерн.сети и оборудов', teacher_name[50] + '/' + teacher_name[14], '102/119',),
           ('', lesson_time['5s'], 'ТСП', teacher_name[50], '102',)]
        ]
    },
  'С82': {
      'UP': [
          [('', lesson_time['4'], 'ГПЗ/СТК', teacher_name[48] + '/' + teacher_name[51], '209/207',),
           ('', lesson_time['5'], 'ГПЗ', teacher_name[48], '209',),
           ('', lesson_time['6'], 'КП ГПЗ/КП СТК', teacher_name[15] + '/' + teacher_name[19], '106/20',)],
          [('', lesson_time['4'], 'КП ГПЗ/КП СТК', teacher_name[48] + '/' + teacher_name[51], '209/207',),
           ('', lesson_time['5'], 'ТСП', teacher_name[67], '212',),
           ('', lesson_time['6'], 'Охрана труда', teacher_name[14], '202',)],
          [('', lesson_time['4'], 'ГПЗ', teacher_name[48], '209',),
           ('', lesson_time['5'], 'Охрана труда', teacher_name[14], '202',),
           ('', lesson_time['6'], 'СТК', teacher_name[51], '207',)],
          [('', lesson_time['4'], 'КП ГПЗ/КП СТК', teacher_name[15] + '/' + teacher_name[19], '106/119',),
           ('', lesson_time['5'], 'Охрана труда', teacher_name[14], '202',),
           ('', lesson_time['6'], 'ТСП', teacher_name[67], '207',)],
          [('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[94], 'с/з',),
           ('', lesson_time['4'], 'ТСП/СТК', teacher_name[67] + '/' + teacher_name[19], '307/20',),
           ('', lesson_time['5'], 'ТСП', teacher_name[67], '212',),
           ('', lesson_time['6'], 'ГПЗ', teacher_name[48], '209',)],
          [('', lesson_time['4s'], 'ОСГН', teacher_name[63], '121'),
           ('', lesson_time['5s'], 'ТСП/СТК', teacher_name[67] + '/' + teacher_name[51], '202/207'),
           ('', lesson_time['6s'], 'СТК', teacher_name[51], '207')]
        ],
    'DOWN': [
          [('', lesson_time['4'], 'ГПЗ/СТК', teacher_name[48] + '/' + teacher_name[51], '209/207',),
           ('', lesson_time['5'], 'ГПЗ', teacher_name[48], '209',),
           ('', lesson_time['6'], 'КП ГПЗ/КП СТК', teacher_name[15] + '/' + teacher_name[19], '106/20',)],
          [('', lesson_time['4'], 'КП ГПЗ/КП СТК', teacher_name[48] + '/' + teacher_name[51], '209/207',),
           ('', lesson_time['5'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['6'], 'Охрана труда', teacher_name[14], '202',)],
          [('', lesson_time['5'], 'СТК', teacher_name[51], '207',),
           ('', lesson_time['6'], 'Физкультура и здоровье', teacher_name[94], 'с/з',)],
          [('', lesson_time['4'], 'КП ГПЗ/КП СТК', teacher_name[15] + '/' + teacher_name[19], '106/119',),
           ('', lesson_time['5'], 'Охрана труда', teacher_name[14], '202',),
           ('', lesson_time['6'], 'ТСП', teacher_name[67], '207',)],
          [('', lesson_time['3'], 'Физкультура и здоровье', teacher_name[94], 'с/з',),
           ('', lesson_time['4'], 'ТСП/СТК', teacher_name[67] + '/' + teacher_name[19], '307/20',),
           ('', lesson_time['5'], 'ТСП', teacher_name[67], '212',),
           ('', lesson_time['6'], 'ГПЗ', teacher_name[48], '209',)],
          [('', lesson_time['4s'], 'ОСГН', teacher_name[63], '121'),
           ('', lesson_time['5s'], 'ТСП/СТК', teacher_name[67] + '/' + teacher_name[51], '202/207'),
           ('', lesson_time['6s'], 'СТК', teacher_name[51], '207')]
        ]
    },
  'С83': {
      'UP': [
          [('', lesson_time['4'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['5'], 'ТСП/СТК', teacher_name[5] + '/' + teacher_name[78], '124/111',),
           ('', lesson_time['6'], 'ТСП', teacher_name[5], '111',)],
          [('', lesson_time['4'], 'Инженерн.сети и оборудов', teacher_name[14], '106',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[94], 'с/з',),
           ('', lesson_time['6'], 'Информ.технологии в строит. произв', teacher_name[48] + '/' + teacher_name[99], '219/114',)],
          [('', lesson_time['4'], 'КП ТСП/ Инженерн.сети и оборудов', teacher_name[5] + '/' + teacher_name[14], '305/119',),
           ('', lesson_time['5'], 'ТСП', teacher_name[5], '104',),
           ('', lesson_time['6'], 'СТК', teacher_name[78], '119',)],
          [('', lesson_time['4'], 'СТК', teacher_name[78], '124',),
           ('', lesson_time['5'], 'Экономика строительства', teacher_name[85], '106',),
           ('', lesson_time['6'], 'Экономика строительства', teacher_name[85], '104',)],
          [('', lesson_time['4'], 'ТСП/СТК', teacher_name[5] + '/' + teacher_name[78], '23/114',),
           ('', lesson_time['5'], 'Экономика строительства', teacher_name[85], '106',),
           ('', lesson_time['6'], 'ТСП/СТК', teacher_name[5] + '/' + teacher_name[78], '106/124',)],
          [('', lesson_time['3s'], 'ОСГН', teacher_name[63], '209',),
           ('', lesson_time['4s'], 'ТСП', teacher_name[5], '104'),
           ('', lesson_time['5s'], 'Инженерн.сети и оборудов', teacher_name[14], '121'),
           ('', lesson_time['6s'], 'Физкультура и здоровье', teacher_name[94], 'с/з')]
        ],
    'DOWN': [
          [('', lesson_time['4'], 'ОСГН', teacher_name[63], '121',),
           ('', lesson_time['5'], 'ТСП/СТК', teacher_name[5] + '/' + teacher_name[78], '124/111',),
           ('', lesson_time['6'], 'ТСП', teacher_name[5], '111',)],
          [('', lesson_time['4'], 'Инженерн.сети и оборудов', teacher_name[14], '106',),
           ('', lesson_time['5'], 'Физкультура и здоровье', teacher_name[94], 'с/з',),
           ('', lesson_time['6'], 'Информ.технологии в строит. произв', teacher_name[48] + '/' + teacher_name[51], '219/114',)],
          [('', lesson_time['4'], 'КП ТСП/ Инженерн.сети и оборудов', teacher_name[5] + '/' + teacher_name[14], '305/119',),
           ('', lesson_time['5'], 'ТСП', teacher_name[5], '104',),
           ('', lesson_time['6'], 'СТК', teacher_name[78], '119',)],
          [('', lesson_time['4'], 'СТК', teacher_name[78], '124',),
           ('', lesson_time['5'], 'Экономика строительства', teacher_name[85], '106',),
           ('', lesson_time['6'], 'Экономика строительства', teacher_name[85], '104',)],
          [('', lesson_time['4'], 'ТСП/СТК', teacher_name[5] + '/' + teacher_name[78], '23/114',),
           ('', lesson_time['5'], 'Информ.технологии в строит. произв', teacher_name[48] + '/' + teacher_name[99], '209/114',),
           ('', lesson_time['6'], 'ТСП/СТК', teacher_name[5] + '/' + teacher_name[78], '106/124',)],
          [('', lesson_time['4s'], 'ТСП', teacher_name[5], '104'),
           ('', lesson_time['5s'], 'Инженерн.сети и оборудов', teacher_name[14], '121'),
           ('', lesson_time['6s'], 'КП ТСП/ Инженерн.сети и оборудов', teacher_name[5] + '/' + teacher_name[14], '104/109')]
        ]
    }
}


def resub(data):
    return re.sub(' +', ' ', data.strip())


groups_schedule = {}

for _, _, files in walk(collage_folder + '/groups/'):
    files = [f for f in files if not f[0] == '.']

for file in files:
    groups_workbook = open_workbook('%s%s' % (collage_folder + '/groups/', file))
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
            groups_schedule[group] = {'UP': [[], [], [], [], [], []],
                                      'DOWN': [[], [], [], [], [], []]}

for file in files:
    groups_workbook = open_workbook('%s%s' % (collage_folder + '/groups/', file))
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

                            (groups_schedule[group][week][day - 1]
                             .append(day_student_shedule))

existing_table_groups = list(groups_schedule.keys())


teachers_shedule = {}

for teacher in teacher_name:
    teachers_shedule[teacher] = {'UP': [[], [], [], [], [], []],
                                 'DOWN': [[], [], [], [], [], []]}


existing_teachers = []

for group in existing_groups:

    if group in existing_table_groups:
        sched = groups_schedule
    else:
        sched = shedule

    for week in sched[group]:
        for day in sched[group][week]:
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
                                 [sched[group][week]
                                  .index(day)]
                                    .append(day_shedule))

                    if (name_of_teacher.strip() not in existing_teachers and
                            '/' not in name_of_teacher):
                        existing_teachers.append(name_of_teacher.strip())

                    if (teacher == name_of_teacher and
                            '/' not in name_of_teacher):
                        (teachers_shedule[teacher][week]
                         [sched[group][week]
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
