from datetime import date
from datetime import datetime
from google.appengine.ext import db
import urllib, hashlib

class Bidragsyter(db.Model):
	googleKonto = db.UserProperty()
	navn = db.StringProperty()
	svartelistet = db.BooleanProperty(default=False)
	
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
	
	def bnavn(self):
		if self.bidragsyter == None:
			return self.bidragsyter_navn
		return self.bidragsyter.navn

class Kommentar(db.Model):
	innhold = db.StringProperty(multiline=True)
	bidragsyter = db.ReferenceProperty(Bidragsyter)
	kommentartidspunkt = db.DateTimeProperty(auto_now_add=True)
	uri = db.StringProperty()
	
	def gravatarUrl(self):
		gravatar_url = "http://www.gravatar.com/avatar.php?"
		gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(self.bidragsyter.googleKonto.email().lower()).hexdigest(), 'default':'http://www.some.where.info', 'size':'40'})
		return gravatar_url