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
import json
from bs4 import BeautifulSoup
from urllib import urlopen
from ConfigParser import SafeConfigParser
from geopy.geocoders import Nominatim
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

CONFIG_FILE = "/etc/airbot.conf"
ERROR_TWEET = "@%s, to get air quality in your city, please tweet \"#airqualityin followed by city name (US only).\""
UNSUPPORTED_ERROR = "@%s, Provided location is not yet supported! Please enter US city name!"
NODATAAVAILABLE_ERROR = "@%s, Air quality data is not available currently. Please check back in some time!"

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


class streamer(StreamListener):
	def start_stream(self):
		
		twitterStream = Stream(auth, streamer())	
		twitterStream.filter(track=["#airqualityin"]) 


	def on_data(self, data):
		try:
			userName = data.split(',"screen_name":"')[1].split('","location')[0]
			tweet = data.split(',"text":"')[1].split('","source')[0]
			city = tweet[tweet.index("#airqualityin")+(len("#airqualityin")+1):]
			print tweet
			print city
			latitude, longitude = self.get_latlon(city)
			
			if latitude != -1 and longitude != -1:
				print latitude
				print longitude
				aqi, quality = self.get_aqi(latitude, longitude)
				self.on_update(userName, city, aqi, quality)
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
		return False
	
	def on_update(self, userName, city, aqi, quality):
		print "update"

		if aqi == -1 and quality == UNSUPPORTED_ERROR:
			api.update_status(UNSUPPORTED_ERROR % (userName))
		elif aqi == -1 and quality == NODATAAVAILABLE_ERROR:
			api.update_status(NODATAAVAILABLE_ERROR % (userName))
		else:

			print '@'+userName+' ,Current Air Quality in '+city+' is '+str(aqi)+ ' !'
			api.update_status('@'+userName+', Air Quality in '+city+' is '+ quality.split()[0].lower()+ ' with index '+str(aqi)+ '. (via @BreezoMeter)')

	def on_limit(self, track):
		print track

	def on_timeout(self):
		print "Timeout, sleeping for 60 seconds...\n"
		time.sleep(60)
		return 
	
	def get_latlon(self, city):
		try:
			geolocator = Nominatim()
			location = geolocator.geocode(city)
			latitude, longitude = location.latitude, location.longitude
			return latitude, longitude
		except: 
			return -1, -1


	def get_aqi(self, latitude, longitude):
		
		try:
			parser = SafeConfigParser()
			parser.read(CONFIG_FILE)
			akey = parser.get('breezometer', 'akey')
		except FileNotFoundError, e:
			print "Config file not found! Aborting..."
			print "Trace: ",str(e)

		try:
			context = ssl._create_unverified_context()

			optionsUrl = 'http://api.breezometer.com/baqi/?lat='+str(latitude)+'&lon='+str(longitude)+'&key='+akey

			print optionsUrl

			optionsPage = urlopen(optionsUrl, context=context).read()
			aqi_json = json.loads(optionsPage)
			
			print aqi_json['error']['code']

			if aqi_json['error']['code'] == 20: 
				return -1, UNSUPPORTED_ERROR
			elif aqi_json['error']['code'] == 21:
				return -1, NODATAAVAILABLE_ERROR
			else:
				return aqi_json['breezometer_aqi'], aqi_json['breezometer_description']
		except BaseException, e:
			print str(e)

if __name__ == "__main__":
	stream = streamer()
	stream.start_stream()


