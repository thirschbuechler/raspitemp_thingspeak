# base by: Joshwa, Brickpi
#modified by t.hirschbuechler

from __future__ import division #make division accurate

import httplib, urllib
import time
import math
import ds18b20_raw
import log

#how many sensors
sensnumb = 5
# use your API key generated in the thingspeak channels for the value of 'key'
apikey=''


#i use 5 sensors, so i initialize 0 to 4
fails = [0 for x in range(sensnumb)]
fails[0]=0
fails[1]=0
fails[2]=0
fails[3]=0
fails[4]=0

#left side: sensors as listed in in ".._raw"-file
#right side: thingspeak field no.
sensors = [0 for x in range(sensnumb)]
sensors[0]=1
sensors[1]=2
sensors[2]=5 
sensors[3]=4
sensors[4]=6
#sensors[i]=$fieldNR



log.verbose(False)
log.create('ds18b20') 
log.logging.warning('----Start-----') 

def thermometer(i=0):
			log.logging.info('%d: reading sensor..'%(i+1))
			strg=" "
			temp=ds18b20_raw.read_temp(i)
			if temp > 60:
				temp=temp/0 #raise an exception and don't upload that bullshit
			temp=temp*10
			temp=int(temp)
			temp=temp/10 #division!
			#strg="field%i" %(i+1)
			strg="field%i" %sensors[i]
			log.logging.info('sensor %i'%(i+1)+' will update '+strg+' with temp:  %d C'%temp)
	                params = urllib.urlencode({strg: temp, 'key':apikey})    

 # temp is the data you will be sending to the thingspeak channel for plotting the graph. You can add more than one channel and plot more graphs
                 	headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
                 	conn = httplib.HTTPConnection("api.thingspeak.com:80")                
                        try:
                                conn.request("POST", "/update", params, headers)
                                response = conn.getresponse()
				log.logging.info('HTTP upload: '+response.reason)
                               # print response.status, response.reason
                                data = response.read()
                                conn.close()
                        except:
				log.logging.warning("HTTP Upload failed (miserably)")

#sleep for 16 seconds (api limit of 15 secs)
if __name__ == "__main__":
        while True:
		for x in range (0, sensnumb):
	                try:
				thermometer(x)#to catch exception if one is NC
				if fails[x]>0:
                    			fails[x]=0
					log.logging.warning('%d: back in business!'%(x+1))
				time.sleep(16)				
			except:
		                if fails[x]==2:
					log.logging.warning('%d: continous error, no more logging'%(x+1))
                		elif fails[x]<2:
					log.logging.warning('%d: failed to read'%(x+1))

				time.sleep(2)
				fails[x]=fails[x]+1
				#print 'failed to read nr. ',x+1
				pass
