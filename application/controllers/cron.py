from google.appengine.ext import webapp
from application.model import Ord
from application.model import Bidragsyter
from datetime import datetime

class ValgHandler(webapp.RequestHandler):
	def get(self):
		paaValg = []
		ordKlareForValg = Ord.gql("WHERE arbeidsflytstilstand = 0")
		for o in ordKlareForValg:
			if len(o.stemmerFor) + len(o.stemmerMot) >= 3:
				if len(o.stemmerFor) > len(o.stemmerMot):
					o.arbeidsflytstilstand = 1
				else:
					o.arbeidsflytstilstand = 2
				o.put()
				paaValg.append(o.navn)
		self.response.headers.add_header("Content-type", "text/plain;encoding=ascii")
		self.response.out.write("Ord på valg: " + str(paaValg))
		
class SettDagensOrdHandler(webapp.RequestHandler):
		
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		nesteDagensOrd = Ord.all().filter("arbeidsflytstilstand =", 1).filter("harVaertDagensOrd =", False).get()
		if nesteDagensOrd == None:
			nesteDagensOrd = Ord.all().filter("harVaertDagensOrd =", True).order('sisteDagensOrdDato').get()
		if nesteDagensOrd == None:
			return
			
		nesteDagensOrd.harVaertDagensOrd = True
		nesteDagensOrd.erDagensOrd = True
		nesteDagensOrd.sisteDagensOrdDato = datetime.utcnow()
		nesteDagensOrd.dagensOrdDatoer.append(datetime.utcnow())
		
		if not dagensOrd == None:
			dagensOrd.erDagensOrd = False
			dagensOrd.put()
		nesteDagensOrd.put()
	
		self.response.headers.add_header("Content-type", "text/plain;encoding=ascii")
		output = ""
		if not dagensOrd == None:
			output = "Gammel: " + dagensOrd.navn + ", ny: " + nesteDagensOrd.navn
		else: 
			output = "Forste dagens ord: " + nesteDagensOrd.navn
		self.response.out.write(output)
