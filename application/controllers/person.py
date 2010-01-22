import cgi
import os
from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import logging
import urllib
from application.authorization import Authorization
from application.controllers.core import CoreHandler
from application.model import Bidragsyter

class BidragsyterHandler(CoreHandler):
	@login_required
	def get(self, key):
		user = users.get_current_user()
		bidragsyter = Bidragsyter.all().filter('__key__ =', db.Key(key)).get()
		if bidragsyter == None:
			self.error(404)
		self.renderUsingTemplate('../../views/bidragsyter.html', { 'bidragsyter': bidragsyter, 'edit' : (user == bidragsyter.googleKonto)})

	def post(self, key):
		if Authorization.authorize(self):
			field = cgi.escape(self.request.get('field'))
			value = cgi.escape(self.request.get('text'))
			user = users.get_current_user()
			bidragsyter = Bidragsyter.all().filter('__key__ =', db.Key(key)).filter('googleKonto =', user).get()
			if bidragsyter == None:
				self.error(404)
			else: 
				if field == "nickname":
					bidragsyter.navn = value
				if field == "twitter":
					bidragsyter.twitter = value
				bidragsyter.put()
				self.response.out.write(value);
		else:
			self.error(302)
