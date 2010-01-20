import cgi
import os
import urllib

from datetime import datetime

from application.authorization import Authorization
from application.model import Kommentar
from application.model import Bidragsyter
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

class KommentarHjelper:
	@staticmethod
	def hentDataForVisning(uri):
		kommentarer = Kommentar.all().filter("uri = ", uri).order('kommentartidspunkt').fetch(limit=500)
		return { 'kommentarer':kommentarer, 'uri' : uri	 }
		
class VisKommentarHandler(webapp.RequestHandler):
	def get(self, uri):
		if uri == "":
			self.redirect("/")
		else:
			template_values = KommentarHjelper.hentDataForVisning(urllib.unquote(uri))
			path = os.path.join(os.path.dirname(__file__), '../views/kommentarer.html')
			self.response.out.write(template.render(path, template_values))

class LeggInnKommentarHandler(webapp.RequestHandler):
	
	def post(self):
		if Authorization.authorize(self):
			kommentar_uri = cgi.escape(self.request.get('uri'))
			kommentar_innhold = cgi.escape(self.request.get('kommentar'))
			bidrager = Bidragsyter.hent(users.get_current_user())
			Kommentar(innhold=kommentar_innhold, bidragsyter=bidrager, uri=kommentar_uri).put()
				
			template_values = KommentarHjelper.hentDataForVisning(kommentar_uri)
			path = os.path.join(os.path.dirname(__file__), '../views/kommentarer.html')
			self.response.out.write(template.render(path, template_values))