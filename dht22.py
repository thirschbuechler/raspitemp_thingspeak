#!/usr/bin/env python
from __future__ import with_statement # Required in 2.5

import os
import re
import subprocess
import time
import datetime
import httplib
import urllib
import sys

#custom logging
import log

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out!"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


        

#put username here
username=""    
#CHANGE THE KEY
API_KEY = "" 


#change this if you have more sensors, on SPI afaik you can only have one anyway
#nevertheless, i used two via gpio method, but that ran very unstable, unfortunately
sensnumb=1

#this simply prevents the logfile from getting a mess, and stops logging after that many errors
#(but tells that it does so in the log)
howmanyfails=5

#new = don't use adafruit script for dht22 if true
new = True

#sensorwait
swait=5
#api-limit of thingspeak = 16s, apiwait = 16-swait because it only needs 16 in total
apiwait=16-swait


#debug: sensor values
#info: 
#warning: ranged, spikefree
#error: try-except
#critical: timeout on non-adafruit sensor



Nodes = [[0 for x in range(5)] for x in range(sensnumb)]#the definition order is in reverse to its latter use
#1D: sensor number 
#2D: sensortype, port, field-name temp, field-name hum, fail-variable


#Sensor one
Nodes[0][0]="22"
Nodes[0][1]="SPI"#17
Nodes[0][2]="field1"
Nodes[0][3]="field2"
Nodes[0][4]=0

#Sensor two
#Nodes[1][0]="22"
#Nodes[1][1]="SPI"#18
#Nodes[1][2]="field3"
#Nodes[1][3]="field4"
#Nodes[1][4]=0

#to exclude bogus values if detected
def failstate():
    global temperature, humidity
    temperature = -50
    humidity = -50

#init
failstate()
log.verbose(False)
log.create('dht22')
log.logging.warning('----Start-----')

#spikefree() init values
lasttemp=100
lasthum=100



# Run the DHT program to get the humidity and temperature readings!
def read_dht(node):
    global temperature, humidity
    processread=False
    #stabilize input, then..
    time.sleep(swait)
    log.logging.debug("node %d: reading" %node)
    try:
        with time_limit(20):
	    if not new:
                output = subprocess.check_output(["/usr/bin/Adafruit_DHT", Nodes[node][0], Nodes[node][1]]);
	    else:
                output = subprocess.check_output(["/home/"+username"/bin/foxg20/dhtlib/example/dhtsensor", "DHT"+Nodes[node][0], Nodes[node][1]]);

    	    log.logging.debug("node %d: is read in" %node)
	    processread=True	
	
            if not new:
		matches = re.search("Temp =\s+([0-9.]+)", output)
	    else:
		matches = re.search("Temperature:   +([0-9.]+)", output)
            if (matches):
                temperature = float(matches.group(1))
            else:
                log.logging.debug('no temp match, raw output was:')
		log.logging.debug(output)
                failstate()


            if not new:
	        matches = re.search("Hum =\s+([0-9.]+)", output)
	    else:
	        matches = re.search("Humidity: +([0-9.]+)", output)
		
            if (matches):
                humidity = float(matches.group(1))
            else:
                log.logging.debug('no hum match, raw output was:')
		log.logging.debug(output)
                failstate()

	    if new and temperature==-50:
	        matches = re.search("+TIMEOUT+", output)
		if matches:
			log.logging.critical(output)
		       
        #return True
                
    except:
        failstate()
	#only debug, because it may be re-read and therefore be no problem
	if processread:
	        log.logging.debug("node %d: exception by  matches" %node)
	else:
	        log.logging.debug("node %d: exception: sensorreader or timeout" %node)

        #return False
    finally:
        log.logging.debug( "node %d"%node + " reads %.1f C" %temperature + " and %.1f percent" %humidity)
#end read


#babysit sensor values
def ranged():
    global temperature, humidity
    retval = False
    
    if temperature>-50:
        if temperature <60:
            if humidity<100:
                if humidity>0:
                    retval = True
    if not retval: log.logging.info('ranged returns false')
    return retval
#end ranged	


def spikefree():
    global temperature, humidity, lasttemp, lasthum
    retval = True
    #posotive spikes?
    if temperature>lasttemp+10:
        retval = False
    if humidity>lasthum+20:
        retval = False
    
    #also look for negative spikes, after first run
    if lasttemp < 100:
        if temperature<lasttemp-10:
            retval = False
        if humidity<lasthum-10:
            retval = False
    #now remember last values for next time
    #make sure to skip the -50 init values
    if temperature>-50:
        lasttemp=temperature
        lasthum=humidity
    if not retval: log.logging.info('spikefree returns false')
    return retval
#end spikefree

def check(node):
    global howmanyfails
    read_dht(node)
    
    if Nodes[node][4]>(howmanyfails-1):
        if ranged() and spikefree():
            Nodes[node][4]=0#he redeemed himself
            log.logging.error('node %d: back in business!'%node)
            return True
        else:
            if Nodes[node][4]==howmanyfails:
                log.logging.error('node %d: continuous error, no more logging'%node)
		Nodes[node][4]=howmanyfails+1
            return False
#(and don't continue)

    if not ranged():
        read_dht(node)

    if not spikefree():
         read_dht(node)

    if ranged() and spikefree():
        Nodes[node][4]=0#past sins forgiven, always less than 3 so no redeem text log
        return True
    else:
        log.logging.error('node %d: no update (re-reading failed)'%node)
        Nodes[node][4]=Nodes[node][4]+1
        return False
#end check
        
        
def send(node):
      global temperature, humidity
      log.logging.debug( "node %d"%node + " gets updated with %.1f C" %temperature + " and %.1f percent" %humidity)
        
      params = urllib.urlencode({Nodes[node][2]: temperature, Nodes[node][3]: humidity})
      headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    
      # This way it doesn't blow
      try:
          conn = httplib.HTTPConnection("api.thingspeak.com:80")
          conn.request("POST", "/update?key="+ API_KEY, params, headers) 
          response = conn.getresponse()
          data = response.read()
          conn.close()
      except:
        log.logging.error('node %d: HTTP Error'%node)
      finally:
        log.logging.debug("node %d: HTTP: "%node + response.reason)# + " response code :%d" response.status)
              
      return True
#end send
      
def run():
    while True:
	for i in range(0,sensnumb):
	        if check(i):
	            send(i)
	            time.sleep(apiwait)
#        if check(1):
#            send(1)
#            time.sleep(apiwait)


run()

