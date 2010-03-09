#encoding: utf-8
from datetime import date
from datetime import datetime
from google.appengine.ext import db
import urllib, hashlib
import base64

class Bidragsyter(db.Model):
	googleKonto = db.UserProperty()
	navn = db.StringProperty()
	twitter = db.StringProperty(default="")
	svartelistet = db.BooleanProperty(default=False)
	bekkAdresse = db.EmailProperty()
	paaBekkMailliste = db.BooleanProperty(default=False)
	paaGoogleMailliste = db.BooleanProperty(default=False)
	
	def visningsnavn(self):
		if self.navn == None or self.navn == "":
			if self.googleKonto != None:
				return self.googleKonto.nickname()
			return "ukjent"
		return self.navn
	
	@staticmethod
	def hent(user):
		bidragsyter = Bidragsyter.gql("WHERE googleKonto = :1", user).get()
		if bidragsyter == None:
			bidragsyter = Bidragsyter(navn=user.nickname(), googleKonto=user)
			bidragsyter.put()
		return bidragsyter

class Ord(db.Model):
	navn = db.StringProperty()
	beskrivelse = db.TextProperty()
	bidragsyter = db.ReferenceProperty(Bidragsyter)
	bidragsyter_navn = db.TextProperty(default="")
	dagensOrdDatoer = db.ListProperty(datetime, default=[])
	harVaertDagensOrd = db.BooleanProperty(default=False)
	sisteDagensOrdDato = db.DateTimeProperty()
	erDagensOrd = db.BooleanProperty(default=False)
	stemmerFor = db.ListProperty(long, default=[])
	stemmerMot = db.ListProperty(long, default=[])
	arbeidsflytstilstand = db.IntegerProperty(default=0)
	forslagstidspunkt = db.DateTimeProperty(auto_now_add=True)
	
	def arbeidsflytstilstand_navn(self):
		if self.arbeidsflytstilstand == 0:
			return "På valg"
		if self.arbeidsflytstilstand == 1:
			return "Godkjent"
		return "Avslått"
	
	def bnavn(self):
		if self.bidragsyter == None:
			return self.bidragsyter_navn
		return self.bidragsyter.visningsnavn()

class Kommentar(db.Model):
	innhold = db.StringProperty(multiline=True)
	bidragsyter = db.ReferenceProperty(Bidragsyter)
	kommentartidspunkt = db.DateTimeProperty(auto_now_add=True)
	uri = db.StringProperty()
	
	def gravatarUrl(self):
		gravatar_url = "http://www.gravatar.com/avatar.php?"
		gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(self.bidragsyter.googleKonto.email().lower()).hexdigest(), 'size':'40'})
		return gravatar_url

class Liker(db.Model):
	bidragsyter = db.ReferenceProperty(Bidragsyter)
	tidspunkt = db.DateTimeProperty(auto_now_add=True)
	uri = db.StringProperty()

	@staticmethod
	def antall_liker(uri):
		return Liker.all().filter('uri = ', uri).count()
		
	@staticmethod
	def fra_person(uri, bidragsyter):
		return Liker.all().filter('uri =', uri).filter('bidragsyter =', bidragsyter).get()
	
class Konto(db.Model):
	navn = db.StringProperty()
	brukernavn = db.StringProperty()
	passord = db.StringProperty()
	
	@staticmethod
	def get(navn):
		if Konto.all().get() == None:
			Konto(navn='dummy', brukernavn='dummy', passord = 'dummy').put()
		return Konto.all().filter('navn = ', navn).get()
		
	def as_basic_auth_header(self):
		base64string = base64.encodestring('%s:%s' % (self.brukernavn, self.passord))[:-1]
		return "Basic %s" % base64string

