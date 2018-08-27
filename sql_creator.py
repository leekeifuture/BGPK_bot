# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


from sqlite3 import connect


def create_sql(db_name):
    sql_con = connect(db_name)
    cursor = sql_con.cursor()

    # user choice
    cursor.execute('''CREATE TABLE user_choice
                        (
                            user_id INT PRIMARY KEY,
                            alias TEXT,
                            div_alias TEXT,
                            division_name TEXT,
                            admission_year_name TEXT,
                            student_group_name TEXT,
                            types_json TEXT,
                            divisions_json TEXT,
                            study_programs_json TEXT,
                            student_groups_json TEXT,
                            step TEXT DEFAULT 'handle_start' NOT NULL
                        )''')
    sql_con.commit()

    # user data
    cursor.execute('''CREATE TABLE user_data
                        (
                            id INT PRIMARY KEY NOT NULL,
                            first_name TEXT,
                            last_name TEXT,
                            username TEXT,
                            alias TEXT,
                            group_name TEXT,
                            date_of_registrations TEXT,
                            sending_rasp INT DEFAULT 0 NOT NULL,
                            sending_zam INT DEFAULT 1 NOT NULL,
                            step TEXT DEFAULT 'main_menu' NOT NULL,
                            rate INT DEFAULT 0 NOT NULL,
                            sending_rasp_5 INT DEFAULT 0 NOT NULL
                        )''')
    sql_con.commit()

    # banned users
    cursor.execute('''CREATE TABLE banned_users
                        (
                            id_banned INT,
                            id_not_banned INT,
                            prichina TEXT
                        )''')
    sql_con.commit()

    # offer
    cursor.execute('''CREATE TABLE offer
                        (
                            week INT DEFAULT 1 NOT NULL,
                            sending_log INT DEFAULT 1 NOT NULL,
                            on_or_off_zam INT DEFAULT 1 NOT NULL,
                            abridged_calls TEXT
                        )''')
    sql_con.commit()

    # all users
    cursor.execute('''CREATE TABLE all_users
                        (
                            id INT PRIMARY KEY NOT NULL
                        )''')
    sql_con.commit()

    cursor.execute('''INSERT INTO offer (week, sending_log, on_or_off_zam)
                           VALUES (?, ?, ?)''', (0, 0, 0,))
    sql_con.commit()
    cursor.close()
    sql_con.close()


if __name__ == '__main__':
    create_sql('Bot.db')
