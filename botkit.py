import confighandler
import oauthclient
import time
import twitterconnector
import os
import logging
import platformutils
import utils


class BotKit( object ):


    def __init__( self, bot_name, debug_mode=False, tweet_interval=10800,
                    last_mention_id=None, reply_direct_only=True ):
        self._bot_name = bot_name
        self._last_mention_id = last_mention_id
        self._debug_mode = debug_mode
        self._default_interval = tweet_interval
        self._reply_direct_only = reply_direct_only


    def do_replies( self, connector, generator ):
        mentions = None
        if self._last_mention_id is not None:
            mentions = connector.mentions( since_id=self._last_mention_id )
        else:
            mentions = connector.mentions()
        
        last_id = self._last_mention_id
        for mention in mentions:
            mention_body = mention.text
            process_mention = True
            
            if self._reply_direct_only:
                self_username = connector.self_username()
                process_mention = mention_body.startswith( "@%s" % self_username )
            
            if process_mention:
                # strip @usernames from beginning of replies
                if mention_body.startswith( "@" ):
                    mention_body = mention_body[mention_body.index(" ")+1:].lstrip()
                
                try:
                    tweet = generator.reply(
                        mention_body,
                        to_username=mention.author.screen_name,
                        to_userid=mention.author.id_str
                    )
                    self.do_tweet(
                        connector,
                        tweet,
                        to_username=mention.author.screen_name,
                        in_reply_to_status_id=mention.id_str
                    )
                    if (last_id is None) or (mention.id > last_id):
                        last_id = mention.id
                except Exception as e:
                    logging.exception( e )

        self._last_mention_id = last_id


    def do_tweet( self, connector, tweet, to_username=None, in_reply_to_status_id=None ):
        
        if tweet is None:
            return
        
        if self._debug_mode:
            logging.info( "do_tweet DEBUG MODE, would tweet: %s" % tweet )
        
        elif tweet and (len(tweet)>1):
            logging.info( tweet )
            prefix = None
            chunk_length = 140
            if to_username:
                prefix = "@%s " % to_username
                chunk_length -= len(prefix)
            chunks = utils.chunk_string( tweet, chunk_length )
            reply_to_status_id = in_reply_to_status_id
            for chunk in chunks:
                if prefix is not None:
                    chunk = "%s%s" % (prefix, chunk)
                new_status = connector.tweet(
                    chunk,
                    in_reply_to_status_id=reply_to_status_id
                )
                reply_to_status_id = new_status.id_str


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

        # start web UI if enabled
        if config.oauth_enabled():
            logging.info( "Start oauth interface..." )
            # handler for token save from oauth web UI
            def save_access_token( token, token_secret ):
                global access_token
                logging.info( "Token received, saving...")
                config.save_twitter_access_token(
                    token=token,
                    secret=token_secret
                )
            # init oauth web UI
            oauth = oauthclient.WebInterface(
                api_key=consumer_token[0],
                api_secret=consumer_token[1], 
                save_token_callback=save_access_token
            )
            oauth.start()

        try:
            # main runloop
            TWEET_INTERVAL = config.tweet_interval(
                default_value=self._default_interval
            )
            RUNNING = True
            logging.info( "Enter main runloop..." )
            while RUNNING:
                logging.info( "Main runloop tick...")
                
                # reload access token in case it's changed
                access_token = config.twitter_access_token()
                
                if (access_token is not None) and (consumer_token is not None):
                    logging.info( "Token set, will tweet..." )
                    
                    # set up a twitter connector
                    connector = twitterconnector.TwitterConnector(
                        consumer_key=consumer_token[0],
                        consumer_secret=consumer_token[1],
                        access_key=access_token[0],
                        access_secret=access_token[1]
                    )
                    
                    try:
                        # generate standalone tweet
                        tweet = None
                        try:
                            tweet = generator.generate()
                        except Exception as e:
                            logging.exception( e )
                        self.do_tweet( connector, tweet )

                        # do replies
                        self.do_replies( connector, generator )
                        
                    except Exception as e:
                        logging.exception( e )

                    # sleep for TWEET_INTERVAL, potentially a long time
                    logging.info( "Sleeping for %d seconds..." % TWEET_INTERVAL )
                    time.sleep( TWEET_INTERVAL )
                
                else:
                    logging.debug( "No token set, doing nothing..." )
                    logging.debug(
                        "-> access_token: %s, consumer_token: %s",
                        access_token,
                        consumer_token
                    )
                    # sleep for a short period, waiting for token
                    time.sleep( 1 )

        except KeyboardInterrupt:
            pass

        # close down web UI on exit
        if config.oauth_enabled():
            oauth.stop()