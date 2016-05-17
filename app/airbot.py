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
import ssl
import tweepy
import utm
from bs4 import BeautifulSoup
from urllib import urlopen
from ConfigParser import SafeConfigParser
from geopy.geocoders import Nominatim
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
	akey = parser.get('breezometer', 'akey')

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
			city = tweet[tweet.index("#airqualityin")+(len("#airqualityin")+1):]
			print tweet
			print city
			latitude, longitude = self.get_latlon(city)
			print latitude
			print longitude
			self.get_aqi(latitude, longitude)
			# 1) get lattitude and longitude from the city
			# 2) pass the lattitude and longitude to get_aqi

			#fetchedTweet = "@"+userName+"-"+tweet
			#call parse_aqi here
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
	def get_latlon(self, city):
		geolocator = Nominatim()
		location = geolocator.geocode(city)
		latitude, longitude = location.latitude, location.longitude
		return latitude, longitude

	def get_aqi(self, latitude, longitude):
		parser = SafeConfigParser()
		parser.read(CONFIG_FILE)
		akey = parser.get('breezometer', 'akey')
		print akey
		context = ssl._create_unverified_context()
		optionsUrl = 'http://api.breezometer.com/baqi/?lat={latitude}&lon={longitude}&key='+akey
		optionsPage = urlopen(optionsUrl, context=context).read()
		print optionsPage

if __name__ == "__main__":
	auth()


