import os 
import logging

class ConfigHandler( object ):

    def __init__( self, pth_root=None ):
        self._pth_root = pth_root

    def parse_boolean( self, var=None ):
        ret = False
        if var is not None:
            try:
                ret = (int(var) != 0)
            except ValueError:
                pass 
            if not ret:
                if (var.lower() != "false") and \
                    (var.lower() != "no"):
                    ret = True
        return ret

    def path_for_resource( self, fn_resource=None ):
        return os.path.join( self._pth_root, fn_resource )

    def save_twitter_access_token( self, token=None, secret=None ):
        pth_creds = self.path_for_resource( "twitter_creds" )
        fh_creds = open( pth_creds, "w" )
        fh_creds.write( "%s\n%s" % (token,secret) )
        fh_creds.close()

    def twitter_access_token( self ):
        ret = None
        pth_creds = self.path_for_resource( "twitter_creds" )
        if os.path.exists( pth_creds ):
            fh_creds = open( pth_creds )
            lines = fh_creds.readlines()
            fh_creds.close()
            ret = []
            for line in lines:
                ret.append( line.rstrip() )
        return ret

    def twitter_consumer_token( self ):
        token = os.environ.get( "TWITTER_CONSUMER_KEY" )
        secret = os.environ.get( "TWITTER_CONSUMER_SECRET" )
        if (token is not None) and (secret is not None):
            return( token, secret )
        return None

    def tweet_interval( self, default_value=3600 ):
        e = os.environ.get( "TWEET_INTERVAL" )
        if e is not None:
            interval = float(e)
        else:
            interval = default_value
        return interval

    def oauth_enabled( self ):
        e = os.environ.get( "OAUTH_ENABLED" )
        enabled = self.parse_boolean( e )
        return enabled


