from google.appengine.api import users
from application.model import Bidragsyter
class Authorization:
	@staticmethod
	def authorize(requestHandler):
		user = users.get_current_user()
		if not user:
			requestHandler.redirect(users.create_login_url(requestHandler.request.uri))
		else:
			bidragsyter = Bidragsyter.all().filter("googleKonto = ", user).get()
			if not bidragsyter == None:
				if bidragsyter.svartelistet:
					requestHandler.error(403)
					return False
		return True
