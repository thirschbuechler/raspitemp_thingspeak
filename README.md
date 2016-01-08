# raspitemp_thingspeak
my hacked way to get temperature measurements from a Raspberrypi to a Webgui via Thingspeak and Python. It is kinda a Sensorstation or Weatherstation, tough no forcasts are made. 

I uploaded the scripts and did my best to explain the basics, but at the end of the day this will remain a hack and be anything but a full-fledged product. It is almost literally held together by duct-tape, but it works. Most of the time.
A demo of the webinterface is provided as well.

However, i didn't come up with all of this, so i'll try to properly link every project i used stuff from. Many thanks to those guys, should they ever read these lines;)

Used hardware: a Raspberry B+ (though you don't need the extra pins for this), many cheap ds18b20 temperature sensors and one DHT22 t+humidity sensor.


Projects/Sites i borrowed stuff from or interface with:

adafruit.com, http://www.dexterindustries.com/BrickPi/projects/thingspeak-temperature-log/,
https://github.com/ondrej1024/foxg20,
http://pymotw.com/2/logging/,
https://docs.python.org/2/howto/logging-cookbook.html,
http://www.free-css.com/free-css-templates/page179/base-2013,
Highstock-charts via http://forum.arduino.cc/index.php?topic=213058.0 (basic version, not the one from github),
Thingspeak and Iobridge
