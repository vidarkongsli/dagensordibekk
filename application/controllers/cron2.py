from .core import CoreHandler
from ..model import Ord, Bidragsyter
from ..twitter import Twitter
from datetime import datetime
from google.appengine.ext import webapp
import logging
from google.appengine.api.labs.taskqueue import Task, Queue

class ValgHandler(webapp.RequestHandler):
    def get(self):
        paaValg = []
        ordKlareForValg = Ord.gql("WHERE arbeidsflytstilstand = 0")
        for o in ordKlareForValg:
            if len(o.stemmerFor) + len(o.stemmerMot) >= 5:
                if len(o.stemmerFor) > len(o.stemmerMot):
                    o.arbeidsflytstilstand = 1
                    logging.info("Ordet '%s' er godkjent" % o.navn)
                else:
                    o.arbeidsflytstilstand = 2
                    logging.info("Ordet '%s' er underkjent" % o.navn)
                o.put()
                paaValg.append(o.navn)
        self.response.headers.add_header("Content-type", "text/plain;encoding=ascii")
        self.response.out.write("Ord på valg: " + str(paaValg))
        
class SettDagensOrdHandler(webapp.RequestHandler):
        
    def get(self):
        dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
        nesteDagensOrd = Ord.all().filter("arbeidsflytstilstand =", 1).filter("harVaertDagensOrd =", False).get()
        if nesteDagensOrd == None:
            logging.info("Fant ingen nye ord. Leter etter neste dagens ord blandt gamle ord...")
            nesteDagensOrd = Ord.all().filter("harVaertDagensOrd =", True).order('sisteDagensOrdDato').get()
        if nesteDagensOrd == None:
            logging.warning("Fant ei noen ord blant gamle ord. Her er det noe muffins")
            return
            
        nesteDagensOrd.harVaertDagensOrd = True
        nesteDagensOrd.erDagensOrd = True
        nesteDagensOrd.sisteDagensOrdDato = datetime.utcnow()
        nesteDagensOrd.dagensOrdDatoer.append(datetime.utcnow())
        
        if not dagensOrd == None:
            logging.info("%s er ikke lengre dagens ord" % dagensOrd.navn)
            dagensOrd.erDagensOrd = False
            dagensOrd.put()
        nesteDagensOrd.put()
        logging.info("%s er nytt dagens ord" % nesteDagensOrd.navn)
    
        self.response.headers.add_header("Content-type", "text/plain;encoding=ascii")
        output = ""
        if not dagensOrd == None:
            output = "Gammel: " + dagensOrd.navn + ", ny: " + nesteDagensOrd.navn
        else: 
            output = "Forste dagens ord: " + nesteDagensOrd.navn
        self.response.out.write(output)

class TwitterHandler(CoreHandler):
    def get(self):
        dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
        if dagensOrd != None:
            Twitter().send_dagens_ord_update(dagensOrd)
        else:
            logging.error("Fant ikke dagens ord")
            self.error(500)
            self.response.out.write("Fant ikke dagens ord")
            
class MailHandler(CoreHandler):
    def get(self):
        dagensOrd = Ord.all().filter("erDagensOrd =", True).get()
        if dagensOrd != None:
            googleAddresses = map(lambda x: x.googleKonto.email(), Bidragsyter.all().filter('paaGoogleMailliste =', True).fetch(100))
            bekkAddresses = map(lambda x: x.bekkAdresse, Bidragsyter.all().filter('paaBekkMailliste', True).fetch(100))
            to = filter(lambda x: x != None, googleAddresses + bekkAddresses)
            logging.info('Sending mail to %s' % ','.join(to))
            subject = dagensOrd.navn
            body = """
            
%s

%s

---------------------------------------------------------------------

Ordet er fremmet av: %s
Kommenter ordet her: http://dagensordibekk.appspot.com/ord/%s
Nye ord fremmes her: http://dagensordibekk.appspot.com/ord/nytt
Denne tjenesten leveres av Dagens Ord-Komiteen. (c) 2003-2010
""" % (dagensOrd.navn, dagensOrd.beskrivelse, dagensOrd.bnavn(), dagensOrd.navn)
            
            queue = Queue('mail-queue')
            for recipient in to:
                queue.add(Task(url='/task/mail', params= { 'to' : recipient, 'subject' : subject, 'body' : body }))
            
            self.response.out.write('Mail queued')