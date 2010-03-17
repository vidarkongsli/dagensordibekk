'''
Created on 17. mars 2010

@author: vidar kongsli
'''
from core import CoreHandler
from ..model import Bidragsyter, Ord
from ..twitter import Twitter
from google.appengine.ext import db
import logging

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
            Twitter().send_liker_update(ord, bidragsyter)
        elif message_key == 2:
            Twitter().send_kommentar_update(ord, bidragsyter)
        else:
            logging.warning('Ukjent message_key: %i' % message_key)
