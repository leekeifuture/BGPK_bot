# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


from constants import path
from sqlite3 import connect


def main():
    sql_con = connect(path + 'Bot.db')
    cursor = sql_con.cursor()
    cursor.execute('''DELETE FROM user_choice
                            WHERE step = "select_teacher"''')
    sql_con.commit()
    cursor.close()
    sql_con.close()


if __name__ == '__main__':
    main()
