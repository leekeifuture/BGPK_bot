# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


from os import environ


my_id = environ['my_telegram_id']  # my id

token = environ['bot_token']  # bot token

WEBHOOK_HOST = environ['server_ip']  # IP adress
WEBHOOK_PORT = 443  # 443, 80, 88, 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # path to certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # path to private key

WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % token
