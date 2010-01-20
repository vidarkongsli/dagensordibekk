import cgi
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from application.model import Bidragsyter
from datetime import datetime

class BidragsyterVisningsHandler(webapp.RequestHandler):
	def get(self):
		bidragsytere = Bidragsyter.all().order('navn')
		template_map = { 'bidragsytere': bidragsytere}
		path = os.path.join(os.path.dirname(__file__), '../views/bidragsytere_liste.html')
		self.response.out.write(template.render(path, template_map))

class BidragsyterSvartelisteHandler(webapp.RequestHandler):
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
			
		self.response.out.write("{'errorCode':" + str(errorCode) + "}") 	
