#!/usr/bin/python
# encoding=utf8
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime
import Adafruit_DHT
#Preping email
import smtplib, ssl
import csv
password = "pieckcmrules1"
emailFile = open('/home/pi/Adafruit_DHT/examples/email.txt', 'r')
receivingEmail = str(emailFile.read())
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "johnleerbp@gmail.com"  # Enter your address
##MESSAGE##
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
headers  = "From: John Test \r\n"
headers += "To: You \r\n"
headers += "Subject: Temperature/Humidity Status\r\n"
headers += "\r\n"
message = "ALERT!"



##dates for highest/lowest recorded stuff
with open('/home/pi/Adafruit_DHT/examples/stats.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            hrtDate = row[0]
            lrtDate = row[1]
            hrhDate= row[2]
            lrhDate = row[3]
            hrt = row[4]
            lrt = row[5]
            hrh= row[6]
            lrh = row[7]
##updating STATS if limit is reached / new record is created
def updateStats():
    with open('/home/pi/Adafruit_DHT/examples/stats.txt', mode='w', newline='') as csv_file:
        log_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow([hrtDate, lrtDate, hrhDate, lrhDate, str(hrt), str(lrt), str(hrh), str(lrh)])
##TEMPERATURE AND HUMIDITY LIMITS######
tempUpLim = 0
tempLowLim = 0
humUpLim = 0
humLowLim = 0
##########################################

#################CHECKING THE CONFIG FILE##
with open('/home/pi/Adafruit_DHT/examples/config.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            tempUpLim = int(row[0])
            tempLowLim = int(row[1])
            humUpLim = int(row[2])
            humLowLim = int(row[3])
print("humUpLim = " + str(humUpLim))
print("humLowLim = " + str(humLowLim))
print("tempUpLim = " + str(tempUpLim))
print("tempLowLim = " + str(tempLowLim))

####################################################

###UPDATING THE CONFIG FILE!!!#####################
def updateConfig():
    with open('/home/pi/Adafruit_DHT/examples/config.txt', mode='w', newline='') as csv_file:
        log_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow([str(tempUpLim), str(tempLowLim), str(humUpLim), str(humLowLim)])
########################################################
sensor = Adafruit_DHT.DHT22
pin = 4
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
def updateLog():
    with open('/home/pi/Adafruit_DHT/examples/log.txt', mode='a', newline='') as csv_file:
        log_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow([date, str(round(temperature, 2)), str(round(humidity, 2)) + "0", str(alert)])

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!


##EMAIL ALERT TIMER##
timer = 0
alert = False
while (True):
    if humidity is not None and temperature is not None:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        ##creating messages for specific use cases
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        message1 = "ALERT! Your server room is TOO HOT! \r\n Date = " + date + "\r\n Temperature = " + str(temperature) + "°\Degrees C\r\n Humidity = " + str(humidity) +"%"
        message2 = "ALERT! Your server room is TOO COLD! \r\n Date = " + date + "\r\n Temperature = " + str(temperature) + "Degrees C\r\n Humidity = " + str(humidity) +"%"
        message3 = "ALERT! Your server room is TOO HUMID! \r\n Date = " + date + "\r\n Temperature = " + str(temperature) + "Degrees C\r\n Humidity = " + str(humidity) +"%"
        message4 = "ALERT! Your server room is TOO DRY! \r\n Date = " + date + "\r\n Temperature = " + str(temperature) + "Degrees C\r\n Humidity = " + str(humidity) +"%"     
        ####################################
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updateLog()
        ##creating checking for stats 
        if temperature > float(hrt):
            hrt = round(temperature,2)
            hrtDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updateStats()
        if temperature < float(lrt):
            lrt = round(temperature,2)
            lrtDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updateStats()
        if humidity > float(hrh):
            hrh = round(humidity,2)
            hrhDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updateStats()
        if humidity < float(lrh):
            lrh = round(humidity,2)
            lrhDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updateStats()
        if temperature > tempUpLim:
            alert = True
            if alert == True:
                print("alert updated")
            message = headers + message1
        with open('/home/pi/Adafruit_DHT/examples/config.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    tempUpLim = int(row[0])
                    tempLowLim = int(row[1])
                    humUpLim = int(row[2])
                    humLowLim = int(row[3])
        if temperature < tempLowLim:
            alert = True
            message = headers + message2
        if humidity > humUpLim:
            alert = True
            message = headers + message3
        if humidity < humLowLim:
            alert = True
            message = headers + message4
        ##RESETTING THE ALERT#####
        if (temperature < tempUpLim and temperature > tempLowLim and humidity < humUpLim and humidity > humLowLim):
            alert = False
        
        #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        context = ssl.create_default_context()
        if (timer == 0 and alert == True):
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receivingEmail, message)
            print("humUpLim = " + str(humUpLim))
            print("humLowLim = " + str(humLowLim))
            print("tempUpLim = " + str(tempUpLim))
            print("tempLowLim = " + str(tempLowLim))
            print("Humidity = " + str(humidity))
            print("Temperature = " + str(temperature))
            print("Email sent!")
            timer = 20
        else:
            if timer != 0:
                timer = timer - 1
            #print ("Timer = " + str(timer))
        time.sleep(30)
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    
    

