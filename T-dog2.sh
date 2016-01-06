#!/bin/bash
#T-dog2.sh
#make-run.sh
#make sure a process is always running.

export DISPLAY=:0 #needed if you are running a simple gui app.

process=dht22
username=""
makerun="sudo python /home/"+username+"/bin/dht22.py"

if ps ax | grep -v grep | grep $process > /dev/null
        then
                exit
        else
        	$makerun &
#		echo "dht22 got (re)started" | mailx -s 'dht22 restarted' mail@mail.com
#		echo $(date) "dht22 got (re)started" >> /logpath/logfile.txt
        fi
exit
