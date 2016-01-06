import glob
import logging
import logging.handlers
import sys
#http://pymotw.com/2/logging/
#https://docs.python.org/2/howto/logging-cookbook.html

username=''
LOG_PATH = '/home/'+username+'/bin/logs/'

llevel=logging.DEBUG

#create logger
def create(logname):
	global llevel
	LOG_FILENAME= LOG_PATH + logname + '.out'
	logging.basicConfig(filename=LOG_FILENAME,
						level=llevel,
						format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
						datefmt='%m-%d %H:%M'
						)



def dunno():					
	f = open(LOG_FILENAME, 'rt')
	try:
		body = f.read()
	finally:
		f.close()

	print 'FILE:'
	print body


LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)

def testlog():	
	logging.debug('This is a debug message')
	logging.info('This is an info message')
	logging.warning('This is a warning message')
	logging.error('This is an error message')
	logging.critical('This is a critical error message')
	


def verbose(var):
    global llevel
    if var:
        llevel=logging.DEBUG
    else :
        llevel=logging.WARNING
