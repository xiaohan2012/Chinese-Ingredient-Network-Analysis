import webapp2
from common import Handler

class MainPage(Handler):

    def get(self):
        self.render("hand_annotation.html")
        
        
application = webapp2.WSGIApplication([('/', MainPage),],
                                      debug=True)