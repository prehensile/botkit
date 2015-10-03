import tweepy
import logging


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

    def tweet( self, status, in_reply_to_status_id=None ):
        this_api = self.api()
        if this_api is not None:
            try:
                return this_api.update_status( status=status, in_reply_to_status_id=in_reply_to_status_id )
            except tweepy.error.TweepError as e:
                logging.exception( e )

    def mentions( self, since_id=None ):
        this_api = self.api()
        return this_api.mentions_timeline( since_id=since_id )

    def self_username( self ):
        this_api = self.api()
        return this_api.me().screen_name