from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from application.model import Ord

class FeedHandler(webapp.RequestHandler):
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		template_values = { 'ord':dagensOrd }
		self.response.headers["Content-Type"] = "application/atom+xml"
		path = os.path.join(os.path.dirname(__file__), '../../views/atom_feed.xml')
		self.response.out.write(template.render(path, template_values))