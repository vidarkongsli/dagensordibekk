from .core import CoreHandler
from ..model import Ord, Bidragsyter, Konto
from datetime import datetime
from google.appengine.ext import webapp
import logging
import httplib, urllib
from google.appengine.api.labs.taskqueue import Task, Queue

class SocialcastHandler(CoreHandler):
    
    def __konto(self):
        return Konto.get('sc_bekk')
    
    def get(self):
        dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
        if dagensOrd != None:
            logging.info(u"Setter dagens ord (%s) på Socialcast" % dagensOrd.navn)            
            message = (u"""%s

%s

(Foreslått av %s)""" % (dagensOrd.navn, dagensOrd.beskrivelse, dagensOrd.bnavn())).encode('utf-8')
            
            params = urllib.urlencode({'message[group_id]': '150', 'message[body]': message, 'message[url]':(u"http://dagensordibekk.appspot.com/ord/%s" % dagensOrd.navn).encode('utf-8') })
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json", "Authorization": self.__konto().as_basic_auth_header()}
            conn = httplib.HTTPSConnection("socialcast.bekk.no")
            conn.request("POST", "/api/messages.json", params, headers)
            response = conn.getresponse()
            status = response.status
            response = response.read()
            conn.close()
            if status != 201:
                logging.error(reponse + " " + str(status))
                self.response.out.write(response)
            else:
                self.response.out.write("OK")
        else:
            logging.error("Fant ikke dagens ord")
            self.error(500)
            self.response.out.write("Fant ikke dagens ord")
