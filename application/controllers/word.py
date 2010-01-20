import os
from application.authorization import Authorization
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app, login_required
from application.model import Ord

class NyttOrdHandler(webapp.RequestHandler):
	@login_required
	def get(self):
		Authorization.authorize(self)
		path = os.path.join(os.path.dirname(__file__), '../../views/forslagsskjema.html')
		self.response.out.write(template.render(path, {}))

class ForslagHandler(webapp.RequestHandler):
	def post(self):
		Authorization.authorize(self)
		ord = cgi.escape(self.request.get('ord'))
		besk = cgi.escape(self.request.get('beskrivelse'))
		
		exists = db.GqlQuery("SELECT * FROM Ord WHERE navn = :1", ord)
		errorCode = 0
		if exists.count() > 0:
			errorCode = 1
		else:
			bidrager = Bidragsyter.hent(users.get_current_user())
			Ord(navn=ord, beskrivelse=besk, bidragsyter=bidrager.key()).put()
			
		self.response.out.write("{'errorCode':" + `errorCode` + "}")
	
class TilGodkjenningHandler(webapp.RequestHandler):
	@login_required
	def get(self):
		alle_ord = Ord.all().filter("arbeidsflytstilstand =", 0).order('navn')
		template_values = { 'ord':alle_ord }
		path = os.path.join(os.path.dirname(__file__), '../../views/liste.html')
		self.response.out.write(template.render(path, template_values))

class NesteDagensOrdHandler(webapp.RequestHandler):
	@login_required
	def get(self):
		alle_ord = []
		alle_nye_godkjente_ord = Ord.all().filter("arbeidsflytstilstand =", 1).filter("harVaertDagensOrd =", False).order('forslagstidspunkt')
		if not alle_nye_godkjente_ord == None:
			alle_ord.extend(alle_nye_godkjente_ord)
		alle_gamle_godkjente_ord = Ord.all().filter("arbeidsflytstilstand =", 1).filter("harVaertDagensOrd =", True).filter("erDagensOrd =", False).order('sisteDagensOrdDato')
		if not alle_gamle_godkjente_ord == None:
			alle_ord.extend(alle_gamle_godkjente_ord)
		template_values = { 'ord':alle_ord }
		path = os.path.join(os.path.dirname(__file__), '../../views/liste_neste.html')
		self.response.out.write(template.render(path, template_values))
		
class StemmeHandler(webapp.RequestHandler):
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
			
		self.response.out.write("{'errorCode':" + str(errorCode) + ",'antallStemmer':"+str(antallStemmer)+"}") 

class VisDagensOrdHandler(webapp.RequestHandler):
	@login_required
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		template_values = { 'ord':dagensOrd }
		path = os.path.join(os.path.dirname(__file__), '../../views/dagens_ord.html')
		self.response.out.write(template.render(path, template_values))

class OrdHandler(webapp.RequestHandler):
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
				logging.info("The type of beskrivelse is " + str(type(ord.beskrivelse)))
				template_values = { 'ord':ord }
				path = os.path.join(os.path.dirname(__file__), '../../views/dagens_ord.html')
				self.response.out.write(template.render(path, template_values))
