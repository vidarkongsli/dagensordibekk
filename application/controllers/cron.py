from google.appengine.api import mail
from google.appengine.ext import webapp
from application.controllers.core import CoreHandler
from application.model import Ord,Bidragsyter,Konto
from datetime import datetime
import logging
from google.appengine.api import urlfetch
from django.utils import simplejson
import base64
import urllib

class ValgHandler(webapp.RequestHandler):
	def get(self):
		paaValg = []
		ordKlareForValg = Ord.gql("WHERE arbeidsflytstilstand = 0")
		for o in ordKlareForValg:
			if len(o.stemmerFor) + len(o.stemmerMot) >= 5:
				if len(o.stemmerFor) > len(o.stemmerMot):
					o.arbeidsflytstilstand = 1
					logging.info("Ordet '%s' er godkjent" % o.navn)
				else:
					o.arbeidsflytstilstand = 2
					logging.info("Ordet '%s' er underkjent" % o.navn)
				o.put()
				paaValg.append(o.navn)
		self.response.headers.add_header("Content-type", "text/plain;encoding=ascii")
		self.response.out.write("Ord på valg: " + str(paaValg))
		
class SettDagensOrdHandler(webapp.RequestHandler):
		
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		nesteDagensOrd = Ord.all().filter("arbeidsflytstilstand =", 1).filter("harVaertDagensOrd =", False).get()
		if nesteDagensOrd == None:
			logging.info("Fant ingen nye ord. Leter etter neste dagens ord blandt gamle ord...")
			nesteDagensOrd = Ord.all().filter("harVaertDagensOrd =", True).order('sisteDagensOrdDato').get()
		if nesteDagensOrd == None:
			logging.warning("Fant ei noen ord blant gamle ord. Her er det noe muffins")
			return
			
		nesteDagensOrd.harVaertDagensOrd = True
		nesteDagensOrd.erDagensOrd = True
		nesteDagensOrd.sisteDagensOrdDato = datetime.utcnow()
		nesteDagensOrd.dagensOrdDatoer.append(datetime.utcnow())
		
		if not dagensOrd == None:
			logging.info("%s er ikke lengre dagens ord" % dagensOrd.navn)
			dagensOrd.erDagensOrd = False
			dagensOrd.put()
		nesteDagensOrd.put()
		logging.info("%s er nytt dagens ord" % nesteDagensOrd.navn)
	
		self.response.headers.add_header("Content-type", "text/plain;encoding=ascii")
		output = ""
		if not dagensOrd == None:
			output = "Gammel: " + dagensOrd.navn + ", ny: " + nesteDagensOrd.navn
		else: 
			output = "Forste dagens ord: " + nesteDagensOrd.navn
		self.response.out.write(output)

class TwitterHandler(CoreHandler):
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		if dagensOrd != None:
			status = (u"%s (%s): %s" % ( dagensOrd.navn, self.shortenUrl(u'http://dagensordibekk.appspot.com/ord/' + dagensOrd.navn), dagensOrd.beskrivelse)).encode('utf-8')
			api_url = "http://twitter.com/statuses/update.json?status=%s" % urllib.quote(status)
			result = urlfetch.fetch(url=api_url, payload={}, method=urlfetch.POST, headers = { 'Authorization' : Konto.get('twitter').as_basic_auth_header() })
			if result.status_code == 200:
				logging.info("Successfully updated twitter status")
				logging.info(result.content)
			else:
				logging.error("Twitter returned status code %i" % result.status_code)
				logging.error(result.content)
				self.error(500)
			self.response.out.write(str(result.status_code) + "|" + result.content)
		else:
			logging.error("Fant ikke dagens ord")
			self.error(500)
			self.response.out.write("Fant ikke dagens ord")
			
	#Shortens a URL using is.gd - if any errors occur it will return the original url.
	def shortenUrl(self, url):	
		try:
			result = urlfetch.fetch("http://is.gd/api.php?longurl=" + urllib.quote(url.encode('utf-8')))
			if result.status_code == 200:
				return result.content
			else:
				return url
		except:
			return url
			
class MailHandler(CoreHandler):
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		if dagensOrd != None:
			googleAddresses = map(lambda x: x.googleKonto.email(), Bidragsyter.all().filter('paaGoogleMailliste =', True).fetch(100))
			bekkAddresses = map(lambda x: x.bekkAdresse, Bidragsyter.all().filter('paaBekkMailliste', True).fetch(100))
			logging.info('Sending mail to %s' % ','.join(googleAddresses + bekkAddresses))
			to = googleAddresses + bekkAddresses
			subject = dagensOrd.navn
			body = """
			
%s

%s

---------------------------------------------------------------------

Ordet er fremmet av: %s
Nye ord fremmes her: %s
Denne tjenesten leveres av Dagens Ord-Komiteen. (c) 2003-2010
""" % (dagensOrd.navn, dagensOrd.beskrivelse, dagensOrd.bnavn(), "http://dagensordibekk.appspot.com/ord/nytt")
			mail.send_mail("Dagens Ord <vidar.kongsli@gmail.com>", to, subject, body)
			self.response.out.write('Mail sendt')