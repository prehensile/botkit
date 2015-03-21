# -*- coding: utf-8 -*-

import cherrypy
import jinja2
import morris
import tweepy

class Templates( object ):
    index = \
    """
    {% extends "layout.html" %}
    {% block body %}
        {% if error %}<p class=error><strong>Error:</strong> {{ error }}{% endif %}
        {% if has_token %}<p>Token receieved!</p>{% endif %}
        <a href="/twitter_auth_start">Link</a>
    {% endblock %}
    """

    layout = \
    """
    <!doctype html>
    <title>Twitter login</title>
    <div class=page>
      <h1>Twitter login</h1>
      {% block body %}{% endblock %}
    </div>
    """

class InterfaceViews( object ):

    def __init__( self, api_key=None, api_secret=None ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._jinja_env = jinja2.Environment( 
            loader=jinja2.DictLoader({
                "index.html" : Templates.index,
                "layout.html" : Templates.layout
            })
        )

    def render_template( self, template, **kwargs ):
        tmpl = self._jinja_env.get_template( template )
        return tmpl.render( **kwargs )

    @cherrypy.expose
    def home( self ):        
        token = cherrypy.session.get('request_token')
        has_token = token != None
        return self.render_template( 'index.html', has_token=has_token )

    @cherrypy.expose
    def twitter_auth_callback( self, oauth_token=None, oauth_verifier=None ):
        
        auth = self.get_auth()
        token = cherrypy.session.get('request_token')
        auth.request_token = token

        try:
            auth.get_access_token( oauth_verifier )
        except:
            cherrypy.log( "Auth error", traceback=True )
            raise cherrypy.HTTPError( 403 )
        
        print oauth_token
        print "auth.access_token: %s" % auth.access_token
        print "auth.access_token_secret: %s" % auth.access_token_secret

        self.save_access_token( auth.access_token,
                                auth.access_token_secret )

        raise cherrypy.HTTPRedirect( cherrypy.url('home') )

    @morris.signal
    def save_access_token( self, access_token,
                                 access_token_secret ):
        """ This is a morris signal."""
        pass

    @cherrypy.expose
    def twitter_auth_start( self ):
        auth = self.get_auth()
        redirect_url = auth.get_authorization_url()
        cherrypy.session['request_token'] = auth.request_token
        raise cherrypy.HTTPRedirect( redirect_url )

    def get_auth( self ):
        callback_url = cherrypy.url('twitter_auth_callback')
        auth = tweepy.OAuthHandler( self._api_key, self._api_secret, callback_url )
        return auth

class WebInterface( object ):

    def __init__( self, api_key=None, api_secret=None, save_token_callback=None ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._save_token_callback = save_token_callback

    def start( self ):
        cherrypy.engine.signal_handler.subscribe()
        cherrypy.config.update( {'server.socket_host': '0.0.0.0'} )
        
        views = InterfaceViews( api_key=self._api_key, api_secret=self._api_secret )
        views.save_access_token.connect( self._save_token_callback )
        
        conf = {
             '/': {
                 'tools.sessions.on': True,
             }
        }
        cherrypy.tree.mount( views, "", config=conf )
        cherrypy.engine.start()

    def stop( self ):
        self.shutdown()

    def shutdown( self ):
        cherrypy.engine.exit()

if __name__ == '__main__':
    interface = WebInterface()
    interface.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    interface.stop()
