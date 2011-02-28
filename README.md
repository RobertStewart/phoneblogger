PhoneBlogger
================
[Project site](http://wombatnation.com/phoneblogger)

[Source code on GitHub](http://github.com/RobertStewart/phoneblogger)

# Description
PhoneBlogger is an application for blogging and tweeting by phone. The original implementation, which is [hosted on Sourceforge](http://sourceforge.net/projects/phoneblogger/), supported only blogging. The new version currently supports only tweeting, but blogging support is on it's way. People still blog, right?

PhoneBlogger runs on Google App Engine and uses the Tweepy library to update your Twitter status. You call your app via Twilio. The goog.gl URL is shortener is used to shorten the rather long Twilio recording URLs.

# Author
Robert Stewart (robert@wombatnation.com)

# Pre-requisites
* Twitter application account
* Google App Engine account
* Twilio account
* Tweepy

The current implementation is in [Python](http://python.org), but I'm planning to add a [Scala](http://scala-lang.org/) implementation. For now, you need to have Python installed.

# Installation / Configuration

## Twitter
After logging into your Twitter account on the web, [register an application](https://dev.twitter.com/apps/new). While it would be relatively simple to extend the phoneblogger code to support tweeting to different accounts, it currently just tweets to one account. So, register the app while logged into the Twitter account you want the tweets to go to.

* Enter an Application Name. Keep trying, because the best choices are already taken.
* Leave Application Type set to Browser.
* Change Default Access Type to Read & Write.
* Enter the CAPTCHA and click Register Application.

## Tweepy
Tweepy is an awesome [Twitter API library for Python](http://joshthecoder.github.com/tweepy/). PhoneBlogger includes a copy of Tweepy.

Go to your [Twitter apps page](https://dev.twitter.com/apps) and note the Consumer Key and Consumer Secret on this page. You will need to use them with Tweepy to get an Access Key and Access Secret for your account.

Create a file named auth.py with the following contents:

	import tweepy

	CONSUMER_KEY = 'consumerkey'
	CONSUMER_SECRET = 'consumersecret'

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth_url = auth.get_authorization_url()
	print 'Please authorize: ' + auth_url
	verifier = raw_input('PIN: ').strip()
	auth.get_access_token(verifier)
	print "ACCESS_KEY = '%s'" % auth.access_token.key
	print "ACCESS_SECRET = '%s'" % auth.access_token.secret
	
Replace consumerkey and consumersecret with the values from your Twitter apps page. Run the script:

	$ python auth.py
	
It will print out 'Please authorize: ' followed by a URL. Go to that URL in a browser and grant your Twitter app access to your account. A PIN will appear. Then, return to the shell window and enter the PIN.
	
Now create a file called auth_step2.py with the following contents:

	import sys
	import tweepy

	CONSUMER_KEY = 'consumerkey'
	CONSUMER_SECRET = 'consumersecret'
	ACCESS_KEY = 'accesskey'
	ACCESS_SECRET = 'accesssecret'

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	api.update_status("test")

Once again, replace consumerkey and consumersecret with the values from your Twitter apps page. Also replace accesskey and accesssecret with the values returned by auth.py. Run the script:

	$ python auth2.py
	
If all goes well, you will see a new tweet in your timeline with the text "test".

## Google App Engine
Unless you already have an AppEngine account, follow the ["Getting Started" instructions on the App Engine website](http://code.google.com/appengine/). After you've downloaded the Python SDK:

* Go to https://appengine.google.com/
* Click Create Application
* Enter an application identifier. You will later enter the full URL in your Twilio account as the Voice URL and in a PhoneBlogger config file.

Run GoogleAppEngine Launcher:

* From the File menu, choose New Application...
* Browse to phoneblogger/python/src
* Click Add

## Twilio
Register for a [Twilio](http://www.twilio.com/) developer account. You get $25 of credit when registering. At 1 penny per minute for an inbound call you can make quite a few calls for free.

On your account page:

* Update the Voice URL to your Google App Engine app URL

## PhoneBlogger
Edit app.yaml:

* Change the value for 'application:' to your AppEngine app identifier.

Edit config.py:

* Change BASE_URL to your AppEngine app URL. This is the same URL you entered as the Twilio Voice URL.

Rename empty_auth_config.py to auth_config.py and then edit it:

* Replace values for CONSUMER\_KEY, CONSUMER\_SECRET, ACCESS\_KEY and ACCESS\_SECRET with the values above from the Tweepy section.

## Final Steps
Return to GoogleAppEngineLauncher, select your app and click Deploy. Once it finishes deploying, make a test call to your Twilio number and enter your Twilio developer account PIN.