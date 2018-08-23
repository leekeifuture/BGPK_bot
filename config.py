# -*- coding: utf-8 -*-
#!/usr/bin/python3.6


my_id = ''  # my id

token = ''  # bot token

WEBHOOK_HOST = ''  # IP adress
WEBHOOK_PORT = 443  # 443, 80, 88, 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = ''  # path to certificate
WEBHOOK_SSL_PRIV = ''  # path to private key

WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % token
