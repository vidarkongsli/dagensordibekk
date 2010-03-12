from application.model import Ord
from application.controllers.core import CoreHandler

class FeedHandler(CoreHandler):
	def get(self):
		dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
		self.response.headers["Content-Type"] = "application/atom+xml"
		self.renderUsingTemplate('../../views/atom_feed.xml', { 'ord':dagensOrd })
