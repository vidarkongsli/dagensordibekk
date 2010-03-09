import cgi
import os
import urllib
import logging
from application.authorization import Authorization
from application.controllers.core import CoreHandler
from application.model import Kommentar, Bidragsyter
from google.appengine.api import users
from google.appengine.ext import db

class SokHandler(CoreHandler):
	def get(self, sokeOrd):
		maxCount = 50
		s = unicode(urllib.unquote(sokeOrd).decode('utf-8'))
		if s == '':
			s = self.request.get('q')
			maxCount = int(self.request.get('s', default_value=str(maxCount)))
		logging.info(u'Søk etter ' + s)
		result = db.GqlQuery("SELECT * FROM Ord WHERE navn >= :1 AND navn < :2", s, s + u"\ufffd").fetch(maxCount)
		if 'application/json' in self.request.headers['Accept']:
			filteredResult = map(lambda ord : { 'id': ord.navn, 'name': ord.navn }, result)
			self.renderAsJson({ "results" : filteredResult })
		else:
			self.renderUsingTemplate('../../views/sokeresultater.html', { 'ord' : result, 'sokeord' : s })
