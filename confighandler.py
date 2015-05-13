import os 
import logging

TWITTER_ACCESS_TOKEN_KEY = "TWITTER_ACCESS_TOKEN"

class ConfigHandler( object ):

    def __init__( self, pth_root=None, persist_twitter_credentials_to_file=False ):
        self._pth_root = pth_root
        self._persist_twitter_credentials_to_file = persist_twitter_credentials_to_file

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
        lines_out = "%s\n%s" % (token,secret)
        logging.info( "save token: %s" % lines_out )
        if self._persist_twitter_credentials_to_file:
            pth_creds = self.path_for_resource( "twitter_creds" )
            fh_creds = open( pth_creds, "w" )
            fh_creds.write( lines_out )
            fh_creds.close()
        os.environ[ TWITTER_ACCESS_TOKEN_KEY ] = lines_out

    def twitter_access_token( self ):
        """
        Load Twitter access token. Try environment variables first, then disk.
        """
        lines = os.environ.get( TWITTER_ACCESS_TOKEN_KEY )
        if lines is not None:
            # lines were in environment, prepare for parsing
            lines = lines.decode('string_escape')
            lines = lines.split("\n")
        else:
            # lines weren't in environment, try reading from disk
            pth_creds = self.path_for_resource( "twitter_creds" )
            if os.path.exists( pth_creds ):
                fh_creds = open( pth_creds )
                lines = fh_creds.readlines()
                fh_creds.close()
        # parse & tidy lines to list & return
        ret = None
        if lines:
            logging.info( "twitter_access_token loaded: %s" % lines )
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


