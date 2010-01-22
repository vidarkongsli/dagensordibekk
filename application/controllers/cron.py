from google.appengine.ext import webapp
from application.model import Ord
from application.model import Bidragsyter
from datetime import datetime
import logging

class ValgHandler(webapp.RequestHandler):
	def get(self):
		paaValg = []
		ordKlareForValg = Ord.gql("WHERE arbeidsflytstilstand = 0")
		for o in ordKlareForValg:
			if len(o.stemmerFor) + len(o.stemmerMot) >= 3:
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
