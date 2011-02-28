from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from config import *
from auth_config import *
import logging
import os
import tweepy
import wsgiref.handlers
 
class RecordPage(webapp.RequestHandler):
    """
    Initial user greeting. Plays a "speak your tweet" message and then records what caller says.
    """
    def get(self):
        self.post()
     
    def post(self):
        templatevalues = {
            'postprefix': BASE_URL,
        }
        xml_response(self, 'record.xml', templatevalues)
        
class TweetPage(webapp.RequestHandler):
    """
    Posts a tweet with a link to the recording.
    """
    def get(self):
        self.post()
     
    def _error(self, msg, redirecturl=None):
        templatevalues = {
            'msg': msg,
            'redirecturl': redirecturl
        }
        xml_response(self, 'error.xml', templatevalues)
        
    def post(self):
        recording_url = self.request.get('RecordingUrl')
        logging.debug("Recording URL: " + recording_url)
        
        # Twilio recording URLs are massive, so have to shorten to fit in a tweet
        short_url = shorten_url(recording_url)
        
        if short_url:
            # Tweet the link to the recording
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api = tweepy.API(auth)
            api.update_status(TWEET_PREFIX_TEXT + short_url)
            xml_response(self, 'disconnect.xml')
        else:
            self._error("An error occurred while creating a link to the tweet.", BASE_URL + "disconnect")
 
class DisconnectPage(webapp.RequestHandler):
    """
    Disconnects phone call.
    """
    def get(self):
        self.post()
        
    def post(self):
        xml_response(self, 'disconnect.xml')
        
def xml_response(handler, page, templatevalues=None):
    """
    Renders an XML response using a provided template page and optional dict of values
    """
    path = os.path.join(os.path.dirname(__file__), page)
    handler.response.headers["Content-Type"] = "text/xml"
    handler.response.out.write(template.render(path, templatevalues))
    
def shorten_url(long_url):
    """
    Returns a shortened URL. Returns None if an error occurs.
    
    Uses the Google shortener to shorten the extremely long Twilio recording URL.
    """
    from google.appengine.api import urlfetch
    from django.utils import simplejson
    
    request_body = simplejson.dumps({"longUrl": long_url})
    logging.debug("request body: " + request_body)
    reponse = urlfetch.fetch(url="https://www.googleapis.com/urlshortener/v1/url",
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/json'},
                            payload=request_body)
    
    logging.debug("response body: " + str(reponse.content))
    if reponse.status_code != 200:
        return None
    response_dict = simplejson.loads(reponse.content)
    return response_dict["id"]
    
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Set up URL to Class dispatchers
    application = webapp.WSGIApplication([
        ('/', RecordPage),
        ('/tweet', TweetPage),
        ('/disconnect', DisconnectPage)],
        debug=True)
    
    wsgiref.handlers.CGIHandler().run(application)
 
if __name__ == "__main__":
    main()