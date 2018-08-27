# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import re
from platform import system
from collections import Counter


syst = system()

if syst == 'Linux':
    path = '/home/ubuntu/bot/'
elif syst == 'Windows':
    path = ''


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
    {'STR4':
        [
            {'StudentGroupName': 'С78'},
            {'StudentGroupName': 'С79'},
            {'StudentGroupName': 'С80'},
            {'StudentGroupName': 'Ср20'}
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
    {'MEH4':
        [
            {'StudentGroupName': 'М47'},
            {'StudentGroupName': 'М48'},
            {'StudentGroupName': 'Мс49'}
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
    '6': 'Беломесова Диана Юрьевна',
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
    '33': 'Короленко Валентина Генриковна',
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
    '84': 'Янкович Александр Леонидович'
}


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
                teacher_name[ind] = \
                    sp_te[0] + ' ' + \
                    sp_te[1][:2] + '. ' + \
                    sp_te[2][:2] + '.'
        sp_te = cap_teachers[index].split()
        teacher_name[index] = \
            sp_te[0] + ' ' + \
            sp_te[1][:2] + '. ' + \
            sp_te[2][:2] + '.'

existing_groups = []
for student_group in student_groups:
    for alias in student_group:
        for group in student_group[alias]:
            existing_groups.append(group['StudentGroupName'])


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
    'magnifying_glass': u'\U0001F50E'
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
    '{3} В любой день расписание смотрится по <b>текущей</b> неделе до '
    'ВОСКРЕСЕНЬЯ. В воскресенье расписание будет показано для следующей '
    'недели.\n'
    '{4} Так же можно <i>подписаться на рассылку</i> расписания – {5}\n '
    'Рассылка производится каждый день в 17:00 или 21:00. О выходных днях '
    'бот не уведомляет.\n'
    '{6} Если найдена ошибка в расписании просьба сразу сообщить об этом '
    '<a href="https://t.me/lee_kei">разработчику</a>.\n\n'
    '<b>Раздел "{7} Замены"</b>\n\n'
    '{8} Информация об изменениях в расписании с <b>официального сайта '
    'БГПК</b> – http://www.bspc.brest.by\n'
    '{9} При отправке команды "Завтра" в субботу, а также '
    'при отправке "Сегодня" в воскресенье, бот пришлёт замены на '
    '<b>понедельник</b>.\n'
    '{10} Так же можно <i>подписаться на рассылку</i> замен – {11}\n '
    'Рассылка производится каждый день в то же время когда замены вывесили '
    'на сайте. Максимальная задержка между сайтом и ботом – '
    '<b>1 минута</b>.\n\n'
    '<b>Раздел "{12}"</b>\n\n'
    '{13} Можно вызвать командой /settings.\n'
    '{14} Во время <i>смены группы</i> можно воспользоваться командой '
    '<b>Назад</b> (или /home) для возврата в <i>Главное меню</i>.\n'
    '{15} Если ты решишь прекратить пользоваться ботом, пожалуйста, '
    '<b>заверши работу</b> с ним (для этого необходимо написать /exit или '
    'выбрать <b>“Завершить работу”</b> в меню настроек. Просто удалить '
    'диалог недостаточно). Боту очень тяжело всех помнить, и ты, решив '
    'больше не использовать его, таким образом облегчишь ему работу.\n\n'
    '<b>Раздел "{16}"</b>\n\n'
    '{17} Можешь <b>оценить</b> бота по пятибалльной шкале (От "неуд" '
    'до "отлично")  или посмотреть <i>средний балл</i> оценок других '
    'пользователей.\n\n<b>Идейный вдохновитель</b> – @Spbu4UBot'
).format(emoji['page_facing_up'], emoji['bullet'], emoji['bullet'],
         emoji['bullet'], emoji['bullet'], emoji['alarm_clock'],
         emoji['bullet'], emoji['anticlockwise'], emoji['bullet'],
         emoji['bullet'], emoji['bullet'], emoji['alarm_clock'],
         emoji['settings'], emoji['bullet'], emoji['bullet'],
         emoji['bullet'], emoji['star'], emoji['bullet'])

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

notify = ''

# shedule1 = {
#   'group': {
#       'UP': [
#           [('', lesson_time['1'], 'lesson', 'teacher', 'audience',), # mon 1
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # tue 2
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # wed 3
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # thu 4
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # fri 5
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # sat 6
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3s'], '', '', ',')]
#         ],
#     'DOWN': [
#           [('', lesson_time['1'], '', '', '',), # mon 1
#             ('', lesson_time['2'], '', '', ','),
#             ('', lesson_time['3'], '', '', ',')],

#           [('', lesson_time['1'], '', '', '',), # tue 2
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # wed 3
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # thu 4
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # fri 5
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3'], '', '', '',)],

#           [('', lesson_time['1'], '', '', '',), # sat 6
#            ('', lesson_time['2'], '', '', '',),
#            ('', lesson_time['3s'], '', '', ',')]
#         ]
#     }
# }

# shedule2 = {
#   'group': {
#       'UP': [
#           [('', lesson_time['4'], 'lesson', 'teacher', 'audience',), # mon 1
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # tue 2
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # wed 3
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # thu 4
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # fri 5
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4s'], '', '', ','), # sat 6
#            ('', lesson_time['5s'], '', '', ','),
#            ('', lesson_time['6s'], '', '', ',')]
#         ],
#     'DOWN': [
#           [('', lesson_time['4'], '', '', '',), # mon 1
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # tue 2
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # wed 3
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # thu 4
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4'], '', '', '',), # fri 5
#            ('', lesson_time['5'], '', '', '',),
#            ('', lesson_time['6'], '', '', '',)],

#           [('', lesson_time['4s'], '', '', ','), # sat 6
#            ('', lesson_time['5s'], '', '', ','),
#            ('', lesson_time['6s'], '', '', ',')]
#         ]
#     }
# }


shedule = {
    "С86": {
        "UP": [
            [("", lesson_time['1'], "Математика", teacher_name[45], "119"), ("", lesson_time['2'], "Иностранный язык", teacher_name[
                73] + '/' + teacher_name[80] + '/' + teacher_name[39], "111/104/121"), ("", lesson_time['3'], "Химия", teacher_name[44], "212")],
            [("", lesson_time['1'], "Физика", teacher_name[16], "202"), ("", lesson_time['2'], "Математика", teacher_name[
                45], "119"), ("", lesson_time['3'], "Информатика", teacher_name[58] + '/' + teacher_name[0], "205/114")],
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Допризывная подготовка",
                                                                        teacher_name[9], "119"), ("", lesson_time['3'], "Русская литература", teacher_name[2], "121")],
            [("", lesson_time['1'], "Математика ", teacher_name[45], "124"), ("", lesson_time['2'], "Физкультура и здоровье ",
                                                                              teacher_name[59] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['3'], "Физика", teacher_name[16], "202")],
            [("", lesson_time['1'], "История Беларуси ", "Мащук С. В.", "202"), ("", lesson_time['2'], "Белорусский язык", teacher_name[60], "20"),
             ("", lesson_time['3'], "Русский язык", teacher_name[2], "121"), ("", lesson_time['4'], "Медицинская подготовка ", teacher_name[24], "207")],
            [("", lesson_time['1'], "Русская литература ", teacher_name[2], "124"), ("", lesson_time[
                '2'], "География ", teacher_name[52], "307"), ("", lesson_time['3s'], "Биология", teacher_name[38], "212")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Белорусская литература", teacher_name[60], "20"), ("", lesson_time['2'], "Иностранный язык", teacher_name[
                73] + '/' + teacher_name[80] + '/' + teacher_name[39], "111/104/121"), ("", lesson_time['3'], "Химия", teacher_name[44], "212")],
            [("", lesson_time['1'], "Астрономия", teacher_name[76], "307"), ("", lesson_time['2'], "Математика", teacher_name[
                45], "119"), ("", lesson_time['3'], "Информатика", teacher_name[58] + '/' + teacher_name[0], "205/114")],
            [("", lesson_time['1'], "Русский язык", teacher_name[2], "121"), ("", lesson_time['2'], "Допризывная подготовка",
                                                                              teacher_name[9], "119"), ("", lesson_time['3'], "История Беларуси", "Мащук С. В.", "302")],
            [("", lesson_time['1'], "Математика ", teacher_name[45], "124"), ("", lesson_time['2'], "Физкультура и здоровье ", teacher_name[59] + '/' +
                                                                              "Кульба А. В.", "с/з"), ("", lesson_time['3'], "Физика", teacher_name[16], "202"), ("", lesson_time['4'], "Биология", teacher_name[38], "212")],
            [("", lesson_time['1'], "История Беларуси ", "Мащук С. В.", "202"), ("", lesson_time['2'], "Белорусский язык", teacher_name[60], "20"), ("", lesson_time[
                '3'], "Белорусская литература", teacher_name[60], "20"), ("", lesson_time['4'], "Медицинская подготовка ", teacher_name[24], "207")],
            [("", lesson_time['1'], "Русская литература ", teacher_name[2], "124"), ("", lesson_time[
                '2'], "География ", teacher_name[52], "307"), ("", lesson_time['3s'], "Биология", teacher_name[38], "212")]
        ]
    },
    "С87": {
        "UP": [
            [("", lesson_time['1'], "Иностранный язык", teacher_name[73] + '/' + teacher_name[80] + '/' + teacher_name[12], "202/210/109"), ("",
                                                                                                                                             lesson_time['2'], "Русская литература", teacher_name[2], "120"), ("", lesson_time['3'], "Белорусский язык", teacher_name[55], "310")],
            [("", lesson_time['1'], "Биология", teacher_name[38], "124"), ("", lesson_time['2'], "Математика",
                                                                           teacher_name[71], "124"), ("", lesson_time['3'], "Белорусская литература", teacher_name[55], "310")],
            [("", lesson_time['1'], "Русская литература", teacher_name[2], "121"), ("", lesson_time[
                '2'], "Математика", teacher_name[71], "111"), ("", lesson_time['3'], "Астрономия", teacher_name[76], "305")],
            [("", lesson_time['1'], "Русский язык", teacher_name[56], "207"), ("", lesson_time[
                '2'], "Физика", teacher_name[16], "202"), ("", lesson_time['3'], "Химия", teacher_name[44], "212")],
            [("", lesson_time['1'], "Допризывная подготовка", teacher_name[9], "119"), ("", lesson_time['2'], "Физическая культура", "Кульба А. В./Шукис О. В.", "с/з"), ("",
                                                                                                                                                                          lesson_time['3'], "Информатика", teacher_name[58] + '/' + teacher_name[0], "205/315"), ("", lesson_time['4'], "Медицинская подготовка", teacher_name[24], "207")],
            [("", lesson_time['1'], "Биология", teacher_name[38], "212"), ("", lesson_time['2'], "История Беларуси",
                                                                           teacher_name[63], "121"), ("", lesson_time['3s'], "География", teacher_name[52], "307")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Иностранный язык", teacher_name[73] + '/' + teacher_name[80] + '/' + teacher_name[12], "202/210/109"),
             ("", lesson_time['2'], "Математика", teacher_name[71], "202"), ("", lesson_time['3'], "Белорусский язык", teacher_name[55], "310")],
            [("", lesson_time['1'], "Физика", teacher_name[16], "202"), ("", lesson_time['2'], "Математика", teacher_name[
                71], "124"), ("", lesson_time['3'], "Белорусская литература", teacher_name[55], "310")],
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Математика", teacher_name[71], "111"), ("", lesson_time[
                '3'], "Русская литература", teacher_name[2], "121"), ("", lesson_time['4'], "История Беларуси", teacher_name[63], "121")],
            [("", lesson_time['1'], "Русский язык", teacher_name[56], "207"), ("", lesson_time[
                '2'], "Физика", teacher_name[16], "202"), ("", lesson_time['3'], "Химия", teacher_name[44], "212")],
            [("", lesson_time['1'], "Допризывная подготовка", teacher_name[9], "119"), ("", lesson_time['2'], "Физическая культура", "Кульба А. В./Шукис О. В.", "с/з"), ("",
                                                                                                                                                                          lesson_time['3'], "Информатика", teacher_name[58] + '/' + teacher_name[0], "205/315"), ("", lesson_time['4'], "Медицинская подготовка", teacher_name[24], "207")],
            [("", lesson_time['1'], "Биология", teacher_name[38], "212"), ("", lesson_time['2'], "История Беларуси",
                                                                           teacher_name[63], "121"), ("", lesson_time['3s'], "География", teacher_name[52], "307")]
        ]
    },
    "Ср23": {
        "UP": [
            [("", lesson_time['1'], "Математика", teacher_name[71], "124"), ("", lesson_time['2'], "Русская литература", teacher_name[
                56], "207"), ("", lesson_time['3'], "Информатика ", teacher_name[58] + '/' + teacher_name[0], "205/114")],
            [("", lesson_time['1'], "Белорусская литература", teacher_name[55], "307"), ("", lesson_time[
                '2'], "Биология", teacher_name[38], "307"), ("", lesson_time['3'], "Физика", teacher_name[76], "307")],
            [("", lesson_time['1'], "Физика ", teacher_name[76], "305"), ("", lesson_time['2'], "Русская литература",
                                                                          teacher_name[56], "207"), ("", lesson_time['3'], "Русский язык", teacher_name[56], "207")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[73] + '/' + teacher_name[12] + '/' + teacher_name[39], "314/318/321"),
             ("", lesson_time['2'], "Химия", teacher_name[44], "212"), ("", lesson_time['3'], "Биология ", teacher_name[38], "307")],
            [("", lesson_time['1'], "Математика", teacher_name[71], "302"), ("", lesson_time['2'], "География", teacher_name[
                52], "307"), ("", lesson_time['3'], "Физкультура и здоровье", "Шукис О. В./Кульба А. В. ", "с/з")],
            [("", lesson_time['1'], "История Беларуси", teacher_name[63], "121"), ("", lesson_time['2'], "Допризывная (Медицинская) подготовка",
                                                                                   teacher_name[9] + '/' + teacher_name[24], "119/207"), ("", lesson_time['3s'], "Белорусский язык", teacher_name[55], "305")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Математика", teacher_name[71], "124"), ("", lesson_time['2'], "Русская литература", teacher_name[
                56], "207"), ("", lesson_time['3'], "Информатика ", teacher_name[58] + '/' + teacher_name[0], "205/114")],
            [("", lesson_time['1'], "Математика", teacher_name[71], "124"), ("", lesson_time['2'], "История Беларуси", teacher_name[63], "121"),
             ("", lesson_time['3'], "Химия", teacher_name[44], "212"), ("", lesson_time['4'], "Белорусская литература", teacher_name[55], "302")],
            [("", lesson_time['1'], "Физика ", teacher_name[76], "305"), ("", lesson_time['2'], "Астрономия",
                                                                          teacher_name[76], "305"), ("", lesson_time['3'], "Русский язык", teacher_name[56], "207")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[73] + '/' + teacher_name[12] + '/' + teacher_name[39], "314/318/321"),
             ("", lesson_time['2'], "Химия", teacher_name[44], "212"), ("", lesson_time['3'], "Биология ", teacher_name[38], "307")],
            [("", lesson_time['1'], "Математика", teacher_name[71], "302"), ("", lesson_time['2'], "География", teacher_name[
                52], "307"), ("", lesson_time['3'], "Физкультура и здоровье", "Шукис О. В./Кульба А. В. ", "с/з")],
            [("", lesson_time['1'], "История Беларуси", teacher_name[63], "121"), ("", lesson_time['2'], "Допризывная (Медицинская) подготовка",
                                                                                   teacher_name[9] + '/' + teacher_name[24], "119/207"), ("", lesson_time['3s'], "Белорусский язык", teacher_name[55], "305")]
        ]
    },
    "Р53": {
        "UP": [
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Математика ", teacher_name[
                13], "124"), ("", lesson_time['3'], "Белорусская литература", teacher_name[60], "20")],
            [("", lesson_time['1'], "Физическая культура", "Шукис О. В./Кульба А. В. ", "с/з"), ("", lesson_time['2'], "История Беларуси", teacher_name[28],
                                                                                                 "121"), ("", lesson_time['3'], "Иностранный язык", teacher_name[77] + '/' + teacher_name[21] + '/' + teacher_name[39], "314/318/315")],
            [("", lesson_time['1'], "Белорусский язык", teacher_name[60], "20"), ("", lesson_time['2'], "Математика",
                                                                                  teacher_name[13], "124"), ("", lesson_time['3'], "Допризывная подготовка ", teacher_name[9], "119")],
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Обществоведение ",
                                                                        teacher_name[28], "121"), ("", lesson_time['3'], "Физика", teacher_name[76], "305")],
            [("", lesson_time['1'], "Математика", teacher_name[13], "124"), ("", lesson_time[
                '2'], "Русская литература", teacher_name[2], "121"), ("", lesson_time['3'], "Биология", teacher_name[24], "119")],
            [("", lesson_time['1'], "География", teacher_name[52], "307"), ("", lesson_time['2'], "Русская литература",
                                                                            teacher_name[2], "124"), ("", lesson_time['3s'], "Русский язык", teacher_name[2], "124")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Математика ", teacher_name[
                13], "124"), ("", lesson_time['3'], "Белорусская литература", teacher_name[60], "20")],
            [("", lesson_time['1'], "Физическая культура", "Шукис О. В./Кульба А. В. ", "с/з"), ("", lesson_time['2'], "Биология", teacher_name[24],
                                                                                                 "120"), ("", lesson_time['3'], "Иностранный язык", teacher_name[77] + '/' + teacher_name[21] + '/' + teacher_name[39], "314/318/315")],
            [("", lesson_time['1'], "Белорусский язык", teacher_name[60], "20"), ("", lesson_time['2'], "Математика",
                                                                                  teacher_name[13], "124"), ("", lesson_time['3'], "Допризывная подготовка ", teacher_name[9], "119")],
            [("", lesson_time['1'], "Белорусская литература", teacher_name[60], "20"), ("", lesson_time[
                '2'], "Обществоведение ", teacher_name[28], "121"), ("", lesson_time['3'], "Физика", teacher_name[76], "305")],
            [("", lesson_time['1'], "Математика", teacher_name[13], "124"), ("", lesson_time[
                '2'], "Физика", teacher_name[76], "302"), ("", lesson_time['3'], "Биология", teacher_name[24], "119")],
            [("", lesson_time['1'], "География", teacher_name[52], "307"), ("", lesson_time['2'], "Русская литература",
                                                                            teacher_name[2], "124"), ("", lesson_time['3s'], "Русский язык", teacher_name[2], "124")]
        ]
    },
    "Р54": {
        "UP": [
            [("", lesson_time['1'], "Физическая культура ", teacher_name[68] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['2'], "Белорусский язык", teacher_name[60],
                                                                                                              "20"), ("", lesson_time['3'], "Математика", teacher_name[13], "124"), ("", lesson_time['4'], "Белорусская литература", teacher_name[60], "")],
            [("", lesson_time['1'], "Обществоведение", teacher_name[28], "121"), ("", lesson_time[
                '2'], "Биология", teacher_name[24], "120"), ("", lesson_time['3'], "Химия", teacher_name[44], "212")],
            [("", lesson_time['1'], "Математика", teacher_name[13], "124"), ("", lesson_time['2'], "Химия",
                                                                             teacher_name[44], "212"), ("", lesson_time['3'], "Русский язык", teacher_name[60], "20")],
            [("", lesson_time['1'], "Физика", teacher_name[76], "305"), ("", lesson_time['2'], "География", teacher_name[
                52], "307"), ("", lesson_time['3'], "Белорусская литература", teacher_name[60], "20")],
            [("", lesson_time['1'], "Русская литература", teacher_name[60], "20"), ("", lesson_time['2'], "Биология", teacher_name[24], "207"),
             ("", lesson_time['3'], "Математика", teacher_name[13], "124"), ("", lesson_time['4'], "Медицинская подготовка", teacher_name[24], "")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[77] + '/' + teacher_name[21] + '/' + teacher_name[53], "314/318/315"), ("",
                                                                                                                                             lesson_time['2'], "История Беларуси", teacher_name[28], "209"), ("", lesson_time['3s'], "Допризывная подготовка", teacher_name[9], "119")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Физическая культура ", teacher_name[68] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['2'], "Белорусский язык",
                                                                                                              teacher_name[60], "20"), ("", lesson_time['3'], "Математика", teacher_name[13], "124"), ("", lesson_time['4'], "Русская литература", teacher_name[60], "")],
            [("", lesson_time['1'], "Обществоведение", teacher_name[28], "121"), ("", lesson_time[
                '2'], "История Беларуси", teacher_name[28], "302"), ("", lesson_time['3'], "Физика", teacher_name[76], "307")],
            [("", lesson_time['1'], "Математика", teacher_name[13], "124"), ("", lesson_time['2'], "Химия",
                                                                             teacher_name[44], "212"), ("", lesson_time['3'], "Русский язык", teacher_name[60], "20")],
            [("", lesson_time['1'], "Физика", teacher_name[76], "305"), ("", lesson_time['2'], "География", teacher_name[
                52], "307"), ("", lesson_time['3'], "Белорусская литература", teacher_name[60], "20")],
            [("", lesson_time['1'], "Русская литература", teacher_name[60], "20"), ("", lesson_time['2'], "Биология", teacher_name[24], "207"),
             ("", lesson_time['3'], "Математика", teacher_name[13], "124"), ("", lesson_time['4'], "Медицинская подготовка", teacher_name[24], "")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[77] + '/' + teacher_name[21] + '/' + teacher_name[53], "314/318/315"), ("",
                                                                                                                                             lesson_time['2'], "История Беларуси", teacher_name[28], "209"), ("", lesson_time['3s'], "Допризывная подготовка", teacher_name[9], "119")]
        ]
    },
    "М56": {
        "UP": [
            [("", lesson_time['1'], "Белорусская литература", teacher_name[55], "309"), ("", lesson_time[
                '2'], "Химия", teacher_name[44], "202"), ("", lesson_time['3'], "Математика ", teacher_name[45], "119")],
            [("", lesson_time['1'], "Математика ", teacher_name[45], "119"), ("", lesson_time['2'], "Химия",
                                                                              teacher_name[44], "212"), ("", lesson_time['3'], "Русский язык", teacher_name[60], "20")],
            [("", lesson_time['1'], "Физическая культура и здоровье ", teacher_name[59] + '/' + "Кульба А. В. ", "с/з"), ("", lesson_time['2'], "История Беларуси",
                                                                                                                          teacher_name[75], "120"), ("", lesson_time['3'], "Иностранный язык", teacher_name[53] + '/' + teacher_name[77] + '/' + teacher_name[21], "315/314/318")],
            [("", lesson_time['1'], "Физика", teacher_name[16], ""), ("", lesson_time['2'], "Математика ",
                                                                      teacher_name[45], "124"), ("", lesson_time['3'], "Обществоведение", teacher_name[28], "")],
            [("", lesson_time['1'], "Биология", teacher_name[38], "210"), ("", lesson_time['2'], "Физика",
                                                                           teacher_name[16], "202"), ("", lesson_time['3'], "География", teacher_name[52], "307")],
            [("", lesson_time['1'], "Допризывная подготовка", teacher_name[9], "119"), ("", lesson_time[
                '2'], "Биология", teacher_name[38], "212"), ("", lesson_time['3s'], "Белорусский язык", teacher_name[21], "310")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Белорусская литература", teacher_name[55], "309"), ("", lesson_time[
                '2'], "Русская литература", teacher_name[2], "120"), ("", lesson_time['3'], "Математика ", teacher_name[45], "119")],
            [("", lesson_time['1'], "Математика ", teacher_name[45], "119"), ("", lesson_time['2'], "Химия",
                                                                              teacher_name[44], "212"), ("", lesson_time['3'], "Русский язык", teacher_name[60], "20")],
            [("", lesson_time['1'], "Физическая культура и здоровье ", teacher_name[59] + '/' + "Кульба А. В. ", "с/з"), ("", lesson_time['2'], "История Беларуси",
                                                                                                                          teacher_name[75], "120"), ("", lesson_time['3'], "Иностранный язык", teacher_name[53] + '/' + teacher_name[77] + '/' + teacher_name[21], "315/314/318")],
            [("", lesson_time['1'], "Физика", teacher_name[16], ""), ("", lesson_time['2'], "Математика ",
                                                                      teacher_name[45], "124"), ("", lesson_time['3'], "Обществоведение", teacher_name[28], "")],
            [("", lesson_time['1'], "История Беларуси", teacher_name[75], "121"), ("", lesson_time[
                '2'], "Русская литература", teacher_name[2], "121"), ("", lesson_time['3'], "География", teacher_name[52], "307")],
            [("", lesson_time['1'], "Допризывная подготовка", teacher_name[9], "119"), ("", lesson_time[
                '2'], "Биология", teacher_name[38], "212"), ("", lesson_time['3s'], "Белорусский язык", teacher_name[21], "310")]
        ]
    },
    "М57": {
        "UP": [
            [("", lesson_time['1'], "Иностранный язык", teacher_name[53] + '/' + teacher_name[77] + '/' + teacher_name[21], "311/314/318"),
             ("", lesson_time['2'], "Математика ", teacher_name[45], "119"), ("", lesson_time['3'], "Русский язык", teacher_name[56], "312")],
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Белорусский язык",
                                                                        teacher_name[55], "302"), ("", lesson_time['3'], "Математика ", teacher_name[45], "119")],
            [("", lesson_time['1'], "Допризывная подготовка", teacher_name[9], "119"), ("", lesson_time['2'], "Физическая культура и здоровье",
                                                                                        teacher_name[59] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['3'], "История Беларуси", teacher_name[75], "120")],
            [("", lesson_time['2'], "Русская литература", teacher_name[56], "312"), ("", lesson_time[
                '3'], "Математика ", teacher_name[45], "124"), ("", lesson_time['4'], "Физика", teacher_name[16], "")],
            [("", lesson_time['1'], "География", teacher_name[52], "111"), ("", lesson_time[
                '2'], "Биология", teacher_name[38], "212"), ("", lesson_time['3'], "Физика", teacher_name[16], "202")],
            [("", lesson_time['1'], "Белорусский язык", teacher_name[55], "305"), ("", lesson_time[
                '2'], "Белорусская литература", teacher_name[55], "305"), ("", lesson_time['3s'], "Обществоведение", teacher_name[28], "121")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Иностранный язык", teacher_name[53] + '/' + teacher_name[77] + '/' + teacher_name[21], "311/314/318"),
             ("", lesson_time['2'], "Математика ", teacher_name[45], "119"), ("", lesson_time['3'], "Русский язык", teacher_name[56], "312")],
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Биология",
                                                                        teacher_name[38], "307"), ("", lesson_time['3'], "Математика ", teacher_name[45], "119")],
            [("", lesson_time['1'], "Допризывная подготовка", teacher_name[9], "119"), ("", lesson_time['2'], "Физическая культура и здоровье",
                                                                                        teacher_name[59] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['3'], "История Беларуси", teacher_name[75], "120")],
            [("", lesson_time['1'], "Химия", teacher_name[44], "212"), ("", lesson_time['2'], "Русская литература",
                                                                        teacher_name[56], "312"), ("", lesson_time['3'], "Математика ", teacher_name[45], "124")],
            [("", lesson_time['1'], "География", teacher_name[52], "111"), ("", lesson_time[
                '2'], "Биология", teacher_name[38], "212"), ("", lesson_time['3'], "Физика", teacher_name[16], "202")],
            [("", lesson_time['1'], "История Беларуси", teacher_name[75], "111"), ("", lesson_time[
                '2'], "Белорусская литература", teacher_name[55], "305"), ("", lesson_time['3s'], "Обществоведение", teacher_name[28], "121")]
        ]
    },
    "Ю44": {
        "UP": [
            [("", lesson_time['1'], "Русский язык", teacher_name[2], "120"), ("", lesson_time['2'], "Физкультура и здоровье",
                                                                              teacher_name[68] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['3'], "Математика", teacher_name[71], "202")],
            [("", lesson_time['1'], "Обществоведение", teacher_name[41], "209"), ("", lesson_time['2'], "Информатика", teacher_name[58] + '/' + "Гац",
                                                                                  "205/209"), ("", lesson_time['3'], "Биология", teacher_name[24], "120"), ("", lesson_time['4'], "История Беларуси", teacher_name[28], "124")],
            [("", lesson_time['1'], "Физика", teacher_name[16], "202"), ("", lesson_time['2'], "Русская литература",
                                                                         teacher_name[2], "121"), ("", lesson_time['3'], "Математика", teacher_name[71], "124")],
            [("", lesson_time['1'], "География", teacher_name[52], "307"), ("", lesson_time['2'], "Иностранный язык", teacher_name[12] + '/' +
                                                                            teacher_name[73] + '/' + teacher_name[80], "20/321/310"), ("", lesson_time['3'], "Белорусская литература", teacher_name[30], "302")],
            [("", lesson_time['1'], "Допризывная (Медицинская) подготовка", teacher_name[9] + '/' + teacher_name[40], "119/212"), ("",
                                                                                                                                   lesson_time['2'], "Математика", teacher_name[71], "124"), ("", lesson_time['3'], "Белорусский язык", teacher_name[30], "207")],
            [("", lesson_time['1'], "История Беларуси", teacher_name[28], "209"), ("", lesson_time[
                '2'], "Физика", teacher_name[16], "202"), ("", lesson_time['3s'], "Биология", teacher_name[24], "207")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Русский язык", teacher_name[2], "120"), ("", lesson_time['2'], "Физкультура и здоровье",
                                                                              teacher_name[68] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['3'], "Математика", teacher_name[71], "202")],
            [("", lesson_time['1'], "Обществоведение", teacher_name[41], "209"), ("", lesson_time['2'], "Информатика", teacher_name[
                58] + '/' + "Гац", "205/209"), ("", lesson_time['3'], "Белорусская литература", teacher_name[30], "120")],
            [("", lesson_time['1'], "Белорусский язык", teacher_name[30], "207"), ("", lesson_time[
                '2'], "Русская литература", teacher_name[2], "121"), ("", lesson_time['3'], "Математика", teacher_name[71], "124")],
            [("", lesson_time['1'], "География", teacher_name[52], "307"), ("", lesson_time['2'], "Иностранный язык", teacher_name[12] + '/' +
                                                                            teacher_name[73] + '/' + teacher_name[80], "20/321/310"), ("", lesson_time['3'], "Информатика", teacher_name[58] + '/' + "Гац", "205/315")],
            [("", lesson_time['1'], "Допризывная (Медицинская) подготовка", teacher_name[9] + '/' + teacher_name[40], "119/212"), ("",
                                                                                                                                   lesson_time['2'], "Математика", teacher_name[71], "124"), ("", lesson_time['3'], "Обществоведение", teacher_name[41], "212")],
            [("", lesson_time['1'], "История Беларуси", teacher_name[28], "209"), ("", lesson_time[
                '2'], "Физика", teacher_name[16], "202"), ("", lesson_time['3s'], "Биология", teacher_name[24], "207")]
        ]
    },
    "С84": {
        "UP": [
            [("", lesson_time['1'], "Строит.маш.и обор/Тех.механика ", teacher_name[50] + '/' + teacher_name[72], "102/302"), ("", lesson_time['2'], "Строит.маш.и обор/Тех.механика ", teacher_name[50] + '/' + teacher_name[72],
                                                                                                                               "102/302"), ("", lesson_time['3'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "200/302/120"), ("", lesson_time['4'], "Техническая механика", teacher_name[72], "302")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[72], "305"), ("", lesson_time['2'], "Инженерная графика ", teacher_name[
                22] + '/' + teacher_name[23], "319/321"), ("", lesson_time['3'], "Физкультура и здоровье ", teacher_name[59], "с/з")],
            [("", lesson_time['1'], "Строит.мат.и изделия/КП ГПЗ ", teacher_name[6] + '/' + teacher_name[48], "10/209"), ("", lesson_time['2'],
                                                                                                                          "Техническая механика", teacher_name[72], "302"), ("", lesson_time['3'], "Осн.электротехники", teacher_name[29], "102")],
            [("", lesson_time['1'], "Физкультура и здоровье", teacher_name[59], "с/з"), ("", lesson_time['2'], "Строит.машины и оборудование",
                                                                                         teacher_name[50], "102"), ("", lesson_time['3'], "Осн. электротехн./КП ГПЗ", teacher_name[29] + '/' + teacher_name[48], "104/209")],
            [("", lesson_time['1'], "Строит.мат.и изделия/КП ГПЗ ", teacher_name[6] + '/' + teacher_name[48], "10/209"), ("", lesson_time['2'], "Строит.мат.и изделия",
                                                                                                                          teacher_name[6], "102"), ("", lesson_time['3'], "Информационные технологии ", teacher_name[15] + '/' + teacher_name[48], "314/209")],
            [("", lesson_time['1'], "Строит.мат.и изделия", teacher_name[6], "104"), ("", lesson_time['2'], "Строит.машины и оборудование",
                                                                                      teacher_name[50], "102"), ("", lesson_time['3s'], "Инженерная графика ", teacher_name[22] + '/' + teacher_name[23], "319/321")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Строит.маш.и обор/Тех.механика ", teacher_name[50] + '/' + teacher_name[72], "102/302"), ("", lesson_time['2'], "Строит.маш.и обор/Тех.механика ", teacher_name[50] + '/' + teacher_name[72],
                                                                                                                               "102/302"), ("", lesson_time['3'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "200/302/120"), ("", lesson_time['4'], "Информационные технологии", teacher_name[15], "114")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[72], "305"), ("", lesson_time['2'], "Инженерная графика ", teacher_name[
                22] + '/' + teacher_name[23], "319/321"), ("", lesson_time['3'], "Физкультура и здоровье ", teacher_name[59], "с/з")],
            [("", lesson_time['1'], "Строит.мат.и изделия/КП ГПЗ ", teacher_name[6] + '/' + teacher_name[48], "10/209"), ("", lesson_time['2'], "Техническая механика",
                                                                                                                          teacher_name[72], "302"), ("", lesson_time['3'], "Осн. электротехн./КП ГПЗ ", teacher_name[29] + '/' + teacher_name[48], "311/209")],
            [("", lesson_time['1'], "Осн.электротехники", teacher_name[29], "104"), ("", lesson_time['2'], "ГПЗ", teacher_name[48], "209"), ("", lesson_time[
                '3'], "Осн. электротехн./КП ГПЗ", teacher_name[29] + '/' + teacher_name[48], "104/209"), ("", lesson_time['4'], "Информационные технологии", teacher_name[48], "209")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "314/318/321"), ("", lesson_time['2'],
                                                                                                                                             "Строит.мат.и изделия", teacher_name[6], "102"), ("", lesson_time['3'], "Информационные технологии ", teacher_name[15] + '/' + teacher_name[48], "314/209")],
            [("", lesson_time['1'], "Строит.мат.и изделия", teacher_name[6], "104"), ("", lesson_time['2'], "Строит.машины и оборудование",
                                                                                      teacher_name[50], "102"), ("", lesson_time['3s'], "Инженерная графика ", teacher_name[22] + '/' + teacher_name[23], "319/321")]
        ]
    },
    "С85": {
        "UP": [
            [("", lesson_time['1'], "Строит.мат.и изделия", teacher_name[6], "104"), ("", lesson_time['2'], "Инженерная графика ", teacher_name[22] + '/' +
                                                                                      teacher_name[23], "106/321"), ("", lesson_time['3'], "Строит.маш.и обор/Тех.механика", teacher_name[50] + '/' + teacher_name[51], "102/207")],
            [("", lesson_time['1'], "Информационные технологии ", teacher_name[51], "205"), ("", lesson_time['2'], "Техническая механика ", teacher_name[51], "207"),
             ("", lesson_time['3'], "Физкультура и здоровье", "Шукис О. В.", "с/з"), ("", lesson_time['4'], "Информационные технологии", teacher_name[48], "209")],
            [("", lesson_time['1'], "Осн.электротехники", teacher_name[29], "102"), ("", lesson_time['2'], "Строит.мат.и изделия/Осн.электротехн", teacher_name[6] + '/' + teacher_name[29], "10/205"), ("",
                                                                                                                                                                                                         lesson_time['3'], "КП ГПЗ ", teacher_name[48] + '/' + teacher_name[15], "209/106"), ("", lesson_time['4'], "Строит.мат.и изделия/Осн.электротехн", teacher_name[6] + '/' + teacher_name[29], "10/315")],
            [("", lesson_time['1'], "Строит.машины и оборудование", teacher_name[50], "102"), ("", lesson_time['2'], "ГПЗ", teacher_name[48], "209"), ("", lesson_time['3'], "Строит.маш.и обор/Тех.механика",
                                                                                                                                                       teacher_name[50] + '/' + teacher_name[51], "102/207"), ("", lesson_time['4'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "309/200/120")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[51], "207"), ("", lesson_time['2'], "КП ГПЗ", teacher_name[48] + '/' + teacher_name[15],
                                                                                       "209/106"), ("", lesson_time['3'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "310/318/321")],
            [("", lesson_time['1'], "Строит.машины и оборудование ", teacher_name[50], "102"), ("", lesson_time['2'], "Инженерная графика ", teacher_name[22] + '/' + teacher_name[23],
                                                                                                "319/321"), ("", lesson_time['3s'], "Строит.мат.и изделия", teacher_name[6], "104"), ("", lesson_time['4s'], "Физкультура и здоровье", "Шукис О. В.", "с/з")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Строит.мат.и изделия", teacher_name[6], "104"), ("", lesson_time['2'], "Инженерная графика ", teacher_name[22] + '/' +
                                                                                      teacher_name[23], "106/321"), ("", lesson_time['3'], "Строит.маш.и обор/Тех.механика", teacher_name[50] + '/' + teacher_name[51], "102/207")],
            [("", lesson_time['1'], "Информационные технологии ", teacher_name[51], "205"), ("", lesson_time['2'], "Техническая механика ", teacher_name[51], "207"),
             ("", lesson_time['3'], "Физкультура и здоровье", "Шукис О. В.", "с/з"), ("", lesson_time['4'], "Информационные технологии", teacher_name[48], "209")],
            [("", lesson_time['1'], "Осн.электротехники", teacher_name[29], "102"), ("", lesson_time[
                '2'], "Строит.мат.и изделия/Осн.электротехн", teacher_name[6] + '/' + teacher_name[29], "10/205")],
            [("", lesson_time['1'], "Информационные технологии ", teacher_name[51], "209/205"), ("", lesson_time['2'], "Техническая механика",
                                                                                                 teacher_name[51], "207"), ("", lesson_time['3'], "Строит.маш.и обор/Тех.механика", teacher_name[50] + '/' + teacher_name[51], "102/207")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[51], "207"), ("", lesson_time['2'], "КП ГПЗ", teacher_name[48] + '/' + teacher_name[15],
                                                                                       "209/106"), ("", lesson_time['3'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "310/318/321")],
            [("", lesson_time['1'], "Строит.машины и оборудование ", teacher_name[50], "102"), ("", lesson_time['2'], "Инженерная графика ",
                                                                                                teacher_name[22] + '/' + teacher_name[23], "319/321"), ("", lesson_time['3s'], "Строит.мат.и изделия", teacher_name[6], "104")]
        ]
    },
    "С83": {
        "UP": [
            [("", lesson_time['1'], "Информационные технологии", teacher_name[15] + '/' + teacher_name[17], "205"), ("", lesson_time['2'], "Иностранный язык", teacher_name[53] +
                                                                                                                     '/' + teacher_name[77] + '/' + teacher_name[21], "315/314/318"), ("", lesson_time['3'], "КП ГПЗ", teacher_name[15] + '/' + teacher_name[17], "106/109")],
            [("", lesson_time['1'], "Осн.электротехники", teacher_name[29], "102"), ("", lesson_time['2'], "Физкультура и здоровье",
                                                                                     "Шукис О. В.", "с/з"), ("", lesson_time['3'], "Инженерная графика", teacher_name[22] + '/' + teacher_name[23], "319/321")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[53] + '/' + teacher_name[77] + '/' + teacher_name[21], "315/314/318"), ("", lesson_time['2'], "Строит.маш.и обор/Тех.механика", teacher_name[5] + '/' +
                                                                                                                                             teacher_name[54], "109/104"), ("", lesson_time['3'], "Строит.мат.и изделия", teacher_name[6], "104"), ("", lesson_time['4'], "Строит.маш.и  обор/Тех.механика", teacher_name[5] + '/' + teacher_name[54], "109/102")],
            [("", lesson_time['1'], "Строит.мат.и изделия", teacher_name[6], "106"), ("", lesson_time['2'], "Строит.мат.и изделия/Осн.электротехн",
                                                                                      teacher_name[6] + '/' + teacher_name[29], "10/205"), ("", lesson_time['3'], "Строит.машины и оборудование", teacher_name[5], "106")],
            [("", lesson_time['1'], "Информационные технологии", teacher_name[15] + '/' + teacher_name[17], "205"), ("", lesson_time['2'], "Строит.маш.и обор/Тех.механика",
                                                                                                                     teacher_name[5] + '/' + teacher_name[54], "104/109"), ("", lesson_time['3'], "Техническая механика", teacher_name[54], "104")],
            [("", lesson_time['1'], "Инженерная графика", teacher_name[22] + '/' + teacher_name[23], "319/321"), ("", lesson_time['2'],
                                                                                                                  "Техническая механика", teacher_name[54], "106"), ("", lesson_time['3s'], "Физкультура и здоровье", "Шукис О. В.", "с/з")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Информационные технологии", teacher_name[15] + '/' + teacher_name[17], "205"), ("", lesson_time['2'], "Иностранный язык", teacher_name[53] +
                                                                                                                     '/' + teacher_name[77] + '/' + teacher_name[21], "315/314/318"), ("", lesson_time['3'], "КП ГПЗ", teacher_name[15] + '/' + teacher_name[17], "106/109")],
            [("", lesson_time['1'], "Осн.электротехники", teacher_name[29], "102"), ("", lesson_time['2'], "Физкультура и здоровье",
                                                                                     "Шукис О. В.", "с/з"), ("", lesson_time['3'], "Инженерная графика", teacher_name[22] + '/' + teacher_name[23], "319/321")],
            [("", lesson_time['1'], "ГПЗ", teacher_name[15], "106"), ("", lesson_time['2'], "Строит.маш.и обор/Тех.механика", teacher_name[5] + '/' + teacher_name[54],
                                                                      "109/104"), ("", lesson_time['3'], "Строит.мат.и изделия", teacher_name[6], "104"), ("", lesson_time['4'], "Техническая механика", teacher_name[54], "102")],
            [("", lesson_time['1'], "Строит.мат.и изделия", teacher_name[6], "106"), ("", lesson_time['2'], "Строит.мат.и изделия/Осн.электротехн", teacher_name[6] + '/' + teacher_name[29], "10/205"), ("",
                                                                                                                                                                                                          lesson_time['3'], "Строит.машины и оборудование", teacher_name[5], "106"), ("", lesson_time['4'], "Строит.мат.и изделия/Осн.электротехн", teacher_name[6] + '/' + teacher_name[29], "10/311")],
            [("", lesson_time['1'], "КП ГПЗ", teacher_name[15] + '/' + teacher_name[17], "106/109"), ("", lesson_time['2'],
                                                                                                      "Строит.машины и оборудование", teacher_name[5], "120"), ("", lesson_time['3'], "Техническая механика", teacher_name[54], "104")],
            [("", lesson_time['1'], "Инженерная графика", teacher_name[22] + '/' + teacher_name[23],
              "319/321"), ("", lesson_time['2'], "Техническая механика", teacher_name[54], "106")]
        ]
    },
    "Ср22": {
        "UP": [
            [("", lesson_time['1'], "Инженерная графика ", teacher_name[22] + '/' + teacher_name[23], "106/321"), ("", lesson_time['2'], "Строит.мат.и изделия/КП ГПЗ", teacher_name[6] + '/' + teacher_name[17],
                                                                                                                   "10/109"), ("", lesson_time['3'], "Техническая механика ", teacher_name[54], "104"), ("", lesson_time['4'], "Информационные технологии", teacher_name[15] + '/' + teacher_name[17], "114/205")],
            [("", lesson_time['1'], "Инженерная графика", teacher_name[22] + '/' + teacher_name[23], "319/321"), ("", lesson_time['2'], "Осн. электротехн./КП ГПЗ ", teacher_name[29] + '/' +
                                                                                                                  teacher_name[17], "311/109"), ("", lesson_time['3'], "Осн.электротехники", teacher_name[29], "102"), ("", lesson_time['4'], "Физкультура и здоровье ", teacher_name[59], "с/з")],
            [("", lesson_time['1'], "Строит.маш.и обор/Тех.механика ", teacher_name[5] + '/' + teacher_name[54], "109/104"), ("", lesson_time['2'], "Информационные технологии ",
                                                                                                                              teacher_name[15] + '/' + teacher_name[17], "210/209"), ("", lesson_time['3'], "Строит.маш.и обор/Тех.механика", teacher_name[5] + '/' + teacher_name[54], "109/111")],
            [("", lesson_time['1'], "Осн.электротехники", teacher_name[29], "104"), ("", lesson_time['2'], "Строит.машины и оборудование", teacher_name[
                5], "104"), ("", lesson_time['3'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "109/200/120")],
            [("", lesson_time['1'], "Строит.машины и оборудование", teacher_name[5], "102"), ("", lesson_time['2'], "Иностранный язык", teacher_name[
                12] + '/' + teacher_name[73] + '/' + teacher_name[80], "314/318/321"), ("", lesson_time['3'], "Строит.мат.и изделия", teacher_name[6], "102")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[54], "106"),
             ("", lesson_time['2'], "Строит.машины и оборудование ", teacher_name[5], "104")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Инженерная графика ", teacher_name[22] + '/' + teacher_name[23], "106/321"), ("", lesson_time['2'], "Строит.мат.и изделия/КП ГПЗ", teacher_name[6] +
                                                                                                                   '/' + teacher_name[17], "10/109"), ("", lesson_time['3'], "Техническая механика ", teacher_name[54], "104"), ("", lesson_time['4'], "ГПЗ ", teacher_name[17], "104")],
            [("", lesson_time['1'], "Инженерная графика", teacher_name[22] + '/' + teacher_name[23], "319/321"), ("", lesson_time['2'], "Осн. электротехн./КП ГПЗ ", teacher_name[29] + '/' + teacher_name[17],
                                                                                                                  "311/109"), ("", lesson_time['3'], "Осн. электротехн./КП ГПЗ", teacher_name[29] + '/' + teacher_name[17], "311/109"), ("", lesson_time['4'], "Физкультура и здоровье ", teacher_name[59], "с/з")],
            [("", lesson_time['1'], "Строит.маш.и обор/Тех.механика ", teacher_name[5] + '/' + teacher_name[54], "109/104"), ("", lesson_time['2'], "Информационные технологии ",
                                                                                                                              teacher_name[15] + '/' + teacher_name[17], "210/209"), ("", lesson_time['3'], "Строит.маш.и обор/Тех.механика", teacher_name[5] + '/' + teacher_name[54], "109/111")],
            [("", lesson_time['1'], "Физкультура и здоровье", teacher_name[59], "с/з"), ("", lesson_time['2'], "Строит.машины и оборудование", teacher_name[5],
                                                                                         "104"), ("", lesson_time['3'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "109/200/120")],
            [("", lesson_time['1'], "Строит.мат.и изделия", teacher_name[6], "102"), ("", lesson_time['2'], "Техническая механика", teacher_name[
                54], "104"), ("", lesson_time['3'], "Строит.мат.и изделия/КП ГПЗ ", teacher_name[6] + '/' + teacher_name[17], "10/102")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[54], "106"),
             ("", lesson_time['2'], "Строит.машины и оборудование ", teacher_name[5], "104")]
        ]
    },
    "Р51": {
        "UP": [
            [("", lesson_time['1'], "ЭРЭ и УФЭ", teacher_name[64], "305"), ("", lesson_time['2'], "ЭРИ/Осн.электр.и микроэл ", teacher_name[64] +
                                                                            '/' + teacher_name[81], "300/311"), ("", lesson_time['3'], "САПР/Инж. графика ", teacher_name[18] + '/' + teacher_name[72], "210/305")],
            [("", lesson_time['1'], "Источники питания РЭУ", teacher_name[74], "302"), ("", lesson_time[
                '2'], "Физическая культура", teacher_name[59], "с/з"), ("", lesson_time['3'], "САПР", teacher_name[18], "210")],
            [("", lesson_time['1'], "Электрорадиоматериалы", teacher_name[7], "307"), ("", lesson_time['2'], "Электрорад.материалы/ЭРЭиУФЭ", teacher_name[7] +
                                                                                       '/' + teacher_name[64], "308/300"), ("", lesson_time['3'], "ЭРИ/Стандартиз.и сертификац", teacher_name[64] + '/' + teacher_name[33], "300/311")],
            [("", lesson_time['1'], "Радиотехника/КП ТОЭ", teacher_name[81] + '/' + teacher_name[74], "311/302"), ("", lesson_time['2'], "Радиотехника ",
                                                                                                                   teacher_name[81], "311"), ("", lesson_time['3'], "Иностранный язык", teacher_name[21] + '/' + teacher_name[77] + '/' + teacher_name[39], "318/314/312")],
            [("", lesson_time['1'], "Импульсная и цифровая техника ", teacher_name[7], "307"), ("", lesson_time['2'], "Осн.электроники и микроэлектроники ",
                                                                                                teacher_name[81], "311"), ("", lesson_time['3'], "Имп. и цифр.техника/Ист. пит.РЭУ", teacher_name[7] + '/' + teacher_name[74], "210/311")],
            [("", lesson_time['1'], "ОСГН", teacher_name[75], "120"), ("", lesson_time['2'], "Иностранный язык", teacher_name[
                77] + '/' + teacher_name[21], "314/318"), ("", lesson_time['3s'], "Стандартизац.и сертификац.", teacher_name[33], "302")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Электрорадиоматериалы", teacher_name[7], "307"), ("", lesson_time['2'], "ЭРИ", teacher_name[
                64], "305"), ("", lesson_time['3'], "САПР/Инж. графика ", teacher_name[18] + '/' + teacher_name[72], "210/305")],
            [("", lesson_time['1'], "Источники питания РЭУ", teacher_name[74], "302"),
             ("", lesson_time['2'], "Физическая культура", teacher_name[59], "с/з")],
            [("", lesson_time['1'], "ТОЭ", teacher_name[74], "302"), ("", lesson_time['2'], "ЭРИ/ТОЭ ", teacher_name[64] + '/' +
                                                                      teacher_name[74], "300/311"), ("", lesson_time['3'], "САПР/Инж. графика", teacher_name[18] + '/' + teacher_name[72], "210/307")],
            [("", lesson_time['1'], "Радиотехника/КП ТОЭ", teacher_name[81] + '/' + teacher_name[74], "311/302"), ("", lesson_time['2'], "Радиотехника ",
                                                                                                                   teacher_name[81], "311"), ("", lesson_time['3'], "Иностранный язык", teacher_name[21] + '/' + teacher_name[77] + '/' + teacher_name[39], "318/314/312")],
            [("", lesson_time['1'], "Импульсная и цифровая техника ", teacher_name[7], "307"), ("", lesson_time['2'], "Осн.электроники и микроэлектроники ", teacher_name[81], "311"), ("", lesson_time[
                '3'], "Имп. и цифр.техника/Ист. пит.РЭУ", teacher_name[7] + '/' + teacher_name[74], "210/311"), ("", lesson_time['4'], "Физкультура и здоровье", teacher_name[59], "с/з")],
            [("", lesson_time['1'], "ТОЭ", teacher_name[74], "302"), ("", lesson_time['2'], "Иностранный язык", teacher_name[
                77] + '/' + teacher_name[21], "314/318"), ("", lesson_time['3s'], "Стандартизац.и сертификац.", teacher_name[33], "302")]
        ]
    },
    "Р52": {
        "UP": [
            [("", lesson_time['1'], "Электрорадиоматериалы", teacher_name[7], "307"), ("", lesson_time['2'], "Импульсная и цифровая техника",
                                                                                       teacher_name[7], "307"), ("", lesson_time['3'], "ЭРИ/Осн.электр.и микроэл", teacher_name[64] + '/' + teacher_name[81], "300/311")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[77] + '/' + teacher_name[53], "314/318"), ("", lesson_time['2'],
                                                                                                                "САПР/Инж. графика", teacher_name[18] + '/' + teacher_name[72], "210/305"), ("", lesson_time['3'], "ОСГН", teacher_name[63], "121")],
            [("", lesson_time['1'], "ЭРИ/ТОЭ", teacher_name[64] + '/' + teacher_name[74], "300/311"), ("", lesson_time['2'], "ТОЭ",
                                                                                                       teacher_name[74], "307"), ("", lesson_time['3'], "САПР/Инж. графика", teacher_name[18] + '/' + teacher_name[72], "210/307")],
            [("", lesson_time['1'], "Физическая культура", teacher_name[66], "с/з"), ("", lesson_time['2'],
                                                                                      "Источники питания РЭУ", teacher_name[74], "302"), ("", lesson_time['3'], "Радиотехника", teacher_name[81], "311")],
            [("", lesson_time['1'], "Радиотехника/КП ТОЭ", teacher_name[81] + '/' + teacher_name[74], "311/104"), ("", lesson_time['2'], "Имп. и цифр.техника/Ист. пит.РЭУ",
                                                                                                                   teacher_name[7] + '/' + teacher_name[74], "210/315"), ("", lesson_time['3'], "Осн.электроники и микроэлектроники", teacher_name[81], "302")],
            [("", lesson_time['1'], "ТОЭ", teacher_name[74], "302"), ("", lesson_time['2'], "Стандартизац.и сертификац.", teacher_name[
                33], "302"), ("", lesson_time['3s'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "311/312/318")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "ЭРИ", teacher_name[64], "305"), ("", lesson_time['2'], "Импульсная и цифровая техника",
                                                                      teacher_name[7], "307"), ("", lesson_time['3'], "ЭРЭ и УФЭ", teacher_name[64], "307")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[77] + '/' + teacher_name[53], "314/318"), ("", lesson_time['2'],
                                                                                                                "САПР/Инж. графика", teacher_name[18] + '/' + teacher_name[72], "210/305"), ("", lesson_time['3'], "САПР", teacher_name[18], "210")],
            [("", lesson_time['1'], "Электрорад.материалы/ЭРЭиУФЭ", teacher_name[7] + '/' + teacher_name[64], "308/300"), ("", lesson_time['2'], "Электрорадиоматериалы",
                                                                                                                           teacher_name[7], "307"), ("", lesson_time['3'], "ЭРИ/Стандартиз.и сертификац.", teacher_name[64] + '/' + teacher_name[33], "300/311а")],
            [("", lesson_time['1'], "Физическая культура", teacher_name[66], "с/з"), ("", lesson_time['2'],
                                                                                      "Источники питания РЭУ", teacher_name[74], "302"), ("", lesson_time['3'], "Радиотехника", teacher_name[81], "311")],
            [("", lesson_time['1'], "Радиотехника/КП ТОЭ", teacher_name[81] + '/' + teacher_name[74], "311/104"), ("", lesson_time['2'], "Имп. и цифр.техника/Ист. пит.РЭУ",
                                                                                                                   teacher_name[7] + '/' + teacher_name[74], "210/315"), ("", lesson_time['3'], "Осн.электроники и микроэлектроники", teacher_name[81], "302")],
            [("", lesson_time['1'], "Физкультура и здоровье", teacher_name[66], "с/з"), ("", lesson_time['2'], "Стандартизац.и сертификац.", teacher_name[33],
                                                                                         "302"), ("", lesson_time['3s'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "311/312/318")]
        ]
    },
    "М53": {
        "UP": [
            [("", lesson_time['1'], "Техническая механика", teacher_name[25], "121"), ("", lesson_time[
                '2'], "Инженерная графика ", teacher_name[82] + '/' + teacher_name[35], "319/200")],
            [("", lesson_time['1'], "Материалов.и техн.материал", teacher_name[82], "310"), ("", lesson_time['2'], "Электротехн/Материаловедение ", teacher_name[16] + '/' + teacher_name[82],
                                                                                             "202/310"), ("", lesson_time['3'], "Техническая механика", teacher_name[25], "207"), ("", lesson_time['4'], "Физкультура и здоровье", teacher_name[68], "с/з")],
            [("", lesson_time['1'], "Обраб.мат.и инстр.", teacher_name[8], "310"), ("", lesson_time['2'], "Электротехн. с осн.элетрон",
                                                                                    teacher_name[16], "202"), ("", lesson_time['3'], "Инженерная графика", teacher_name[82], "319/200")],
            [("", lesson_time['1'], "Материалов. и техн. материал.", teacher_name[82], "319"), ("", lesson_time['2'], "Иностранный язык", teacher_name[
                77] + '/' + teacher_name[53] + '/' + teacher_name[21], "314/315/318"), ("", lesson_time['3'], "Нормир.точн.и тех.изм ", teacher_name[26], "309")],
            [("", lesson_time['1'], "Инженерная графика ", teacher_name[82] + '/' + teacher_name[35], "319/200"), ("", lesson_time['2'], "Нормир.точн.и тех.изм/Обраб.мат. ", teacher_name[26] + '/' + teacher_name[8],
                                                                                                                   "309/310"), ("", lesson_time['3'], "КП Технич. механика ", teacher_name[25] + '/' + teacher_name[37], "114/111"), ("", lesson_time['4'], "Техническая механика", teacher_name[25], "111")],
            [("", lesson_time['1'], "Электротехн/Материаловедение ", teacher_name[16] + '/' + teacher_name[82], "202/309"), ("",
                                                                                                                             lesson_time['2'], "ОСГН", teacher_name[75], "120"), ("", lesson_time['3s'], "Мет.станки", teacher_name[69], "111")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Техническая механика/Мет. станки ", teacher_name[25] + '/' + teacher_name[69], "114/111"),
             ("", lesson_time['2'], "Инженерная графика ", teacher_name[82] + '/' + teacher_name[35], "319/200")],
            [("", lesson_time['1'], "Материалов.и техн.материал", teacher_name[82], "310"), ("", lesson_time['2'], "Электротехн/Материаловедение ", teacher_name[16] + '/' + teacher_name[82],
                                                                                             "202/310"), ("", lesson_time['3'], "Техническая механика", teacher_name[25], "207"), ("", lesson_time['4'], "Физкультура и здоровье", teacher_name[68], "с/з")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[77] + '/' + teacher_name[53] + '/' + teacher_name[21], "314/315/318"), ("",
                                                                                                                                             lesson_time['2'], "Электротехн. с осн. электрон.", teacher_name[16], "202"), ("", lesson_time['3'], "Обраб.мат.и инстр.", teacher_name[8], "310")],
            [("", lesson_time['1'], "Материалов. и техн. материал.", teacher_name[82], "319"), ("", lesson_time['2'], "Иностранный язык", teacher_name[
                77] + '/' + teacher_name[53] + '/' + teacher_name[21], "314/315/318"), ("", lesson_time['3'], "Нормир.точн.и тех.изм ", teacher_name[26], "309")],
            [("", lesson_time['1'], "Инженерная графика ", teacher_name[82] + '/' + teacher_name[35], "319/200"), ("", lesson_time['2'],
                                                                                                                   "Нормир.точн.и тех.изм/Обраб.мат. ", teacher_name[26] + '/' + teacher_name[8], "309/310"), ("", lesson_time['3'], "Мет. станки", teacher_name[69], "111")],
            [("", lesson_time['1'], "Физкультура и здоровье", teacher_name[68], "с/з"), ("", lesson_time['2'],
                                                                                         "ОСГН", teacher_name[75], "120"), ("", lesson_time['3s'], "Мет.станки", teacher_name[69], "111")]
        ]
    },
    "М54": {
        "UP": [
            [("", lesson_time['1'], "Инженерная графика", teacher_name[82] + '/' + teacher_name[35],
              "319/200"), ("", lesson_time['2'], "Обраб.мат.и инстр.", teacher_name[8], "312")],
            [("", lesson_time['1'], "Техническая механика/Мет.станки", teacher_name[25] + '/' + teacher_name[69], "315/111"), ("",
                                                                                                                               lesson_time['2'], "Нормир.точн.и тех.изм", teacher_name[26], "309"), ("", lesson_time['3'], "Мет.станки", teacher_name[69], "111")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[25], "111"), ("", lesson_time['2'], "Материалов.и техн.материал", teacher_name[82], "309"),
             ("", lesson_time['3'], "Электротехн. с осн.элетрон", teacher_name[16], "202"), ("", lesson_time['4'], "Физкультура и здоровье", teacher_name[68], "с/з")],
            [("", lesson_time['1'], "Техническая механика ", teacher_name[25], "111"), ("", lesson_time['2'], "Инженерная графика",
                                                                                        teacher_name[82] + '/' + teacher_name[35], "319/200"), ("", lesson_time['3'], "ОСГН", teacher_name[63], "121")],
            [("", lesson_time['1'], "Нормир.точн.и тех.изм/Обраб.мат. ", teacher_name[26] + '/' + teacher_name[8], "300/312"), ("", lesson_time['2'],
                                                                                                                                "Материал.и техн.материал", teacher_name[82], "319"), ("", lesson_time['3'], "Инженерная графика ", teacher_name[82], "319/200")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "310/311/312"), ("", lesson_time['2'],
                                                                                                                                             "Материал.и техн.материал", teacher_name[82], "309"), ("", lesson_time['3s'], "Электротехн/Материаловедение", teacher_name[16] + '/' + teacher_name[82], "202/309")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Инженерная графика", teacher_name[82] + '/' + teacher_name[35], "319/200"), ("", lesson_time['2'],
                                                                                                                  "Обраб.мат.и инстр.", teacher_name[8], "312"), ("", lesson_time['3'], "Мет. станки", teacher_name[69], "111")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[25], "111"), ("", lesson_time[
                '2'], "Нормир.точн.и тех.изм", teacher_name[26], "309"), ("", lesson_time['3'], "Мет.станки", teacher_name[69], "111")],
            [("", lesson_time['1'], "Электротехн/Материаловедение ", teacher_name[16] + '/' + teacher_name[82], "202/309"), ("", lesson_time['2'], "Материалов.и техн.материал",
                                                                                                                             teacher_name[82], "309"), ("", lesson_time['3'], "Электротехн. с осн.элетрон", teacher_name[16], "202"), ("", lesson_time['4'], "Физкультура и здоровье", teacher_name[68], "с/з")],
            [("", lesson_time['1'], "Техническая механика ", teacher_name[25], "111"), ("", lesson_time['2'], "Инженерная графика",
                                                                                        teacher_name[82] + '/' + teacher_name[35], "319/200"), ("", lesson_time['3'], "ОСГН", teacher_name[63], "121")],
            [("", lesson_time['1'], "Нормир.точн.и тех.изм/Обраб.мат. ", teacher_name[26] + '/' + teacher_name[8], "300/312"), ("", lesson_time['2'], "Иностранный язык", teacher_name[12] +
                                                                                                                                '/' + teacher_name[73] + '/' + teacher_name[80], "314/318/321"), ("", lesson_time['3'], "КП Технич.механика", teacher_name[25] + '/' + teacher_name[37], "315/312")],
            [("", lesson_time['1'], "Иностранный язык", teacher_name[12] + '/' + teacher_name[73] + '/' + teacher_name[80], "310/311/312"), ("", lesson_time['2'],
                                                                                                                                             "Физкультура и здоровье", teacher_name[68], "с/з"), ("", lesson_time['3s'], "Электротехн/Материаловедение", teacher_name[16] + '/' + teacher_name[82], "202/309")]
        ]
    },
    "Мс55": {
        "UP": [
            [("", lesson_time['1'], "Обраб. мат. и инстр.", teacher_name[8], "312"), ("", lesson_time['2'], "Техническая механика", teacher_name[
                25], "309"), ("", lesson_time['3'], "Инженерная графика", teacher_name[82] + '/' + teacher_name[23], "319/321")],
            [("", lesson_time['1'], "Технол.обор./Нормир.точн.и тех.изм", teacher_name[37] + '/' + teacher_name[26], "312/309"), ("", lesson_time['2'], "Мет.станки/Маш.графика",
                                                                                                                                  teacher_name[69] + '/' + teacher_name[25], "111/315"), ("", lesson_time['3'], "Электротехн/Нормир.точн.и тех.изм", teacher_name[16] + '/' + teacher_name[26], "202/309")],
            [("", lesson_time['1'], "Инженерная графика", teacher_name[82], "319/321"), ("", lesson_time['2'], "Техн. механика/Обраб. мат.", teacher_name[25] +
                                                                                         '/' + teacher_name[8], "315/312"), ("", lesson_time['3'], "Физкультура и здоровье", "Кульба А. В." + '/' + teacher_name[66], "с/з")],
            [("", lesson_time['1'], "Нормир.точн.и тех.изм", teacher_name[26], "309"), ("", lesson_time['2'], "Материаловедение /Маш.графика", teacher_name[26] +
                                                                                        '/' + teacher_name[25], "309/315"), ("", lesson_time['3'], "Инженерная графика", teacher_name[82] + '/' + teacher_name[23], "319/321")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[25], "310"), ("", lesson_time['2'], "Технологическое оборудование",
                                                                                       teacher_name[37], "111"), ("", lesson_time['3'], "Материалов.и техн.материал", teacher_name[26], "309")],
            [("", lesson_time['1'], "Физкультура и здоровье", "Кульба А. В." + '/' + teacher_name[66], "с/з"), ("", lesson_time['2'],
                                                                                                                "Мет.станки", teacher_name[69], "111"), ("", lesson_time['3s'], "САПР", teacher_name[1] + '/' + teacher_name[20], "114/315")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Обраб. мат. и инстр.", teacher_name[8], "312"), ("", lesson_time['2'], "Техническая механика", teacher_name[
                25], "309"), ("", lesson_time['3'], "Инженерная графика", teacher_name[82] + '/' + teacher_name[23], "319/321")],
            [("", lesson_time['1'], "Технол.оборудование", teacher_name[37], "312/309"), ("", lesson_time['2'], "Мет.станки/Маш.графика", teacher_name[69] +
                                                                                          '/' + teacher_name[25], "111/315"), ("", lesson_time['3'], "Электротехн/Нормир.точн.и тех.изм", teacher_name[16] + '/' + teacher_name[26], "202/309")],
            [("", lesson_time['1'], "Техн.механика/Обраб.мат.", teacher_name[25] + '/' + teacher_name[8], "315/312"), ("", lesson_time['2'], "Техн. механика/Обраб. мат.",
                                                                                                                       teacher_name[25] + '/' + teacher_name[8], "315/312"), ("", lesson_time['3'], "Физкультура и здоровье", "Кульба А. В." + '/' + teacher_name[66], "с/з")],
            [("", lesson_time['1'], "Нормир.точн.и тех.изм", teacher_name[26], "309"), ("", lesson_time['2'], "Материаловедение /Маш.графика", teacher_name[26] +
                                                                                        '/' + teacher_name[25], "309/315"), ("", lesson_time['3'], "Инженерная графика", teacher_name[82] + '/' + teacher_name[23], "319/321")],
            [("", lesson_time['1'], "Техническая механика", teacher_name[25], "310"), ("", lesson_time['2'], "Технологическое оборудование", teacher_name[37], "111"), ("", lesson_time[
                '3'], "Материалов.и техн.материал", teacher_name[26], "309"), ("", lesson_time['4'], "КП Технич. механика ", teacher_name[25] + '/' + teacher_name[37], "315/312")],
            [("", lesson_time['1'], "Электротехн. с осн.элетрон", teacher_name[16], "202"), ("", lesson_time['2'], "Мет.станки",
                                                                                             teacher_name[69], "111"), ("", lesson_time['3s'], "САПР", teacher_name[1] + '/' + teacher_name[20], "114/315")]
        ]
    },
    "Юс42": {
        "UP": [
            [("", lesson_time['1'], "Трудовое право", teacher_name[27], "24"), ("", lesson_time['2'], "ИГиП Беларуси", teacher_name[
                41], "209"), ("", lesson_time['3'], "Иностранный язык (проф.лекс)", teacher_name[53] + '/' + teacher_name[77], "315/314")],
            [("", lesson_time['1'], "Гражд.право/Трудов.право", teacher_name[10] + '/' + teacher_name[27], "23/210"), ("", lesson_time['2'],
                                                                                                                       "Культра речи юриста", teacher_name[60], "20"), ("", lesson_time['3'], "Уголовное право", teacher_name[70], "21")],
            [("", lesson_time['1'], "Угол.право/Док.обесп.упр.и дел.док.орг", teacher_name[70] + '/' + teacher_name[4], "21/120"), ("", lesson_time['2'], "Док.обесп.упр.и дел.док.орг", teacher_name[4], "20"), ("",
                                                                                                                                                                                                                  lesson_time['3'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[0], "205/114"), ("", lesson_time['4'], "Угол.право/Док.обесп.упр.и дел.док.орг", teacher_name[70] + '/' + teacher_name[4], "21/23")],
            [("", lesson_time['1'], "Семейное право", teacher_name[10], "23"), ("", lesson_time['2'], "Гражд.право/Трудов.право", teacher_name[10] +
                                                                                '/' + teacher_name[27], "24/23"), ("", lesson_time['3'], "Физкультура и здоровье", teacher_name[59] + '/' + "Кульба А. В.", "с/з")],
            [("", lesson_time['1'], "Этика и психология проф.деят.юриста", teacher_name[62], "305"), ("", lesson_time['2'], "Угол.право/Адм.дел.право",
                                                                                                      teacher_name[70] + '/' + teacher_name[34], "21/119"), ("", lesson_time['3'], "Экологическое право", teacher_name[27], "24")],
            [("", lesson_time['1'], "Юридич.служба в организации", "Родина О. Л.", "24"), ("", lesson_time['2'], "Физкультура и здоровье",
                                                                                           teacher_name[59] + '/' + "Кульба А. В.", "с/з"), ("", lesson_time['3s'], "Гражданское право", teacher_name[10], "23")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Трудовое право", teacher_name[27], "24"), ("", lesson_time['2'], "ИГиП Беларуси", teacher_name[
                41], "209"), ("", lesson_time['3'], "Иностранный язык (проф.лекс)", teacher_name[53] + '/' + teacher_name[77], "315/314")],
            [("", lesson_time['1'], "Гражд.право/Трудов.право", teacher_name[10] + '/' + teacher_name[27], "23/210"), ("", lesson_time['2'],
                                                                                                                       "Культра речи юриста", teacher_name[60], "20"), ("", lesson_time['3'], "Уголовное право", teacher_name[70], "21")],
            [("", lesson_time['1'], "Угол.право/Док.обесп.упр.и дел.док.орг", teacher_name[70] + '/' + teacher_name[4], "21/120"), ("", lesson_time['2'], "Информационные технологии", teacher_name[58],
                                                                                                                                    "210"), ("", lesson_time['3'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[0], "205/114"), ("", lesson_time['4'], "Адм.-деликтн. право", teacher_name[34], "24")],
            [("", lesson_time['1'], "Семейное право", teacher_name[10], "23"), ("", lesson_time['2'], "Гражд.право/Трудов.право", teacher_name[10] +
                                                                                '/' + teacher_name[27], "24/23"), ("", lesson_time['3'], "Физкультура и здоровье", teacher_name[59] + '/' + "Кульба А. В.", "с/з")],
            [("", lesson_time['1'], "Этика и психология проф.деят.юриста", teacher_name[62], "305"), ("", lesson_time['2'], "Угол.право/Адм.дел.право",
                                                                                                      teacher_name[70] + '/' + teacher_name[34], "21/119"), ("", lesson_time['3'], "Экологическое право", teacher_name[27], "24")],
            [("", lesson_time['1'], "Юридич.служба в организации", "Родина О. Л.", "24"), ("", lesson_time['2'], "Гражданское право", teacher_name[
                10], "23"), ("", lesson_time['3s'], "Иностранный язык (проф.лекс)", teacher_name[53] + '/' + teacher_name[77], "314/315")]
        ]
    },
    "Ю43": {
        "UP": [
            [("", lesson_time['1'], "Адм.-деликтн. право", teacher_name[34], "21"), ("", lesson_time['2'], "Информационные технологии ",
                                                                                     teacher_name[58] + '/' + teacher_name[18], "205/210"), ("", lesson_time['3'], "Физкультура и здоровье ", teacher_name[68], "с/з")],
            [("", lesson_time['1'], "Культра речи юриста ", teacher_name[60], "20"), ("", lesson_time['2'], "Иностранный язык", teacher_name[53] + '/' + teacher_name[77] + '/' + teacher_name[21],
                                                                                      "312/314/318"), ("", lesson_time['3'], "Трудовое право", teacher_name[27], "24"), ("", lesson_time['4'], "Гражд.право/Трудов.право", teacher_name[10] + '/' + teacher_name[27], "23/315")],
            [("", lesson_time['1'], "Экологическое право ", teacher_name[27], "24"), ("", lesson_time['2'], "Иностранный язык (проф.лекс)", teacher_name[
                53] + '/' + teacher_name[77], "318/314"), ("", lesson_time['3'], "Угол.право/Док.обесп.упр.и дел.док.орг ", teacher_name[70] + '/' + teacher_name[4], "21/23")],
            [("", lesson_time['1'], "Угол.право/Док.обесп.упр.и дел.док.орг ", teacher_name[70] + '/' + teacher_name[4], "21/20"), ("", lesson_time['2'],
                                                                                                                                    "ИгиП Беларуси", teacher_name[41], "207"), ("", lesson_time['3'], "Гражд.право/Трудов.право", teacher_name[10] + '/' + teacher_name[27], "23/210")],
            [("", lesson_time['1'], "Уголовное право", teacher_name[70], "21"), ("", lesson_time['2'], "Гражданское право", teacher_name[10], "23"), ("", lesson_time[
                '3'], "Семейное право ", teacher_name[10], "23"), ("", lesson_time['4'], "Угол.право/Адм.дел.право", teacher_name[70] + '/' + teacher_name[34], "21/23")],
            [("", lesson_time['2'], "Юридич.служба в организации", "Родина О. Л.", "24"), ("", lesson_time[
                '3s'], "Иностранный язык (проф.лекс) ", teacher_name[53] + '/' + teacher_name[77], "314/315")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "ИГиП Беларуси", teacher_name[41], "209"), ("", lesson_time['2'], "Информационные технологии ", teacher_name[
                58] + '/' + teacher_name[18], "205/210"), ("", lesson_time['3'], "Физкультура и здоровье ", teacher_name[68], "с/з")],
            [("", lesson_time['1'], "Культра речи юриста ", teacher_name[60], "20"), ("", lesson_time['2'], "Иностранный язык", teacher_name[53] + '/' + teacher_name[77] + '/' + teacher_name[21],
                                                                                      "312/314/318"), ("", lesson_time['3'], "Трудовое право", teacher_name[27], "24"), ("", lesson_time['4'], "Гражд.право/Трудов.право", teacher_name[10] + '/' + teacher_name[27], "23/315")],
            [("", lesson_time['1'], "Экологическое право ", teacher_name[27], "24"), ("", lesson_time['2'], "Иностранный язык (проф.лекс)", teacher_name[53] + '/' + teacher_name[77], "318/314"), ("",
                                                                                                                                                                                                    lesson_time['3'], "Угол.право/Док.обесп.упр.и дел.док.орг ", teacher_name[70] + '/' + teacher_name[4], "21/23"), ("", lesson_time['4'], "Док.обесп.упр.и дел.док.орг ", teacher_name[4], "23")],
            [("", lesson_time['2'], "Информационные технологии", teacher_name[58], "210"), ("", lesson_time[
                '3'], "Гражд.право/Трудов.право", teacher_name[10] + '/' + teacher_name[27], "23/210")],
            [("", lesson_time['1'], "Уголовное право", teacher_name[70], "21"), ("", lesson_time['2'], "Гражданское право", teacher_name[10], "23"), ("", lesson_time[
                '3'], "Семейное право ", teacher_name[10], "23"), ("", lesson_time['4'], "Угол.право/Адм.дел.право", teacher_name[70] + '/' + teacher_name[34], "21/23")],
            [("", lesson_time['2'], "Юридич.служба в организации", "Родина О. Л.", "24"),
             ("", lesson_time['3s'], "Физкультура и здоровье", teacher_name[68], "с/з")]
        ]
    },
    "С81": {
        "UP": [
            [("", lesson_time['4'], "СТК", teacher_name[54], "102"), ("", lesson_time['5'], "Инженерные сети", teacher_name[
                14], "106"), ("", lesson_time['6'], "ТСП/СТК", teacher_name[42] + '/' + teacher_name[54], "109/200")],
            [("", lesson_time['5'], "ТСП/СТК", teacher_name[42] + '/' + teacher_name[54],
              "109/200"), ("", lesson_time['6'], "ТСП ", teacher_name[42], "202")],
            [("", lesson_time['4'], "Инж.сети/Эконом.строит ", teacher_name[14] + '/' + teacher_name[61], "104/200"), ("",
                                                                                                                       lesson_time['5'], "СТК", teacher_name[54], "102"), ("", lesson_time['6'], "Физкультура и здоровье", teacher_name[68], "с/з")],
            [("", lesson_time['4'], "ОСГН ", teacher_name[63], "121"), ("", lesson_time[
                '5'], "Экономика строительства ", teacher_name[61], "104"), ("", lesson_time['6'], "ТСП ", teacher_name[42], "102")],
            [("", lesson_time['4'], "Инженерные сети ", teacher_name[14], "106"), ("", lesson_time['5'], "Физкультура и здоровье", teacher_name[
                68], "с/з"), ("", lesson_time['6'], "КП ТСП/Инф.технологии в строит ", teacher_name[42] + '/' + teacher_name[67], "109/20")],
            [("", lesson_time['4s'], "КП ТСП/Инф.технологии в строит", teacher_name[42] + '/' + teacher_name[54], "109/210"), ("", lesson_time['5s'],
                                                                                                                               "ТСП/СТК ", teacher_name[42] + '/' + teacher_name[54], "109/200"), ("", lesson_time['6s'], "ТСП", teacher_name[42], "102")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "СТК", teacher_name[54], "102"), ("", lesson_time['5'], "ТСП", teacher_name[
                42], "106"), ("", lesson_time['6'], "ТСП/СТК", teacher_name[42] + '/' + teacher_name[54], "109/200")],
            [("", lesson_time['3'], "ОСГН", teacher_name[63], "121"), ("", lesson_time['4'], "Инженерные сети", teacher_name[14], "106"),  ("", lesson_time[
                '5'], "ТСП/СТК", teacher_name[42] + '/' + teacher_name[54], "109/200"), ("", lesson_time['6'], "ТСП ", teacher_name[42], "202")],
            [("", lesson_time['4'], "Инж.сети/Эконом.строит ", teacher_name[14] + '/' + teacher_name[61], "104/200"), ("",
                                                                                                                       lesson_time['5'], "СТК", teacher_name[54], "102"), ("", lesson_time['6'], "Физкультура и здоровье", teacher_name[68], "с/з")],
            [("", lesson_time['4'], "ОСГН ", teacher_name[63], "121"), ("", lesson_time[
                '5'], "Экономика строительства ", teacher_name[61], "104"), ("", lesson_time['6'], "ТСП ", teacher_name[42], "102")],
            [("", lesson_time['4'], "Инженерные сети ", teacher_name[14], "106"), ("", lesson_time['5'], "Экономика строительства", teacher_name[
                61], "104"), ("", lesson_time['6'], "КП ТСП/Инф.технологии в строит ", teacher_name[42] + '/' + teacher_name[67], "109/20")],
            [("", lesson_time['4s'], "КП ТСП/Инф.технологии в строит", teacher_name[42] + '/' + teacher_name[54], "109/210"), ("", lesson_time['5s'],
                                                                                                                               "ТСП/СТК ", teacher_name[42] + '/' + teacher_name[54], "109/200"), ("", lesson_time['6s'], "ТСП", teacher_name[42], "102")]
        ]
    },
    "С82": {
        "UP": [
            [("", lesson_time['4'], "ТСП", teacher_name[67], "124"), ("", lesson_time['5'], "СТК", teacher_name[
                51], "207"), ("", lesson_time['6'], "Инж.сети/Эконом.строит ", teacher_name[61] + '/' + "Карпяк", "102/104")],
            [("", lesson_time['4'], "ОСГН", teacher_name[63], "121"), ("", lesson_time['5'], "ТСП/СТК",
                                                                       teacher_name[67] + '/' + teacher_name[51], "104/207"), ("", lesson_time['6'], "СТК", teacher_name[51], "207")],
            [("", lesson_time['4'], "Физкультура и здоровье", "Шукис О. В. ", "с/з"), ("", lesson_time['5'], "ОСГН",
                                                                                       teacher_name[63], "121"), ("", lesson_time['6'], "Инж.сети и оборудование", teacher_name[61], "102")],
            [("", lesson_time['4'], "Инж.сети и оборудование", teacher_name[61], "104"), ("", lesson_time['5'], "КП ТСП/Инф.технологии в строит", teacher_name[67] +
                                                                                          '/' + teacher_name[48], "200/209"), ("", lesson_time['6'], "КП ТСП/Инф.технологии в строит ", teacher_name[67] + '/' + teacher_name[48], "200/209")],
            [("", lesson_time['4'], "Инж.сети/Инф.технологии в строит ", teacher_name[61] + '/' + teacher_name[48], "109/209"), ("", lesson_time['5'],
                                                                                                                                 "ТСП/СТК", teacher_name[67] + '/' + teacher_name[19], "102/109"), ("", lesson_time['6'], "Инж.сети и оборудование", teacher_name[61], "104")],
            [("", lesson_time['4s'], "Экономика строительства", "Карпяк Т. А.", "207"), ("", lesson_time['5s'], "ТСП/СТК",
                                                                                         teacher_name[67] + '/' + teacher_name[19], "202/207"), ("", lesson_time['6s'], "ТСП", teacher_name[67], "202")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "ТСП/СТК", teacher_name[67] + '/' + teacher_name[51], "109/207"), ("", lesson_time['5'],
                                                                                                       "СТК", teacher_name[51], "207"), ("", lesson_time['6'], "Экономика строиттельства", "Карпяк Т. А.", "104")],
            [("", lesson_time['4'], "СТК", teacher_name[51], "207"), ("", lesson_time['5'], "ТСП/СТК", teacher_name[67] +
                                                                      '/' + teacher_name[51], "104/207"), ("", lesson_time['6'], "ТСП", teacher_name[67], "104")],
            [("", lesson_time['4'], "Физкультура и здоровье", "Шукис О. В. ", "с/з"), ("", lesson_time['5'], "ОСГН", teacher_name[63],
                                                                                       "121"), ("", lesson_time['6'], "Инж.сети/Эконом.строит", teacher_name[61] + '/' + "Карпяк", "102/106")],
            [("", lesson_time['4'], "Инж.сети и оборудование", teacher_name[61], "104"), ("", lesson_time['5'], "КП ТСП/Инф.технологии в строит", teacher_name[67] +
                                                                                          '/' + teacher_name[48], "200/209"), ("", lesson_time['6'], "КП ТСП/Инф.технологии в строит ", teacher_name[67] + '/' + teacher_name[48], "200/209")],
            [("", lesson_time['3'], "СТК", teacher_name[51], "207"), ("", lesson_time['4'], "ТСП", teacher_name[
                67], "102"), ("", lesson_time['5'], "ТСП/СТК", teacher_name[67] + '/' + teacher_name[19], "102/109")],
            [("", lesson_time['4s'], "Экономика строительства", "Карпяк Т. А.", "207"), ("", lesson_time[
                '5s'], "Физкультура и здоровье", "Шукис О. В.", "с/з"), ("", lesson_time['6s'], "ТСП", teacher_name[67], "202")]
        ]
    },
    "С83": {
        "UP": [
            [("", lesson_time['4'], "Экономика строительства", teacher_name[61], "106"), ("", lesson_time[
                '5'], "Физкультура и здоровье", "Шукис О. В.", "с/з"), ("", lesson_time['6'], "ТСП", teacher_name[14], "106")],
            [("", lesson_time['4'], "Инж.сети и оборудование", teacher_name[14], "106"), ("", lesson_time['5'], "ТСП", teacher_name[
                14], "106"), ("", lesson_time['6'], "КП ТСП/Инф.технологии в строит", teacher_name[14] + '/' + teacher_name[54], "106/200")],
            [("", lesson_time['4'], "СТК", teacher_name[46], "106"), ("", lesson_time['5'], "ТСП/СТК", teacher_name[14] +
                                                                      '/' + teacher_name[46], "104/106"), ("", lesson_time['6'], "ОСГН", teacher_name[63], "121")],
            [("", lesson_time['3'], "СТК", teacher_name[46], "104"), ("", lesson_time['4'], "ТСП", teacher_name[14], "106"), ("", lesson_time[
                '5'], "Инж.сети и оборудование", teacher_name[14], "106"), ("", lesson_time['6'], "Инж.сети/Эконом.строит", teacher_name[14] + '/' + teacher_name[61], "106/104")],
            [("", lesson_time['5'], "СТК", teacher_name[46], "106"), ("", lesson_time[
                '6'], "СТК/ТСП", teacher_name[19] + '/' + teacher_name[14], "200/106")],
            [("", lesson_time['4s'], "СТК/ТСП", teacher_name[19] + '/' + teacher_name[14], "202/104"), ("", lesson_time['5s'], "Физкультура и здоровье",
                                                                                                        teacher_name[59], "с/з"), ("", lesson_time['6s'], "КП ТСП/Инф.технологии в строит", teacher_name[14] + '/' + teacher_name[48], "104/209")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "Экономика строительства", teacher_name[61], "106"), ("", lesson_time[
                '5'], "Физкультура и здоровье", "Шукис О. В.", "с/з"), ("", lesson_time['6'], "ТСП", teacher_name[14], "106")],
            [("", lesson_time['4'], "ОСГН", teacher_name[63], "121"), ("", lesson_time['5'], "ТСП", teacher_name[14], "106"),
             ("", lesson_time['6'], "КП ТСП/Инф.технологии в строит", teacher_name[14] + '/' + teacher_name[54], "106/200")],
            [("", lesson_time['4'], "СТК", teacher_name[46], "106"), ("", lesson_time['5'], "ТСП/СТК",
                                                                      teacher_name[14] + '/' + teacher_name[46], "104"), ("", lesson_time['6'], "ОСГН", teacher_name[63], "121")],
            [("", lesson_time['3'], "СТК", teacher_name[46], "104"), ("", lesson_time['4'], "СТК/ТСП", teacher_name[19] + '/' + teacher_name[14], "109/106"), ("", lesson_time['5'],
                                                                                                                                                               "Инж.сети и оборудование", teacher_name[14], "106"), ("", lesson_time['6'], "Инж.сети/Эконом.строит", teacher_name[14] + '/' + teacher_name[61], "106/104")],
            [("", lesson_time['3'], "Экономика строительства", teacher_name[61], ""), ("", lesson_time['5'], "ТСП", teacher_name[
                14], "106"), ("", lesson_time['6'], "СТК/ТСП", teacher_name[19] + '/' + teacher_name[14], "200/106")],
            [("", lesson_time['3s'], "Инж.сети/Инф.технологии в строит", teacher_name[14] + '/' + teacher_name[48], ""), ("", lesson_time['4s'], "Инж.сети и оборудование", teacher_name[14],
                                                                                                                          "104"), ("", lesson_time['5s'], "ТСП", teacher_name[14], "104"), ("", lesson_time['6s'], "КП ТСП/Инф.технологии в строит", teacher_name[14] + '/' + teacher_name[48], "104/209")]
        ]
    },
    "Ср21": {
        "UP": [
            [("", lesson_time['4'], "Физкультура и здоровье ", "Шукис О. В. ", "с/з"), ("", lesson_time['5'],
                                                                                        "ТСП", teacher_name[50], "102"), ("", lesson_time['6'], "СТК", teacher_name[78], "119")],
            [("", lesson_time['4'], "КП ТСП/Инф.технологии в строит ", teacher_name[50] + '/' + teacher_name[17], "102/314"), ("", lesson_time['5'],
                                                                                                                               "ТСП/СТК", teacher_name[50] + '/' + teacher_name[78], "102/111"), ("", lesson_time['6'], "ТСП", teacher_name[50], "102")],
            [("", lesson_time['4'], "ОСГН", teacher_name[75], "124"), ("", lesson_time['5'], "Эконом.строит /СТК", teacher_name[61] +
                                                                       '/' + teacher_name[78], "200/119"), ("", lesson_time['6'], "Инженерные сети", "Селевоник Ю. С.", "104")],
            [("", lesson_time['4'], "ТСП", teacher_name[50], "102"), ("", lesson_time['5'], "ТСП/СТК", teacher_name[50] +
                                                                      '/' + teacher_name[78], "102/119"), ("", lesson_time['6'], "СТК", teacher_name[78], "119")],
            [("", lesson_time['4'], "Физкультура и здоровье", "Шукис О. В.", "с/з"), ("", lesson_time['5'],
                                                                                      "Экономика строительства", teacher_name[61], "104"), ("", lesson_time['6'], "СТК", teacher_name[78], "119")],
            [("", lesson_time['3s'], "ТСП", teacher_name[50], "102"), ("", lesson_time['4s'], "КП ТСП/Инф.технологии в строит ", teacher_name[50] + '/' + teacher_name[48], "102/209"),
             ("", lesson_time['5s'], "ТСП/ Инж.сети ", teacher_name[50] + '/' + "Селевоник", "102/106"), ("", lesson_time['6s'], "Инженерные сети", "Селевоник Ю. С.", "106")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "Физкультура и здоровье ", "Шукис О. В. ", "с/з"), ("", lesson_time['5'], "ТСП",
                                                                                        teacher_name[50], "102"), ("", lesson_time['6'], "Экономика строиттельства", teacher_name[61], "102")],
            [("", lesson_time['4'], "КП ТСП/Инф.технологии в строит ", teacher_name[50] + '/' + teacher_name[17], "102/314"), ("", lesson_time['5'],
                                                                                                                               "ТСП/СТК", teacher_name[50] + '/' + teacher_name[78], "102/111"), ("", lesson_time['6'], "ТСП", teacher_name[50], "102")],
            [("", lesson_time['4'], "ОСГН", teacher_name[75], "124"), ("", lesson_time['5'], "Эконом.строит /СТК", teacher_name[61] +
                                                                       '/' + teacher_name[78], "200/119"), ("", lesson_time['6'], "Инженерные сети", "Селевоник Ю. С.", "104")],
            [("", lesson_time['4'], "ТСП", teacher_name[50], "102"), ("", lesson_time['5'], "ТСП/СТК", teacher_name[50] +
                                                                      '/' + teacher_name[78], "102/119"), ("", lesson_time['6'], "СТК", teacher_name[78], "119")],
            [("", lesson_time['3'], "ОСГН", teacher_name[75], ""), ("", lesson_time['4'], "Инф.технологии в строит", teacher_name[17] + '/' + teacher_name[48],
                                                                    "209/311"), ("", lesson_time['5'], "СТК", teacher_name[78], "119"), ("", lesson_time['6'], "Экономика строительства", teacher_name[61], "104")],
            [("", lesson_time['4s'], "КП ТСП/Инф.технологии в строит ", teacher_name[50] + '/' + teacher_name[48], "102/209"), ("", lesson_time['5s'],
                                                                                                                                "ТСП/ Инж.сети ", teacher_name[50] + '/' + "Селевоник", "102/106"), ("", lesson_time['6s'], "Инженерные сети", "Селевоник Ю. С.", "106")]
        ]
    },
    "Р49": {
        "UP": [
            [("", lesson_time['4'], "ТАП РЭС", teacher_name[11], "305"), ("", lesson_time['5'], "КРЭС", teacher_name[
                3], "302"), ("", lesson_time['6'], "Физкультура и здоровье", "Шукис О. В.", "с/з")],
            [("", lesson_time['3'], "Экономика организации ", teacher_name[4], "24"), ("", lesson_time['4'], "Микропроцессорная техника ", teacher_name[
                18], "210"), ("", lesson_time['5'], "Микропроцессорная техника/ТАП РЭС", teacher_name[18] + '/' + teacher_name[11], "210/305")],
            [("", lesson_time['4'], "РЭУ", teacher_name[33], "302"), ("", lesson_time[
                '5'], "Микропроцессорная техника", teacher_name[18], "210")],
            [("", lesson_time['3'], "Экономика организации", teacher_name[4], "111"), ("", lesson_time['4'], "КП РЭУ/КРЭС", teacher_name[33] + '/' + teacher_name[3],
                                                                                       "311а/302"), ("", lesson_time['5'], "КП РЭУ/КРЭС", teacher_name[33] + '/' + teacher_name[3], "311а/302"), ("", lesson_time['6'], "РЭУ", teacher_name[33], "307")],
            [("", lesson_time['3'], "Экономика организации", teacher_name[4], "24"), ("", lesson_time[
                '4'], "ТАП РЭС", teacher_name[11], "305"), ("", lesson_time['5'], "РЭУ", teacher_name[33], "302")],
            [("", lesson_time['4s'], "РЭУ", teacher_name[33], "307"), ("", lesson_time['5s'], "КРЭС",
                                                                       teacher_name[3], "302"), ("", lesson_time['6s'], "ТАП РЭС ", teacher_name[11], "305")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "ТАП РЭС", teacher_name[11], "305"), ("", lesson_time['5'], "КРЭС", teacher_name[
                3], "302"), ("", lesson_time['6'], "Физкультура и здоровье", "Шукис О. В.", "с/з")],
            [("", lesson_time['3'], "Экономика организации ", teacher_name[4], "24"), ("", lesson_time['4'], "Микропроцессорная техника ", teacher_name[
                18], "210"), ("", lesson_time['5'], "Микропроцессорная техника/ТАП РЭС", teacher_name[18] + '/' + teacher_name[11], "210/305")],
            [("", lesson_time['4'], "РЭУ", teacher_name[33], "302"), ("", lesson_time['5'], "Микропроцессорная техника", teacher_name[
                18], "210"), ("", lesson_time['6'], "Микропроцессорная техника/ТАП РЭС", teacher_name[18] + '/' + teacher_name[11], "210/305")],
            [("", lesson_time['3'], "Экономика организации", teacher_name[4], "111"), ("", lesson_time['4'], "КП РЭУ/КРЭС", teacher_name[33] + '/' + teacher_name[3],
                                                                                       "311а/302"), ("", lesson_time['5'], "КП РЭУ/КРЭС", teacher_name[33] + '/' + teacher_name[3], "311а/302"), ("", lesson_time['6'], "РЭУ", teacher_name[33], "307")],
            [("", lesson_time['3'], "Экономика организации", teacher_name[4], "24"), ("", lesson_time[
                '4'], "Физкультура и здоровье", "Шукис О. В.", "с/з"), ("", lesson_time['5'], "РЭУ", teacher_name[33], "302")],
            [("", lesson_time['4s'], "РЭУ", teacher_name[33], "307"), ("", lesson_time['5s'], "КРЭС",
                                                                       teacher_name[3], "302"), ("", lesson_time['6s'], "ТАП РЭС ", teacher_name[11], "305")]
        ]
    },
    "Р50": {
        "UP": [
            [("", lesson_time['3'], "РЭУ", teacher_name[11], "311а"), ("", lesson_time['4'], "Микропроцессорная техника", teacher_name[18], "210"), ("", lesson_time[
                '5'], "Микропроцессорная техника/ТАП РЭС", teacher_name[18] + '/' + teacher_name[11], "210/305"), ("", lesson_time['6'], "КРЭС", teacher_name[3], "302")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[4], "305"), ("", lesson_time[
                '5'], "Физкультура и здоровье", teacher_name[59], "с/з"), ("", lesson_time['6'], "РЭУ", teacher_name[11], "305")],
            [("", lesson_time['4'], "Микропроцессорная техника", teacher_name[18], "210"), ("", lesson_time['5'], "ТАП РЭС", teacher_name[
                11], "305"), ("", lesson_time['6'], "Микропроцессорная техника/ТАП РЭС", teacher_name[18] + '/' + teacher_name[11], "")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[4], "21"), ("", lesson_time['5'], "РЭУ", teacher_name[
                11], "305"), ("", lesson_time['6'], "КП РЭУ/КРЭС", teacher_name[11] + '/' + teacher_name[3], "305/302")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[4], "24"), ("", lesson_time[
                '5'], "Физкультура и здоровье", teacher_name[59], "с/з"), ("", lesson_time['6'], "РЭУ", teacher_name[11], "305")],
            [("", lesson_time['4s'], "КП РЭУ/КРЭС", teacher_name[11] + '/' + teacher_name[3], "311а/302"), ("",
                                                                                                            lesson_time['5s'], "ТАП РЭС", teacher_name[11], "305"), ("", lesson_time['6s'], "КРЭС", teacher_name[3], "302")]
        ],
        "DOWN": [
            [("", lesson_time['3'], "РЭУ", teacher_name[11], "311а"), ("", lesson_time['4'], "Микропроцессорная техника", teacher_name[18], "210"), ("", lesson_time[
                '5'], "Микропроцессорная техника/ТАП РЭС", teacher_name[18] + '/' + teacher_name[11], "210/305"), ("", lesson_time['6'], "КРЭС", teacher_name[3], "302")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[4], "305"), ("", lesson_time[
                '5'], "Физкультура и здоровье", teacher_name[59], "с/з"), ("", lesson_time['6'], "РЭУ", teacher_name[11], "305")],
            [("", lesson_time['4'], "Микропроцессорная техника", teacher_name[
              18], "210"), ("", lesson_time['5'], "ТАП РЭС", teacher_name[11], "305")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[4], "21"), ("", lesson_time['5'], "РЭУ", teacher_name[
                11], "305"), ("", lesson_time['6'], "КП РЭУ/КРЭС", teacher_name[11] + '/' + teacher_name[3], "305/302")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[4], "24"), ("", lesson_time[
                '5'], "ТАП РЭС", teacher_name[11], "305"), ("", lesson_time['6'], "РЭУ", teacher_name[11], "305")],
            [("", lesson_time['4s'], "КП РЭУ/КРЭС", teacher_name[11] + '/' + teacher_name[3], "311а/302"), ("",
                                                                                                            lesson_time['5s'], "ТАП РЭС", teacher_name[11], "305"), ("", lesson_time['6s'], "КРЭС", teacher_name[3], "302")]
        ]
    },
    "М50": {
        "UP": [
            [("", lesson_time['4'], "Основы автоматики ", teacher_name[49], "310"), ("", lesson_time[
                '5'], "Экономика организации ", teacher_name[32], "111"), ("", lesson_time['6'], "Охрана труда", teacher_name[79], "111")],
            [("", lesson_time['4'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[0], "114/205"), ("",
                                                                                                                        lesson_time['5'], "ТОиН", teacher_name[47], "310"), ("", lesson_time['6'], "Охрана труда", teacher_name[79], "111")],
            [("", lesson_time['4'], "КиРС/Станд.и кач.прод", teacher_name[1] + '/' + "Кульбачинская", "120/20"), ("", lesson_time['5'], "Информационные технологии ",
                                                                                                                  teacher_name[58] + '/' + teacher_name[0], "205/114"), ("", lesson_time['6'], "Физкультура и здоровье", teacher_name[66], "с/з")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[32], "111"), ("", lesson_time['5'], "Станд.и кач.продукции ",
                                                                                        "Кульбачинская Л. А.", "20"), ("", lesson_time['6'], "Осн.прогр.для ст.с ЧПУ ", teacher_name[49], "312")],
            [("", lesson_time['4'], "ТОиН", teacher_name[47], "310"), ("", lesson_time['5'], "Информационные технологии ",
                                                                       teacher_name[58] + '/' + teacher_name[0], "205/114"), ("", lesson_time['6'], "КиРС", teacher_name[1], "120")],
            [("", lesson_time['4s'], "ТОиН", teacher_name[47], "310"), ("", lesson_time['5s'], "КП КиРС", teacher_name[1] + '/' + teacher_name[20],
                                                                        "120/111"), ("", lesson_time['6s'], "Осн.прогр.для ст.с ЧПУ/ТОиН ", teacher_name[49] + '/' + teacher_name[47], "315/310")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "Основы автоматики ", teacher_name[49], "310"), ("", lesson_time[
                '5'], "Экономика организации ", teacher_name[32], "111"), ("", lesson_time['6'], "Охрана труда", teacher_name[79], "111")],
            [("", lesson_time['4'], "Осн.автоматики/Станд.и кач.прод ", teacher_name[49] + '/' + "Кульбачинская", "315/20"), ("",
                                                                                                                              lesson_time['5'], "Осн.автоматики", teacher_name[49], "312"), ("", lesson_time['6'], "Охрана труда", teacher_name[79], "111")],
            [("", lesson_time['4'], "Осн.прогр.для ст.с ЧПУ", teacher_name[49], "310"), ("", lesson_time['5'], "Информационные технологии ",
                                                                                         teacher_name[58] + '/' + teacher_name[0], "205/114"), ("", lesson_time['6'], "Физкультура и здоровье", teacher_name[66], "с/з")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[32], "111"), ("", lesson_time['5'], "Станд.и кач.продукции ",
                                                                                        "Кульбачинская Л. А.", "20"), ("", lesson_time['6'], "Осн.прогр.для ст.с ЧПУ ", teacher_name[49], "312")],
            [("", lesson_time['4'], "ТОиН", teacher_name[47], "310"), ("", lesson_time['5'], "Информационные технологии ", teacher_name[
                58] + '/' + teacher_name[0], "205/114"), ("", lesson_time['6'], "Физкультура и здоровье", teacher_name[66], "с/з")],
            [("", lesson_time['4s'], "ТОиН", teacher_name[47], "310"), ("", lesson_time['5s'], "КП КиРС", teacher_name[1] + '/' + teacher_name[20],
                                                                        "120/111"), ("", lesson_time['6s'], "Осн.прогр.для ст.с ЧПУ/ТОиН ", teacher_name[49] + '/' + teacher_name[47], "315/310")]
        ]
    },
    "М51": {
        "UP": [
            [("", lesson_time['4'], "ТОиН", teacher_name[1], "120"), ("", lesson_time['5'], "Осн.прогр.для ст.с ЧПУ/ТОиН",
                                                                      teacher_name[49] + '/' + teacher_name[1], "315/120"), ("", lesson_time['6'], "Осн.прогр.для ст.с ЧПУ", teacher_name[49], "310")],
            [("", lesson_time['4'], "Экономика организации", teacher_name[32], "120"), ("", lesson_time['5'], "Станд.и кач.продукции",
                                                                                        "Кульбачинская Л. А.", "20"), ("", lesson_time['6'], "Осн.автоматики/Станд.и кач.прод", teacher_name[49] + '/' + "Кульбачинская", "20")],
            [("", lesson_time['4'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[83], "205/114"), ("",
                                                                                                                         lesson_time['5'], "Физкультура и здоровье ", teacher_name[68], "с/з"), ("", lesson_time['6'], "ТОиН", teacher_name[1], "120")],
            [("", lesson_time['4'], "Основы автоматики", teacher_name[49], "312"), ("", lesson_time['5'], "Экономика организации",
                                                                                    teacher_name[32], "111"), ("", lesson_time['6'], "КП КиРС", teacher_name[47] + '/' + teacher_name[20], "310/111")],
            [("", lesson_time['4'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[83], "205/114"), ("",
                                                                                                                         lesson_time['5'], "ТОиН ", teacher_name[1], "120"), ("", lesson_time['6'], "Осн.прогр.для ст.с ЧПУ", teacher_name[49], "312")],
            [("", lesson_time['4s'], "Осн.прогр.для ст.с ЧПУ", teacher_name[49], "312"), ("", lesson_time[
                '5s'], "Осн.автоматики", teacher_name[49], "312"), ("", lesson_time['6s'], "Охрана труда", teacher_name[1], "120")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "Экономика организации", teacher_name[32], "111"), ("", lesson_time['5'], "Осн.прогр.для ст.с ЧПУ/ТОиН",
                                                                                        teacher_name[49] + '/' + teacher_name[1], "315/120"), ("", lesson_time['6'], "Охрана труда", teacher_name[1], "120")],
            [("", lesson_time['4'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[83], "114/205"), ("", lesson_time['5'], "КиРС/Станд.и кач.прод ",
                                                                                                                         teacher_name[42] + '/' + "Кульбачинская", "310/20"), ("", lesson_time['6'], "Станд.и кач.продукции", "Кульбачинская Л. А.", "20")],
            [("", lesson_time['4'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[83], "205/114"), ("",
                                                                                                                         lesson_time['5'], "Физкультура и здоровье ", teacher_name[68], "с/з"), ("", lesson_time['6'], "ТОиН", teacher_name[1], "120")],
            [("", lesson_time['4'], "Основы автоматики", teacher_name[49], "312"), ("", lesson_time['5'], "Экономика организации",
                                                                                    teacher_name[32], "111"), ("", lesson_time['6'], "КП КиРС", teacher_name[47] + '/' + teacher_name[20], "310/111")],
            [("", lesson_time['4'], "Информационные технологии", teacher_name[58] + '/' + teacher_name[83], "205/114"), ("",
                                                                                                                         lesson_time['5'], "ТОиН ", teacher_name[1], "120"), ("", lesson_time['6'], "Охрана труда", teacher_name[1], "120")],
            [("", lesson_time['4s'], "Физкультура и здоровье", teacher_name[68], "с/з"), ("", lesson_time['5s'],
                                                                                          "КиРС", teacher_name[47], "310"), ("", lesson_time['6s'], "Охрана труда", teacher_name[1], "120")]
        ]
    },
    "Мс52": {
        "UP": [
            [("", lesson_time['4'], "Технология машиностроения", teacher_name[37], "312"),
             ("", lesson_time['5'], "Экономика организации", teacher_name[43], "200")],
            [("", lesson_time['4'], "КП КиРС", teacher_name[42] + '/' + teacher_name[69], "310/111"), ("", lesson_time['5'],
                                                                                                       "Физкультура и здоровье", teacher_name[68], "с/з"), ("", lesson_time['6'], "ТОиН", teacher_name[47], "310")],
            [("", lesson_time['4'], "Технология машиностроения", teacher_name[37], "312"), ("", lesson_time['5'], "Технол.машиностр/КиРС",
                                                                                            teacher_name[37] + '/' + teacher_name[69], "312/111"), ("", lesson_time['6'], "Охрана труда", teacher_name[20], "111")],
            [("", lesson_time['4'], "ТОиН", teacher_name[47], "310"), ("", lesson_time['5'], "Осн.прогр.для ст.с ЧПУ/ТОиН",
                                                                       teacher_name[49] + '/' + teacher_name[47], "315/310"), ("", lesson_time['6'], "Экономика организации", teacher_name[43], "200")],
            [("", lesson_time['4'], "Осн.прогр.для ст.с ЧПУ", teacher_name[49], "312"), ("", lesson_time['5'], "Основы автоматики",
                                                                                         teacher_name[49], "312"), ("", lesson_time['6'], "Физкультура и здоровье", teacher_name[68], "с/з")],
            [("", lesson_time['4s'], "КиРС", teacher_name[69], "111"), ("", lesson_time['5s'], "ТОиН",
                                                                        teacher_name[47], "310"), ("", lesson_time['6s'], "Охрана труда", teacher_name[20], "111")]
        ],
        "DOWN": [
            [("", lesson_time['4'], "Технология машиностроения", teacher_name[37], "312"), ("", lesson_time[
                '5'], "Экономика организации", teacher_name[43], "200"), ("", lesson_time['6'], "Осн.прогр.для ст.с ЧПУ", teacher_name[49], "310")],
            [("", lesson_time['4'], "КП КиРС", teacher_name[43] + '/' + teacher_name[69], "310/111"), ("", lesson_time['5'],
                                                                                                       "Физкультура и здоровье", teacher_name[68], "с/з"), ("", lesson_time['6'], "ТОиН", teacher_name[47], "310")],
            [("", lesson_time['4'], "Технология машиностроения", teacher_name[37], "312"), ("", lesson_time[
                '5'], "КиРС", teacher_name[69], "111"), ("", lesson_time['6'], "Охрана труда", teacher_name[20], "111")],
            [("", lesson_time['4'], "ТОиН", teacher_name[47], "310"), ("", lesson_time['5'], "Осн.прогр.для ст.с ЧПУ/ТОиН",
                                                                       teacher_name[49] + '/' + teacher_name[47], "315/310"), ("", lesson_time['6'], "Экономика организации", teacher_name[43], "200")],
            [("", lesson_time['4'], "КиРС", teacher_name[69], "111"), ("", lesson_time['5'], "Основы автоматики",
                                                                       teacher_name[49], "312"), ("", lesson_time['6'], "Осн.прогр.для ст.с ЧПУ", teacher_name[49], "312")],
            [("", lesson_time['4s'], "Осн.автоматики/КиРС", teacher_name[49] + '/' + teacher_name[69], "315/111"), ("", lesson_time['5s'],
                                                                                                                    "Осн.автоматики", teacher_name[49], "312"), ("", lesson_time['6s'], "Охрана труда", teacher_name[20], "111")]
        ]
    },
    "Ю41": {
        "UP": [
            [("", lesson_time['1'], "Охрана окр.среды", teacher_name[62], "209"), ("", lesson_time['2'], "Жилищное право",
                                                                                   teacher_name[10], "23"), ("", lesson_time['3'], "Гражданский процесс", teacher_name[34], "21")],
            [("", lesson_time['1'], "Оформл.кадров.документации ", "Родина О. Л.", "24"), ("", lesson_time[
                '2'], "Уголовный процесс ", teacher_name[70], "21"), ("", lesson_time['3'], "Гражданский процесс", teacher_name[34], "124")],
            [("", lesson_time['2'], "Порядок оф.док.для нач.пенсии ", teacher_name[34], "24"), ("", lesson_time[
                '3'], "Гражданский процесс", teacher_name[34], "24"), ("", lesson_time['4'], "Физкультура и здоровье", teacher_name[59], "с/з")],
            [("", lesson_time['2'], "Уголовный процесс ", teacher_name[70], "21"), ("", lesson_time['3'], "Налоговое право ",
                                                                                    teacher_name[34], "24"), ("", lesson_time['4'], "Гражданский процесс", teacher_name[34], "24")],
            [("", lesson_time['1'], "Таможенное право", teacher_name[27], "24"), ("", lesson_time['2'], "Охрана окр.среды",
                                                                                  teacher_name[62], "305"), ("", lesson_time['3'], "Уголовный процесс ", teacher_name[70], "21")],
            [("", lesson_time['1'], "Хозяйственный процесс", "Куровский Д. Г.", "23"), ("", lesson_time['2'], "Охрана труда ", teacher_name[79], "20"), ("", lesson_time[
                '3s'], "Физкультура и здоровье", teacher_name[59], "с/з"), ("", lesson_time['4s'], "Оформл.кадров.документации", "Родина О. Л.", "24")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Градж.процесс", teacher_name[34], "21"), ("", lesson_time['2'], "Жилищное право", teacher_name[10], "23"),
             ("", lesson_time['3'], "Гражданский процесс", teacher_name[34], "21"), ("", lesson_time['4'], "Градж.процесс", teacher_name[34], "21")],
            [("", lesson_time['1'], "Оформл.кадров.документации ", "Родина О. Л.", "24"), ("", lesson_time[
                '2'], "Уголовный процесс ", teacher_name[70], "21"), ("", lesson_time['3'], "Гражданский процесс", teacher_name[34], "124")],
            [("", lesson_time['2'], "Порядок оф.док.для нач.пенсии ", teacher_name[34], "24"), ("", lesson_time[
                '3'], "Гражданский процесс", teacher_name[34], "24"), ("", lesson_time['4'], "Физкультура и здоровье", teacher_name[59], "с/з")],
            [("", lesson_time['2'], "Уголовный процесс ", teacher_name[70], "21"), ("", lesson_time['3'], "Налоговое право ",
                                                                                    teacher_name[34], "24"), ("", lesson_time['4'], "Гражданский процесс", teacher_name[34], "24")],
            [("", lesson_time['1'], "Таможенное право", teacher_name[27], "24"), ("", lesson_time['2'], "Охрана окр.среды",
                                                                                  teacher_name[62], "305"), ("", lesson_time['3'], "Уголовный процесс ", teacher_name[70], "21")],
            [("", lesson_time['1'], "Хозяйственный процесс", "Куровский Д. Г.", "23"), ("", lesson_time['2'], "Охрана труда ", teacher_name[79], "20"), ("",
                                                                                                                                                         lesson_time['3s'], "Хозяйственный процесс", "Куровский Д. Г.", "23"), ("", lesson_time['4s'], "Оформл.кадров.документации", "Родина О. Л.", "24")]
        ]
    },
    "Юс42": {
        "UP": [
            [("", lesson_time['1'], "Жилищное право", teacher_name[10], "23"), ("", lesson_time['2'], "Гражданский процесс", teacher_name[34], "21"),
             ("", lesson_time['3'], "Физкультура и здоровье", "Кульба А. В.", "с/з"), ("", lesson_time['4'], "Градж.процесс", teacher_name[34], "21")],
            [("", lesson_time['1'], "Уголовный процесс", teacher_name[62], "21"), ("", lesson_time['2'], "Оформл.кадров.документации", teacher_name[70], "24"),
             ("", lesson_time['3'], "Охрана окр. среды", teacher_name[62], "209"), ("", lesson_time['4'], "Гражданский процесс", teacher_name[34], "21")],
            [("", lesson_time['1'], "Гражданский процесс", teacher_name[34], "24"),
             ("", lesson_time['2'], "Уголовный процесс", teacher_name[70], "21")],
            [("", lesson_time['1'], "Гражданский процесс", teacher_name[34], "24"), ("", lesson_time[
                '2'], "Налоговое право", teacher_name[34], "24"), ("", lesson_time['3'], "Уголовный процесс", teacher_name[70], "21")],
            [("", lesson_time['1'], "Физкультура и здоровье", "Кульба А. В.", "с/з"), ("", lesson_time['2'], "Таможенное право",
                                                                                       teacher_name[27], "24"), ("", lesson_time['3'], "Порядок оф.док.для нач.пенсии", teacher_name[34], "120")],
            [("", lesson_time['1'], "Охрана труда", teacher_name[79], "20"), ("", lesson_time['2'], "Хозяйственный процесс",
                                                                              "Куровский Д. Г.", "23"), ("", lesson_time['3s'], "Оформл.кадров.документации", "Родина О. Л.", "24")]
        ],
        "DOWN": [
            [("", lesson_time['1'], "Жилищное право", teacher_name[10], "23"), ("", lesson_time['2'], "Гражданский процесс",
                                                                                teacher_name[34], "21"), ("", lesson_time['3'], "Физкультура и здоровье", "Кульба А. В.", "с/з")],
            [("", lesson_time['1'], "Уголовный процесс", teacher_name[62], "21"), ("", lesson_time['2'], "Оформл.кадров.документации", teacher_name[70], "24"),
             ("", lesson_time['3'], "Охрана окр. среды", teacher_name[62], "209"), ("", lesson_time['4'], "Гражданский процесс", teacher_name[34], "21")],
            [("", lesson_time['1'], "Гражданский процесс", teacher_name[34], "24"), ("", lesson_time[
                '2'], "Уголовный процесс", teacher_name[70], "21"), ("", lesson_time['3'], "Охрана окр.среды", teacher_name[62], "212")],
            [("", lesson_time['1'], "Гражданский процесс", teacher_name[34], "24"), ("", lesson_time[
                '2'], "Налоговое право", teacher_name[34], "24"), ("", lesson_time['3'], "Уголовный процесс", teacher_name[70], "21")],
            [("", lesson_time['1'], "Градж.процесс", teacher_name[34], "23"), ("", lesson_time['2'], "Таможенное право",
                                                                               teacher_name[27], "24"), ("", lesson_time['3'], "Порядок оф.док.для нач.пенсии", teacher_name[34], "120")],
            [("", lesson_time['1'], "Охрана труда", teacher_name[79], "20"), ("", lesson_time['2'], "Хозяйственный процесс", "Куровский Д. Г.", "23"), ("", lesson_time[
                '3s'], "Оформл.кадров.документации", "Родина О. Л.", "24"), ("", lesson_time['4s'], "Хозяйственный процесс", "Куровский Д. Г.", "23")]
        ]
    }
}


teachers_shedule = {}
existing_teachers = []

for teacher in teacher_name:
    teachers_shedule[teacher] = {'UP': [[], [], [], [], [], []],
                                 'DOWN': [[], [], [], [], [], []]}

for group in shedule:
    for week in shedule[group]:
        for day in shedule[group][week]:
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
                                teachers_shedule[teacher][week] \
                                                [shedule[group][week]
                                                 .index(day)] \
                                    .append(day_shedule)

                    if (name_of_teacher.strip() not in existing_teachers and
                            '/' not in name_of_teacher):
                        existing_teachers.append(name_of_teacher.strip())

                    if (teacher == name_of_teacher and
                            '/' not in name_of_teacher):
                        teachers_shedule[teacher][week] \
                                        [shedule[group][week]
                                         .index(day)] \
                            .append(day_shedule)

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
