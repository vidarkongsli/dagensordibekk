#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Vidar Kongsli on 2010-09-04.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
from application.authorization import Authorization
from application.controllers.core import CoreHandler
from application.twitter import Twitter
from google.appengine.ext.webapp.util import login_required
import logging

class TwitterAuthenticationHandler(CoreHandler):
	def __init__(self):
		pass
	
	def post(self):
		if Authorization.authorize(self):
			redirect_url = Twitter().lag_twitter_autentiserings_url()
			logging.info('Redirecting user to %s' % redirect_url)
			#self.redirect(redirect_url)
		else:
			self.redirect('/person/me')

	@login_required
	def get(self):
		bidrager = Bidragsyter.hent(users.get_current_user())
		Twitter().lagre_auth_data(self.request, bidrager)
		self.redirect('/person/me')

class TwitterHandlerTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()