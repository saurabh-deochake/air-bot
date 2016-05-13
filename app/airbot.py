#!/bin/python

"""
The MIT License (MIT)

Copyright (c) 2016 Saurabh Deochake

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import time
import __future__
import logging
import tweepy
from ConfigParser import SafeConfigParser
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

CONFIG_FILE = "/etc/airbot.conf"


def auth():
	parser = SafeConfigParser()
	parser.read(CONFIG_FILE)

	ckey = parser.get('twitter','ckey')
	csecret = parser.get('twitter','csecret')
	atoken = parser.get('twitter','atoken')
	asecret = parser.get('twitter', 'asecret')

	# Create authentication token using our details
	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	api = tweepy.API(auth)
	twitterStream = Stream(auth, streamer())	
	twitterStream.filter(track=["#airqualityin"]) 


class streamer(StreamListener):
	def on_data(self, data):
		try:
			userName = data.split(',"screen_name":"')[1].split('","location')[0]
			tweet = data.split(',"text":"')[1].split('","source')[0]
			print tweet[tweet.index("#airqualityin")+1:]

			#print data

			fetchedTweet = "@"+userName+"-"+tweet
			#print fetchedTweet
			time.sleep(5)
			return True

		except BaseException, e:
			print 'Failed Ondata,', str(e)
			time.sleep(5)
		except KeyboardInterrupt, k:
			print 'Keyboard Interrupt Occured,',str(k)
			quit()

	def on_error(self, status):
		print status

	'''
	def update(self, api):
		print "update"
		#api.update_status('Airbot says hi! It\'s %s' % (time.strftime("%H:%M:%S")))
	'''
	
if __name__ == "__main__":
	auth()


