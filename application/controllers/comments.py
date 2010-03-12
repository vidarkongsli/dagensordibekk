import cgi
import os
import urllib

from application.authorization import Authorization
from application.controllers.core import CoreHandler
from application.model import Kommentar, Bidragsyter
from google.appengine.api import users

class KommentarHjelper:
	@staticmethod
	def hentDataForVisning(uri):
		kommentarer = Kommentar.all().filter("uri = ", uri).order('kommentartidspunkt').fetch(limit=500)
		return { 'kommentarer':kommentarer, 'uri' : uri	 }
		
class VisKommentarHandler(CoreHandler):
	# '/kommentar/(.+)'
	def get(self, uri):
		self.renderUsingTemplate('../../views/kommentarer.html', KommentarHjelper.hentDataForVisning(urllib.unquote(uri)))
			
class LeggInnKommentarHandler(CoreHandler):
	# '/kommentar/ny'
	def post(self):
		if Authorization.authorize(self):
			kommentar_uri = cgi.escape(self.request.get('uri'))
			kommentar_innhold = cgi.escape(self.request.get('kommentar'))
			bidrager = Bidragsyter.hent(users.get_current_user())
			Kommentar(innhold=kommentar_innhold, bidragsyter=bidrager, uri=kommentar_uri).put()
			self.renderUsingTemplate('../../views/kommentarer.html', KommentarHjelper.hentDataForVisning(kommentar_uri))