import confighandler
import oauthclient
import time
import twitterconnector
import os
import logging
import platformutils


class BotKit( object ):

    def __init__( self, bot_name ):
        self._bot_name = bot_name

    def run( self, generator ):

        # init logging
        platformutils.init_logging()

        # init config, get twitter creds
        pth_root = os.path.expanduser( "~/.botkit" )
        pth_root = os.path.join( pth_root, self._bot_name )
        if not os.path.exists( pth_root ):
            os.makedirs( pth_root )
        config = confighandler.ConfigHandler( pth_root=pth_root )

        # twitter connector & tweet generator
        consumer_token = config.twitter_consumer_token()
        access_token = config.twitter_access_token()

        # start web UI if enabled
        if config.oauth_enabled():
            logging.info( "Start oauth interface..." )
            # handler for token save from oauth web UI
            def save_access_token( token, token_secret ):
                global access_token
                logging.info( "Token received, saving...")
                config.save_twitter_access_token( token=token, secret=token_secret )
                access_token = [ token, token_secret ]
            # init oauth web UI
            oauth = oauthclient.WebInterface( api_key=consumer_token[0],
                api_secret=consumer_token[1], save_token_callback=save_access_token )
            oauth.start()

        try:
            # main runloop
            ## default to 3 hours between tweets
            TWEET_INTERVAL = config.tweet_interval( default_value=10800 )
            RUNNING = True
            logging.info( "Enter main runloop..." )
            while RUNNING:
                logging.info( "Main runloop tick...")
                if (access_token is not None) and (consumer_token is not None):
                    logging.info( "Token set, will tweet..." )
                    connector = twitterconnector.TwitterConnector(
                        consumer_key=consumer_token[0], consumer_secret=consumer_token[1],
                        access_key=access_token[0], access_secret=access_token[1]
                    )
                    tweet = None
                    try:
                        tweet = generator.generate()
                    except Exception:
                        pass
                    if tweet and (len(tweet)>1):
                        logging.info( tweet )
                        connector.tweet( tweet )
                else:
                    logging.info( "No token set, doing nothing..." )
                time.sleep( TWEET_INTERVAL ) 
        except KeyboardInterrupt:
            pass

        # close down web UI on exit
        if config.oauth_enabled():
            oauth.stop()