#DS18B20 Sensor handling software, from adafruit.com
import os, glob, time, subprocess
#for cmd line handling
import sys, getopt



#setup bus 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

#put your device's serial adresses here, goto i.e. adafruit.com for instructions on how to get them
devices = ['28-000006000000','28-000006000000','28-000006000000','28-000006000000','28-000006000000']
#remember, the number of devices has to be updated in ds18b20.py as well!

#(used this safe version before even testing the volatile first)
def read_temp_raw(num):
	device_folder = glob.glob(base_dir + devices[num])[0]
	device_file = device_folder + '/w1_slave'
	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines
	
def read_temp(num):
    lines = read_temp_raw(num)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
	return temp_c
