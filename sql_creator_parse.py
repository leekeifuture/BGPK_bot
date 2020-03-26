# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


import datetime as dt
from sqlite3 import connect


if dt.datetime.isoweekday(dt.datetime.now()) != 7:
    isoweekday = dt.datetime.isoweekday(dt.datetime.now())
else:
    isoweekday = dt.datetime.isoweekday(
        dt.datetime.now() + dt.timedelta(days=-1))


def create_sql(db_name):
    sql_con = connect(db_name)
    cursor = sql_con.cursor()

    cursor.execute('''CREATE TABLE parsing_days
                        (
                            pro_parsing_day TEXT DEFAULT {},
                            pro_parsing_date INT DEFAULT {}
                        )'''.format(isoweekday, 0))
    sql_con.commit()

    cursor.execute('''CREATE TABLE zam_from_site
                        (
                            day_1 TEXT,
                            day_2 TEXT,
                            day_3 TEXT,
                            day_4 TEXT,
                            day_5 TEXT,
                            day_6 TEXT
                        )''')
    sql_con.commit()

    cursor.execute('''INSERT INTO parsing_days (pro_parsing_day, pro_parsing_date)
                            VALUES (?, ?)''', (isoweekday, 0,))
    sql_con.commit()

    cursor.execute('''INSERT INTO zam_from_site (day_1, day_2, day_3, day_4, day_5, day_6)
                            VALUES (NULL, NULL, NULL, NULL, NULL, NULL)''')
    sql_con.commit()

    cursor.close()
    sql_con.close()


if __name__ == '__main__':
    create_sql('Parse.db')
