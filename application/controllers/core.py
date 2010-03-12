from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class CoreHandler(webapp.RequestHandler):
    def renderUsingTemplate(self, relativePath, values):
        path = os.path.join(os.path.dirname(__file__), relativePath)
        self.response.out.write(template.render(path, values))
        
    def renderAsJson(self, values):
        self.response.headers["Content-Type"] = 'application/json'
        self.response.out.write(simplejson.dumps(values))