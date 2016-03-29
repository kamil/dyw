#! /usr/bin/env python
# encoding: utf-8

import sys,os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dyw.settings'
sys.path.append('/Users/kamil/Projects/')

from dyw.apps.system.models import FromMail

HOST = 'mail.wservices.ch'
USER = 'robot@doyrwork.com'
PASS = ''

import imaplib,email
from email.header import decode_header

conn = imaplib.IMAP4(HOST)
print conn.login(USER,PASS)
print conn.select()

messages_ids = conn.search(None,'UNSEEN')[1][0].split(' ')

print 'Wiadomosci id (%r)' % messages_ids

for msg in [email.message_from_string(conn.fetch(f_id,'(RFC822)')[1][0][1]) for f_id in messages_ids]:

    mail = {
        'from' : '',
        'to' : [],
        'subject' : '',
        'message' : ''
    }

    for real,femail in email.Utils.getaddresses(msg.get_all('from',[])):
        mail['from'] = femail

    for real,femail in email.Utils.getaddresses(msg.get_all('to',[])):
        mail['to'].append(femail)

    ss = decode_header(msg.get_all('subject',[])[0])[0]
    if ss[1] != None:
        mail['subject'] = ss[0].decode(ss[1])
    else:
        mail['subject'] = ss[0]

    et = msg.get_content_type()

    if et.startswith("multipart"):
        mail['message'] = msg.get_payload()[0].get_payload().strip()
    elif et.startswith("text"):
        mail['message'] = msg.get_payload().strip()
    else:
        mail['message'] = ''


    #conn.store(msg.id, '+FLAGS', "\\Answered")

    print mail
