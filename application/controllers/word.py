import os
import cgi
import urllib
import logging
from application.authorization import Authorization
from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import login_required
from application.controllers.core import CoreHandler
from application.model import Ord, Bidragsyter

class NyttOrdHandler(CoreHandler):
	@login_required
	def get(self):
		Authorization.authorize(self)
		self.renderUsingTemplate('../../views/forslagsskjema.html', {})

class ForslagHandler(CoreHandler):
	def post(self):
		Authorization.authorize(self)
		ord = cgi.escape(self.request.get('ord')).lower()
		besk = cgi.escape(self.request.get('beskrivelse'))
		
		exists = db.GqlQuery("SELECT * FROM Ord WHERE navn = :1", ord)
		errorCode = 0
		if exists.count() > 0:
			errorCode = 1
		else:
			bidrager = Bidragsyter.hent(users.get_current_user())
			Ord(navn=ord, beskrivelse=besk, bidragsyter=bidrager.key()).put()
		
		self.renderAsJson({ 'errorCode':errorCode })
	
class TilGodkjenningHandler(CoreHandler):
	@login_required
	def get(self):
		alle_ord = Ord.all().filter("arbeidsflytstilstand =", 0).order('navn')
		self.renderUsingTemplate('../../views/liste.html', { 'ord':alle_ord })

class NesteDagensOrdHandler(CoreHandler):
	@login_required
	def get(self):
		alle_ord = []
		alle_nye_godkjente_ord = Ord.all().filter("arbeidsflytstilstand =", 1).filter("harVaertDagensOrd =", False).order('forslagstidspunkt')
		if not alle_nye_godkjente_ord == None:
			alle_ord.extend(alle_nye_godkjente_ord)
		alle_gamle_godkjente_ord = Ord.all().filter("arbeidsflytstilstand =", 1).filter("harVaertDagensOrd =", True).filter("erDagensOrd =", False).order('sisteDagensOrdDato')
		if not alle_gamle_godkjente_ord == None:
			alle_ord.extend(alle_gamle_godkjente_ord)
		self.renderUsingTemplate('../../views/liste_neste.html', { 'ord':alle_ord })
		
class StemmeHandler(CoreHandler):
	def post(self):
		errorCode = 0
		antallStemmer = 0
		Authorization.authorize(self)
		ordNokkel = long(cgi.escape(self.request.get('ord-nokkel')))
		stemmeFor = bool(cgi.escape(self.request.get('erStemmeFor')).capitalize())
		
		ord = Ord.get_by_id(ordNokkel)
		bidragsyterId = Bidragsyter.hent(users.get_current_user()).key().id()
		if ord == None:
			errorCode = 1
		elif bidragsyterId in ord.stemmerFor or bidragsyterId in ord.stemmerMot:
			errorCode = 2
		else:
			if stemmeFor:
				ord.stemmerFor.append(bidragsyterId)
				antallStemmer = len(ord.stemmerFor)
			else:
				ord.stemmerMot.append(bidragsyterId)
				antallStemmer = len(ord.stemmerMot)
			ord.put()
		
		self.renderAsJson({ 'errorCode':errorCode, 'antallStemmer':antallStemmer})

class VisDagensOrdHandler(CoreHandler):
	@login_required
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		self.renderUsingTemplate('../../views/dagens_ord.html', { 'ord':dagensOrd })
		
class OrdHandler(CoreHandler):
	def get(self, ordForesporsel):
		if ordForesporsel == "":
			self.redirect("/")
		else:
			ordStreng = urllib.unquote(ordForesporsel)
			logging.info("Was asked for word " + ordStreng)
			ord = Ord.all().filter("navn =", ordStreng.decode("utf-8")).get()
			if ord == None:
				self.error(404)
			else:
				self.renderUsingTemplate('../../views/dagens_ord.html', { 'ord':ord })