from .core import CoreHandler
from ..model import Ord, Bidragsyter
from datetime import datetime
from google.appengine.ext import webapp

class ByeHandler(webapp.RequestHandler):
    def get(self):
        dagensOrd = Ord.all().order('navn').fetch(limit=2000)
        self.response.headers.add_header("Content-type", "text/plain;charset=utf-8")
        self.response.out.write("navn;datoer\n")
        for o in dagensOrd:
            self.response.out.write(o.navn + ';' + ','.join(map(lambda dt: dt.isoformat(), o.dagensOrdDatoer)) + '\n')
