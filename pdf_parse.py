# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import os
import sys
import config
import telebot
import hashlib
from urllib import request
from datetime import datetime


bot = telebot.TeleBot(config.token)

raspisanie = 'http://www.bspc.brest.by/files/raspisanie/'
currently_pdf_dir = '/home/ubuntu/bot/PDF/'
currently_pdf_from_site = '/home/ubuntu/bot/PDF/site_pdf/'

pdfs = [
    's_1k.pdf', 'r_1k.pdf', 'm_1k.pdf', 'u_1k.pdf', 's_2k.pdf', 'r_2k.pdf',
    'm_2k.pdf', 'u_2k.pdf', 's_3k.pdf', 'r_3k.pdf', 'm_3k.pdf', 'u_3k.pdf',
    's_4k.pdf', 'r_4k.pdf', 'm_4k.pdf'
]  # u_4k.pdf

tree = os.walk(currently_pdf_dir)
tree_site_dir = os.walk(currently_pdf_from_site)


for name_of_pdf_file in pdfs:
    my_file = raspisanie + name_of_pdf_file
    my_dir = currently_pdf_from_site + my_file[42:]
    try:
        request.urlretrieve(my_file, my_dir)
    except:
        print('\n\n' + str(datetime.now())
              [:-7] + ' | ' + str(sys.exc_info()[1]) + '\n\n')
        bot.send_message(config.my_id, str(datetime.now())[
                         :-7] + ' | PDF (' + name_of_pdf_file[:4] + ') | ' + str(sys.exc_info()[1]))
        continue

tree_hash = []
for files_names in tree:
    for fn in files_names[2]:
        with open(currently_pdf_dir + fn, 'rb') as file:
            file_name = file.read()
            file.close()
        h = hashlib.md5(file_name).hexdigest()
        tree_hash.append(h)

ind = -1

for files_names in tree_site_dir:
    for fn in files_names[2]:
        ind += 1
        with open(currently_pdf_from_site + fn, 'rb') as file:
            file_name = file.read()
            file.close()
        h = hashlib.md5(file_name).hexdigest()
        if h not in tree_hash:
            bot.send_message(config.my_id, str(datetime.now())[
                             :-7] + ' | ' + fn[:4] + ' | ' + tree_hash[ind] + ' >> ' + h)
