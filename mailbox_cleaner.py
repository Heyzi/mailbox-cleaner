# -*- coding: utf-8 -*-
import os, sys, getpass
import poplib
from email.utils import parsedate_tz
import calendar
import datetime
from datetime import datetime, timedelta


# date checker



def get_last_message_id(messages_ids, M, last_wanted):
    for i in messages_ids:
        try:
            message_lines = M.top( str(i), '0')[1]
        except poplib.error_proto:
            print 'POP problem...'
            continue

        for line in message_lines:
            if line.startswith('Date:'):

                date_hdr = line.partition('Date: ')[2]
                #print date_hdr
                try:
                    (y, month, d, \
                     h, min, sec, \
                     _, _, _, tzoffset) = parsedate_tz(date_hdr)
                except (TypeError): continue
                except (ValueError): continue

                # Python range builtin ?
                date = datetime(y, month, d, h, min, sec)
                if date < last_wanted:
                    return i

# pop config
with open('india.txt') as f:
    credentials = [x.strip().split(':') for x in f.readlines()]
    for username,password in credentials:
        try:
            last_wanted = datetime.now() + timedelta(days=-7)
            #print 'Delete older: ' , last_wanted.strftime("%d %B, %Y")
            M = poplib.POP3('mx25.valuehost.ru')
            print 'mailbox: ', username
            M.user(username)
            M.pass_(password)
            messages_ids = [ int(m.split()[0]) for m in M.list()[1]]
            messages_ids.reverse()
            print 'Total msg count: ', len(messages_ids)
            last_id = get_last_message_id(messages_ids, M, last_wanted)
            messages_to_delete = [i for i in messages_ids if i < last_id]
            #M.set_debuglevel(2)
            for i in messages_to_delete:
                M.dele( str(i) )
            M.quit()
            print 'Deleted: ', len(messages_to_delete)
        except:
            print ('Unkn error')
