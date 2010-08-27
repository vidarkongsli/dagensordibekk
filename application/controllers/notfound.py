from .core import CoreHandler

class NotFoundHandler(CoreHandler):
    def get(self):
        self.not_found()
