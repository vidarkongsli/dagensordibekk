from application.authorization import Authorization
from application.controllers.core import CoreHandler
from application.model import Bidragsyter
from application.model import Konto
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required
import cgi
import logging

class BidragsyterHandler(CoreHandler):
    @login_required
    def get(self, key):
        user = users.get_current_user()
        if key == 'meg':
            bidragsyter = Bidragsyter.all().filter('googleKonto = ', user).get()
            view = '../../views/bidragsyter_redigerbar.html'
            self.renderUsingTemplate(view, { 'bidragsyter' : bidragsyter, 'har_twitter_integrasjon' : bidragsyter.har_twitter_godkjenning() })
        else:
            try:
                bidragsyter = Bidragsyter.all().filter('__key__ =', db.Key(key)).get()
                if bidragsyter == None:
                    self.not_found()
                else:
                    view = '../../views/bidragsyter_redigerbar.html' if user == bidragsyter.googleKonto else '../../views/bidragsyter.html'
                    self.renderUsingTemplate(view, { 'bidragsyter' : bidragsyter, 'har_twitter_integrasjon' : bidragsyter.har_twitter_godkjenning() })
            except:
                self.not_found()

    def post(self, key):
        if Authorization.authorize(self):
            field = cgi.escape(self.request.get('id'))
            value = cgi.escape(self.request.get('value'))
            user = users.get_current_user()
            bidragsyter = Bidragsyter.all().filter('googleKonto =', user).get()
            if bidragsyter == None:
                self.error(404)
            else:
                field_to_attr = {
                    'nickname'         : 'navn',
                    'twitter'          : 'twitter',
                    'bekk'             : 'bekkAdresse',
                    'bekk-mailliste'   : 'paaBekkMailliste',
                    'google-mailliste' : 'paaGoogleMailliste'
                }
                
                if field in field_to_attr.keys():
                    the_value = value
                    if field in ['bekk-mailliste', 'google-mailliste'] :
                        the_value = bool(int(value))
                        value = { True : 'Ja', False : 'Nei' }[the_value]
                    if the_value == '':
                        the_value = None
                    setattr(bidragsyter, field_to_attr[field], the_value)
                    bidragsyter.put()
                    self.response.out.write(value);
                else:
                    self.error(500)
        else:
            self.error(302)
