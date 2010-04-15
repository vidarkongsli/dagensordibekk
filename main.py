from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from application.controllers.cron import ValgHandler, SettDagensOrdHandler, TwitterHandler, MailHandler
from application.controllers.admin import BidragsytereVisningsHandler, BidragsyterSvartelisteHandler, MapBidragsyterHandler
from application.controllers.comments import LeggInnKommentarHandler, VisKommentarHandler
from application.controllers.likes import LikerHandler
from application.controllers.word import NyttOrdHandler, ForslagHandler, TilGodkjenningHandler, TilGodkjenningHandlerGammel, NesteDagensOrdHandler, StemmeHandler, VisDagensOrdHandler, OrdHandler
from application.controllers.feed import FeedHandler
from application.controllers.person import BidragsyterHandler
from application.controllers.search import SokHandler
from application.controllers.tasks import TwitterUpdateTaskHandler, MailSender

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
									  ('/ord/paavalg_gammel', TilGodkjenningHandlerGammel),
									  ('/ord/feed', FeedHandler),
									  ('/ord/neste', NesteDagensOrdHandler),
									  ('/ord/sok/(.*)', SokHandler),
									  ('/ord/(.*)', OrdHandler),
									  ('/kommentar/ny', LeggInnKommentarHandler),
									  ('/kommentar/(.+)', VisKommentarHandler),
									  ('/liker/ny', LikerHandler),
									  ('/liker/(.+)', LikerHandler),
									  ('/admin/bidragsyter', BidragsytereVisningsHandler),
									  ('/admin/bidragsyter/svartelist', BidragsyterSvartelisteHandler),
                                      ('/admin/bidragsyter/map', MapBidragsyterHandler),
                                      ('/task/twitter', TwitterUpdateTaskHandler),
                                      ('/task/mail', MailSender),
									  ('/person/(.+)', BidragsyterHandler)],
                                     debug=False)
	
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
