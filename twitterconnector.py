import tweepy

class TwitterConnector( object ):

    def __init__( self, consumer_key=None, consumer_secret=None,
                        access_key=None, access_secret=None ):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_key = access_key
        self._access_secret = access_secret
        self._api = None

    def api( self ):
        if (self._api is None):
            auth = tweepy.OAuthHandler( self._consumer_key, self._consumer_secret )
            auth.set_access_token( self._access_key, self._access_secret )
            self._api = tweepy.API( auth )
        return self._api

    def tweet( self, status ):
        this_api = self.api()
        if this_api is not None:
            try:
                this_api.update_status( status=status )
            except tweepy.error.TweepError as e:
                print e.reason