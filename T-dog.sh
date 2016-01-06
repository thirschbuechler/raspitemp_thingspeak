#!/bin/bash
#T-dog.sh
#make-run.sh
#make sure a process is always running.

export DISPLAY=:0 #needed if you are running a simple gui app.

process=ds18b20
username=""
makerun="sudo python /home/"+username+"/bin/ds18b20.py"

if ps ax | grep -v grep | grep $process > /dev/null
        then
                exit
        else
	        $makerun &
#		echo "ds18b20.py got (re)started" | mailx -s 'Thingspeak restarted' mail@mail.com
#		echo $(date) "ds18b20.py (re)started" >> /logpath/logfile.txt
        fi
exit
