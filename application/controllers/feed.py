from application.controllers.core import CoreHandler
from application.model import Ord

class FeedHandler(CoreHandler):
    def get(self):
        if self.request.headers['User-Agent'].find('FeedBurner') == -1:
            self.redirect('http://feeds.feedburner.com/dagensordibekk', permanent=True)
        else:
            dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
            self.response.headers["Content-Type"] = "application/atom+xml"
            self.renderUsingTemplate('../../views/atom_feed.xml', { 'ord':dagensOrd })
