'''
Created on 17. mars 2010

@author: vidar kongsli
'''
from google.appengine.api import urlfetch
import urllib
from .model import Konto
import logging
import oauth

class Twitter(object):

    def __init__(self):
        self.consumer_key = "uJDoRvGZMCd9SjEDGoomtA"
        self.consumer_secret = "okYariZZL0JbNr7vzXgOI8RaXSSFulACneXxTbJzR0"
        self.callback_url = "http://dagensordibekk.appspot.com/twittercallback"
		
    def lag_twitter_autentiserings_url(self):
        return oauth.TwitterClient(self.consumer_key, self.consumer_secret, self.callback_url).get_authorization_url()

    def lagre_auth_data(self, request, bidrager):
        client = oauth.TwitterClient(self.consumer_key, self.consumer_secret, self.callback_url)
        auth_token = request.get("oauth_token")
        auth_verifier = request.get("oauth_verifier")
        user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
        bidrager.twitter_token = user_info['token']
        bidrager.twitter_token_secret = user_info['secret']
        bidrager.twitter_username = user_info['username']
        bidrager.twitter_name = user_info['name']
        bidrager.put()

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
        
        twitter_konto = Konto.get('twitter')
        client = oauth.TwitterClient(self.consumer_key, self.consumer_secret, self.callback_url)

        additional_params = {
            'status' : status
        }
        
        result = client.make_request(
             "http://twitter.com/statuses/update.json",
              token=twitter_konto.oauth_token,
              secret=twitter_konto.oauth_secret,
              additional_params=additional_params,
              method=urlfetch.POST)

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