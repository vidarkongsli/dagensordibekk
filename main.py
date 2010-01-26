from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
 
from application.model import Bidragsyter
from application.model import Ord
from application.authorization import Authorization
from application.controllers.cron import ValgHandler,SettDagensOrdHandler,TwitterHandler, MailHandler
from application.controllers.admin import BidragsytereVisningsHandler, BidragsyterSvartelisteHandler
from application.controllers.comments import LeggInnKommentarHandler, VisKommentarHandler
from application.controllers.word import NyttOrdHandler, ForslagHandler, TilGodkjenningHandler, NesteDagensOrdHandler, StemmeHandler, VisDagensOrdHandler, OrdHandler
from application.controllers.feed import FeedHandler
from application.controllers.person import BidragsyterHandler

application = webapp.WSGIApplication(
                                     [('/', VisDagensOrdHandler),
									  ('/ord/nytt', NyttOrdHandler),
                                      ('/forslag', ForslagHandler),
									  ('/ord/stem', StemmeHandler),
									  ('/ord/cron/valg', ValgHandler),
									  ('/ord/cron/settdagensord', SettDagensOrdHandler),
									  ('/ord/cron/twitter', TwitterHandler),
									  ('/ord/cron/mail', MailHandler),
									  ('/ord/paavalg', TilGodkjenningHandler),
									  ('/ord/feed', FeedHandler),
									  ('/ord/neste', NesteDagensOrdHandler),
									  ('/ord/(.*)', OrdHandler),
									  ('/kommentar/ny', LeggInnKommentarHandler),
									  ('/kommentar/(.+)', VisKommentarHandler),
									  ('/admin/bidragsyter', BidragsytereVisningsHandler),
									  ('/admin/bidragsyter/svartelist', BidragsyterSvartelisteHandler),
									  ('/person/(.+)', BidragsyterHandler)],
                                     debug=True)
	
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()