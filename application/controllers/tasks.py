'''
Created on 17. mars 2010

@author: vidar kongsli
'''
from core import CoreHandler
from ..model import Bidragsyter, Ord
from ..twitter import Twitter
from google.appengine.ext import db
import logging
from google.appengine.api import mail

class TwitterUpdateTaskHandler(CoreHandler):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def post(self):
        message_key = int(self.request.get('message_key'))
        ord_key = self.request.get('uri').split(':')[-1]
        bidragsyter_key = self.request.get('bidragsyter')
        
        ord = Ord.get(db.Key(ord_key))
        bidragsyter = Bidragsyter.get(db.Key(bidragsyter_key))
        
        if message_key == 1:
            logging.info('Oppdaterer liker paa twitter')
            Twitter().send_liker_update(ord, bidragsyter)
        elif message_key == 2:
            logging.info('Oppdaterer kommentar paa twitter')
            Twitter().send_kommentar_update(ord, bidragsyter)
        else:
            logging.warning('Ukjent message_key: %i' % message_key)


class MailSender(CoreHandler):
    def post(self):
        to = self.request.get('to')
        subject = self.request.get('subject')
        body = self.request.get('body')
        logging.info("Sending '%s' to %s" % (subject, to))
        mail.send_mail("Dagens Ord <vidar.kongsli@gmail.com>", to, subject, body)
