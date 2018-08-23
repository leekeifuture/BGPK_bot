# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


from functions import sql_execute


def main():
    sql_execute('Bot_db', 'DELETE FROM user_choice')


if __name__ == '__main__':
    main()
