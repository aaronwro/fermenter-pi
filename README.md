fermenter-pi
============

python script that monitors a digital temperature sensor connected over i2c and controls a heater connected via a GPIO switched power outlet. 

Setup Info
----------
Start with [necessary packages][packages] and [COSM Account and Feed][cosm-setup], then modify the _sample-config.json_ file to 

Bill of Materials
-----------------
* raspberry pi model b
* [Powerswitch Tail II][powerswitch]
* [Sparkfun DS18B20 Waterproof Temperature Sensor][ds18b20]
* [Electric Fermentation Heater][heater]

Acknowledgements
-----------------
I was only able to acheive this result with the help of resources including but not limited to:
* [http://learn.adafruit.com/category/raspberry-pi][adafruit-learn]
* [http://www.raspberrypi.org/][raspberrypi]
* [http://docs.python.org/2.7/][python-docs]

[packages]: http://learn.adafruit.com/send-raspberry-pi-data-to-cosm/necessary-packages "Adafruit Learning System: Send Raspberry Pi Data to COSM - COSM Account and Feed"
[cosm-setup]: http://learn.adafruit.com/send-raspberry-pi-data-to-cosm/cosm-account-and-feed "Adafruit Learning System: Send Raspberry Pi Data to COSM - Necessary Packages"
[heater]: http://www.northernbrewer.com/shop/electric-fermentation-heater.html "Electric Fermentation Heater @ Northern Brewer"
[ds18b20]: http://www.abra-electronics.com/products/SEN%252d11050-Temperature-Sensor-%252d-Waterproof-%28DS18B20%29.html "Sparkfun DS18B20 Waterproof Temperature Sensor @ ABRA Electronics"
[powerswitch]: http://www.abra-electronics.com/products/COM%252d10747-PowerSwitch-Tail-II.html "PowerSwitch Tail II @ ABRA Electronics"
[adafruit-learn]: http://learn.adafruit.com/category/raspberry-pi "Adafruit Learning System - Raspberry Pi"
[raspberrypi]: http://www.raspberrypi.org/ "Raspberry Pi"
[python-docs]: http://docs.python.org/2.7/ "Python v2.7.3 documentation"