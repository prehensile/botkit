# botkit

* Version 0.1 (March 2015)
* Author: Henry Cooke, me@prehensile.co.uk

## Overview 

`botkit` is a toolkit for the creation of Twitter bots, written in Python. It is intended to take care of the tricky and annoying stuff (like obtaining OAuth tokens and scheduling tweets) so you can

## Configuration 
`botkit` is configured with a few environment variables:

* `TWITTER_CONSUMER_KEY`: a Twitter app key
* `TWITTER_CONSUMER_SECRET`: a Twitter app key secret
* `TWEET_INTERVAL`: time between tweets, in seconds. Optional, defaults to 3 hours (3600).
* `OAUTH_ENABLED`: if True (or yes, or 1), botkit will run a web interface for obtaining oauth keys.

## Example projects
Two sample bot projects are available that use `botkit`:

* [asciibot][1], which tweets random lines from [textfiles.com][2].
* [ragebot][3], which tweets lines from Dylan Thomas's poem [*Do not go gentle into that good night*][4].

## Roadmap

### Version 0.2

* More flexible tweet timing options
* More extensive documentation & commenting

[1]: https://github.com/prehensile/asciibot
[2]: http://www.textfiles.com/
[3]: https://github.com/prehensile/ragebot
[4]: http://www.poets.org/poetsorg/poem/do-not-go-gentle-good-night
