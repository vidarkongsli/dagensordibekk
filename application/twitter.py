'''
Created on 17. mars 2010

@author: vidar kongsli
'''
from google.appengine.api import urlfetch
import urllib
from .model import Konto
import logging

class Twitter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def send_dagens_ord_update(self, dagensOrd):
        status = (u"%s (%s ): %s" % ( dagensOrd.navn, self.shortened_url_to_dagens_ord(dagensOrd), dagensOrd.beskrivelse )).encode('utf-8')
        self.update(status)
           
    def send_liker_update(self, ord, bidragsyter):
        status = (u'Ordet %s (%s ) behager %s' % (ord.navn, self.shortened_url_to_dagens_ord(ord), self.bidragsyter_twitter_navn(bidragsyter))).encode('utf-8')
        self.update(status)
    
    def send_kommentar_update(self, ord, bidragsyter):
        status = (u'Ordet %s (%s ) kommentert av %s' % (ord.navn, self.shortened_url_to_dagens_ord(ord), self.bidragsyter_twitter_navn(bidragsyter))).encode('utf-8')
        self.update(status)
        
    def update(self, status):
        if len(status) > 140:
            status = status[:137] + '...'
        api_url = "http://twitter.com/statuses/update.json?status=%s" % urllib.quote(status)
        result = urlfetch.fetch(url=api_url, payload={}, method=urlfetch.POST, headers = { 'Authorization' : Konto.get('twitter').as_basic_auth_header() })
        if result.status_code == 200:
            logging.info("Successfully updated twitter status")
            logging.info(result.content)
        else:
            logging.error("Twitter returned status code %i" % result.status_code)
            logging.error(result.content)

    def bidragsyter_twitter_navn(self, bidragsyter):
        return '@' + bidragsyter.twitter if bidragsyter.twitter != '' else bidragsyter.visningsnavn()    
    
    def shortened_url_to_dagens_ord(self, ord):
        return self.shortenUrl(u'http://dagensordibekk.appspot.com/ord/' + ord.navn)
        
    #Shortens a URL using is.gd - if any errors occur it will return the original url.
    def shortenUrl(self, url):    
        try:
            result = urlfetch.fetch("http://is.gd/api.php?longurl=" + urllib.quote(url.encode('utf-8')))
            if result.status_code == 200:
                return result.content
            else:
                return url
        except:
            return url