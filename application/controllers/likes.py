from application.authorization import Authorization
from .core import CoreHandler
from application.model import Bidragsyter, Liker
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
import cgi
import urllib
from google.appengine.api.labs import taskqueue

class LikerHandler(CoreHandler):
    def post(self):
        if Authorization.authorize(self):
            liker_uri = cgi.escape(self.request.get('uri'))
            bidrager = Bidragsyter.hent(users.get_current_user())
            if Liker.fra_person(liker_uri, bidrager) != None:
                self.renderAsJson({ 'errorCode' : 1})
            else:            
                Liker(bidragsyter=bidrager, uri=liker_uri).put()
                taskqueue.add(url='/task/twitter', params={ 'message_key' : 1, 'uri' : liker_uri, 'bidragsyter' : bidrager.key() })
                self.renderAsJson({ 'errorCode': 0, 'numberOfLikes' : Liker.antall_liker(liker_uri), 'likerDuOrdet' : True })

    @login_required
    def get(self, uri):
        liker_uri = urllib.unquote(uri)
        bidrager = Bidragsyter.hent(users.get_current_user())
        liker_ordet = Liker.fra_person(liker_uri, bidrager) != None
        
        self.renderAsJson({ 'errorCode': 0, 'numberOfLikes' : Liker.antall_liker(liker_uri), 'likerDuOrdet' : liker_ordet })

    def delete(self, uri):
        if Authorization.authorize(self):
            liker_uri = urllib.unquote(uri)
            bidrager = Bidragsyter.hent(users.get_current_user())
            eksisterende_liker = Liker.fra_person(liker_uri, bidrager)
            if eksisterende_liker != None:
                eksisterende_liker.delete()
            self.renderAsJson( { 'errorCode': 0, 'numberOfLikes' : Liker.antall_liker(liker_uri), 'likerDuOrdet' : False })
