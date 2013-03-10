#!/usr/bin/env python

import time
import os
import eeml
import RPi.GPIO as GPIO
from datetime import datetime
from sys import exit
import math
import json

CONFIG_FILE = 'config-sample.json'

# default config
COSM_API_URL_BASE = '/v2/feeds/{feednum}.xml'
COSM_API_FEED = 'YYYYYY'
COSM_ENABLED = False
COSM_STRING_TEMP_C_DATA = 'MeasuredTempDegC'
COSM_STRING_TARGET_TEMP_DATA = 'TargetTempDegC'
COSM_STRING_HEATER_IS_ON_DATA = 'HeaterIsOn'
COSM_STRING_TEMP_PERCENT_DIFF_DATA = 'Measured-TargetPercentDifference'
DEBUG = True
FERMENTORTHERMOMETER ='/sys/bus/w1/devices/28-000002aac1bd/w1_slave'
HEATER_GPIO_PIN = 24
LED_GPIO_PIN = 25
LOGFILE = '/home/webide/repositories/my-pi-projects/Fermentor/fermentor.log'
MEASUREMENT_INTERVAL_SEC = 10
TARGET_TEMP_C = 19.0

def log(message):
    logStr = '{time}: {str}'.format(time = datetime.now(), str = message)
    with open(LOGFILE, 'a') as f:
        f.write(logStr + '\n')
    if DEBUG:
        print logStr

def loadConfig(config_filename):
    log('--- Loading config from file "{file}"...'.format(file = config_filename))
    with open(config_filename) as json_config_file:
        try:
            json_config = json.load(json_config_file)
            for k,v in json_config.items():
                log('------ setting {key} = {value}'.format(key = k, value = v))
            globals().update(json_config)
            log('--- Finished updating config.')
        except Exception as e:
            print 'Exception reading config file "{file}":\n {ex}'.format(file = config_filename, ex = e)

def setupGPIO():
    log("Setting up GPIO")
    GPIO.setmode(GPIO.BCM)
    log('Setting up Heater on GPIO {HEATER_GPIO_PIN}'.format(HEATER_GPIO_PIN = HEATER_GPIO_PIN))
    GPIO.setup(HEATER_GPIO_PIN, GPIO.OUT)
    #print 'Setting up LED on GPIO {LED_GPIO_PIN}'.format(LED_GPIO_PIN = LED_GPIO_PIN)
    #GPIO.setup(LED_GPIO_PIN, GPIO.OUT)

def getTemperature(thermometer):
    try:
        tfile = open(thermometer)
        text = tfile.read()
        tfile.close()
        lines = text.split('\n')
        line1split = lines[0].split(' ')
        crc = line1split[10]
        yesOrNo = line1split[11]
        if yesOrNo == 'YES':
            temperaturedata = lines[1].split(' ')[9].split('=')[1]
            return float(temperaturedata) / 1000
        else:
            log("Thermometer: {thermometer} did not return yes.\n Text:\n {thermometertext}".format(thermometer, thermometertext))
            return -1
    except IOError as e:
        log("I/O error({0}): {1} reading thermometer {2}".format(e.errno, e.strerror, thermometer))
        return -1

def powerOnHeater():
    GPIO.output(HEATER_GPIO_PIN, True)
    #GPIO.output(LED_GPIO_PIN, True)
    log('***** HEATING *****')

def powerOffHeater():
    GPIO.output(HEATER_GPIO_PIN, False)
    #GPIO.output(LED_GPIO_PIN, False)
    log('______ heater off ______')

def runTempController():
    temp_C = getTemperature(FERMENTORTHERMOMETER)
    if temp_C < 0:
        log('!!! Invalid temperature reading !!!')
        return
    temp_F = ( temp_C * 9.0 / 5.0 ) + 32
    
    #3 significant digits
    temp_C = float("{0:.3g}".format(temp_C))
    temp_F = float("{0:.3g}".format(temp_F))
    
    powerOn = False
    percentDiff = (temp_C - TARGET_TEMP_C) / TARGET_TEMP_C * 100
    percentDiff = float("{0:.3g}".format(percentDiff))
    
    #heat until n% higher than target temp
    if percentDiff < 3.0 and percentDiff < 1.0:
        powerOn = True

    log("temp_F:\t\t{0} degF".format(temp_F))
    log("temp_C:\t\t{0} degC".format(temp_C))
    log("target:\t\t{0} degC".format(TARGET_TEMP_C))
    log('percent difference:\t{0:}%'.format(percentDiff))
    
    if powerOn:
        powerOnHeater()
    else:
        powerOffHeater()
    
    if COSM:
        # open up your cosm feed
        pac = eeml.Pachube(COSM_API_URL_BASE.format(feednum = COSM_API_FEED), COSM_API_KEY)
        #prepare temperature, target, percent difference and heater status data
        pac.update([eeml.Data(COSM_STRING_TEMP_C_DATA, temp_C, unit=eeml.Celsius())])
        pac.update([eeml.Data(COSM_STRING_TARGET_TEMP_DATA, TARGET_TEMP_C, unit=eeml.Celsius())])
        pac.update([eeml.Data(COSM_STRING_HEATER_IS_ON_DATA, int(powerOn), unit=eeml.Unit('HeaterOnOff', 'contextDependentUnits', ''))])
        pac.update([eeml.Data(COSM_STRING_TEMP_PERCENT_DIFF_DATA, float('{0:.3g}'.format(percentDiff)), unit=eeml.Unit('PercentDifferenceToTargetTemperature', 'contextDependentUnits', '%'))])
        # send data to cosm
        try:
            log('sending data to cosm...')
            pac.put()
            log('done :)')
        except Exception as e:
            log('!!! Failed to send data to cosm :( !!! Exception: {0}'.format(e))
    
    
log('====================================================')
log('*** Starting up...')
loadConfig(CONFIG_FILE)
setupGPIO()
while True:
    try:
        runTempController()
    except Exception as e:
        log('Exception in runTempController:\n{0}'.format(e))
        log('Powering off the heater due to the exception...')
        powerOffHeater()
        log('ok: program excution should continue.')
    time.sleep(MEASUREMENT_INTERVAL_SEC)
log('*** Shutting down...')
powerOffHeater()
exit(-1)