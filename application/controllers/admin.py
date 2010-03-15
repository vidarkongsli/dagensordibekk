from .core import CoreHandler
from ..model import Ord, Bidragsyter
from ..authorization import Authorization
import cgi
import logging
from google.appengine.ext import db

class BidragsytereVisningsHandler(CoreHandler):
    def get(self):
        bidragsytere = Bidragsyter.all().order('navn')
        self.renderUsingTemplate('../../views/bidragsytere_liste.html', { 'bidragsytere': bidragsytere })

class BidragsyterSvartelisteHandler(CoreHandler):
    def post(self):
        errorCode = 0
        bidragsyterId = long(cgi.escape(self.request.get('bidragsyterId')))
        skalSvartelistes = bool(cgi.escape(self.request.get('skalSvartelistes')).capitalize())
        bidragsyter = Bidragsyter.get_by_id(bidragsyterId)
        if bidragsyter == None:
            errorCode = 1
        else:
            bidragsyter.svartelistet = skalSvartelistes
            bidragsyter.put()
            
        self.renderAsJson({ 'errorCode' : errorCode })
        
class MapBidragsyterHandler(CoreHandler):
    def get(self):
        ord = Ord.all().filter('bidragsyter = ', None).fetch(900)
        navn = set(map(lambda n : n.bidragsyter_navn, ord))
        self.renderUsingTemplate('../../views/admin_user_mapping.html', { 'navn' : navn, 'bidragsytere' : Bidragsyter.all().fetch(100) })

    def post(self):
        if Authorization.authorize(self):
            konto = cgi.escape(filter(lambda k : k != '', self.request.get_all('konto'))[0])
            navn = cgi.escape(self.request.get('navn'))
            logging.info(navn)
            bidragsyter = Bidragsyter.all().filter('__key__ =', db.Key(konto)).get()
            if bidragsyter != None:
                logging.info('bidragsyter funnet')
                ord = Ord().all().filter('bidragsyter = ', None).fetch(900)
                logging.info(len(ord))
                for o in ord:
                    if o.bidragsyter_navn == navn:
                        logging.info('setter bidragsyter for %s' % o.navn)
                        o.bidragsyter = bidragsyter
                        o.bidragsyter_navn = None
                        o.put()
        
            self.redirect(self.request.path, False)