#Preping email
import smtplib, ssl
import csv
import time
import datetime
import Adafruit_DHT
from tkinter import*
##getting email address from txt file

#####CODE FOR DISPLAYING THE LOG??###
def showLog():
    logWindow = Tk()
    logWindow.geometry("500x500")
    scrollbar = Scrollbar(logWindow)
    scrollbar.pack(side=RIGHT, fill=Y, expand=TRUE)
    listbox = Listbox(logWindow, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    file = open("/home/pi/Adafruit_DHT/examples/log.txt")
    numline = len(file.readlines())
    with open("/home/pi/Adafruit_DHT/examples/log.txt") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            word = str(row[0]) + "///T:"+ str(row[1])+ "///H:"+ str(row[2])+ "///S:"+ str(row[3])
            listbox.insert(END, word)
        #lis=[line.split() for line in csvfile]
        #for i, x in enumerate(lis):
        #    listbox.insert(END, "{1}".format(i,x))
    listbox.pack(side=LEFT, fill=BOTH, expand=TRUE)




####END LOG DISPLAY CODE#####

#showLog()


emailFile = open('/home/pi/Adafruit_DHT/examples/email.txt', 'r')
receivingEmail = str(emailFile.read())
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "johnleerbp@gmail.com"  # Enter your address
receiver_email = ""
password = "pieckcmrules"
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#current temperature
##TEMPERATURE AND HUMIDITY LIMITS######
tempUpLim = 0
tempLowLim = 0
humUpLim = 0
humLowLim = 0
#ADAFRUIT CALL
sensor = Adafruit_DHT.DHT22
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
humidity = round(humidity,2)
temperature = round(temperature,2)
#temperature = int(temperature)
#humidity = int(humidity)
#highest recorded temperature
hrt = 100
#highest recorded temperature date
hrtDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#lowest recorded temperature
lrt = 10
#lowest recorded temperature
lrtDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#highest recoded humidity
hrh = 100
#highest recoded humidity date
hrhDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#lowest recorded humidity
lrhDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#lowest recorded humidity date
lrh = 0
headers  = "From: John Test \r\n"
headers += "To: You \r\n"
headers += "Subject: Temperature/Humidity Status\r\n"
headers += "\r\n"
message = "The current date and time is: " + date + "\r\nThe current temperature is " + str(temperature) + " Degrees Celsius.\r\nThe current humidity is " + str(humidity) + "%.\r\nThe highest recorded temperature is " + str(hrt) + " and occured at " + str(hrtDate) + ".\r\nThe lowest recorded temperature is " + str(lrt) + " and occured at " + str(lrtDate) +".\r\nThe highest recorded humidity is " + str(hrh) + " and occured at " + str(hrhDate) +".\r\nThe lowest recorded humidity is " + str(lrt) + " and occured at " + str(lrtDate) + "."
message = headers + message
####################################
window = Tk()
window.title("Server Room")
window.geometry('850x300')
numOfClicks = 0
###CHECKING AND UPDATING
def updateStats():
    with open('/home/pi/Adafruit_DHT/examples/stats.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        global hrtDate
        global lrtDate
        global hrhDate
        global lrhDate
        global hrt
        global lrt
        global hrh
        global lrh
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
updateStats()

lbl0Text = "Current Temp in Celsius"
lbl1Text = "Current Temp in Fahrenheit"
lbl2Text = "Current Humidity in Percentage"
lbl3Text = str(temperature) + "°C"
fTemperature = (temperature)*9/5 + 32
fTemperature = round(fTemperature, 2)
lbl4Text =  str(fTemperature) + "°F"
lbl5Text = str(humidity) + "%"
#lbl6Text = "______"
lbl7Text = emailFile.read()
lbl8Text = "BUTTON HERE"
lbl9Text = "Current Date/Time"
lbl10Text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
lbl11Text = "BLANK"
lbl12Text = "Highest Recorded Temperature"
lbl13Text = str(hrt) + "°C"
lbl14Text = "DATE/TIME"
lbl15Text = "Lowest Recorded Temperature"
lbl16Text = str(lrt) + "°C"
lbl17Text = "DATE/TIME"
lbl18Text = "Highest Recorded Humidity "
lbl19Text = str(hrh) + "%"
lbl20Text = "DATE/TIME"
lbl21Text = "Lowest Recorded Humidity"
lbl22Text = str(lrh) + "%"
lbl23Text = "DATE/TIME"


##menu##
def hello():
    print ("hello!")
def refresh():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    humidity = round(humidity,2)
    temperature = round(temperature,2)
    lbl3.config(text=str(temperature) + "°C")
    fTemperature = round(((temperature)*9/5 + 32),2)
    lbl4.config(text=str(fTemperature) + "°F")
    lbl5.config(text=str(humidity) + "%")
    updateStats()
    lbl13.config(text=hrt + "°C")
    lbl14.config(text=hrtDate)
    lbl16.config(text=lrt + "°C")
    lbl17.config(text=lrtDate)
    lbl19.config(text=hrh + "%")
    lbl20.config(text=hrhDate)
    lbl22.config(text=lrh + "%")
    lbl23.config(text=lrhDate)

    
menubar = Menu(window)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Refresh", command=refresh)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)


# display the menu
window.config(menu=menubar)



#DEGREES IN FAHRENHEIT TITLE
lbl0 = Label(window, text=lbl0Text, width = 25)
lbl0.grid(column=0, row=0)

#DEGREES IN CELSIUS TITLE
lbl1 = Label(window, text=lbl1Text)
lbl1.grid(column=1, row=0)


#HUMIDITY IN PERCENTAGE TITLE
lbl2 = Label(window, text=lbl2Text)
lbl2.grid(column=2, row=0)

#DEGREES IN FAHRENHEIT
lbl3 = Label(window, text=lbl3Text)
lbl3.grid(column=0, row=1)

#DEGREES IN CELSIUS
lbl4 = Label(window, text=lbl4Text)
lbl4.grid(column=1, row=1)

#HUMIDITY IN PERCENTAGE
lbl5 = Label(window, text=lbl5Text)
lbl5.grid(column=2, row=1)

#UPDATE EMAIL
Entry1 = Entry(window, width = 30)
Entry1.insert(10,"Update Email Here")
Entry1.grid(column=0, row=2)


#HUMIDITY IN PERCENTAGE
lbl7Text = receivingEmail
lbl7 = Label(window, text=lbl7Text)
lbl7.grid(column=1, row=2)

###THIS WILL BE A WHILE LOOP IN FINISHED PRODUCT 
###CHECKING AND UPDATING
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


def updateEmail():
    #exit()
    emailText = Entry1.get()
    receiver_email = Entry1.get()
    lbl7.config(text=emailText)
    context = ssl.create_default_context()
    lbl10.config(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ##updating email
    emailFile = open('/home/pi/Adafruit_DHT/examples/email.txt', 'w')
    emailFile.write(str(emailText))
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    with open('/home/pi/Adafruit_DHT/examples/log.txt', mode='a', newline='') as csv_file:
        log_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow([date, str(temperature), str(humidity)])
###updating tempUpLim 
def updateTempUpLim():
    #exit()
    global tempUpLim
    tempUpLim = Entry2.get()
    lbl24.config(text="Temperature Lower Limit : " + tempUpLim + "°C")
    updateConfig()
###updating tempLowLim
def updateTempLowLim():
    #exit()
    global tempLowLim
    tempLowLim = Entry3.get()
    lbl25.config(text="Temperature Lower Limit : " + tempLowLim + "°C")
    updateConfig()
###updating humUpLim
def updateHumUpLim():
    #exit()
    global humUpLim
    humUpLim = Entry4.get()
    lbl26.config(text="Humidity Upper Limit : " + humUpLim + "%")
    updateConfig()
###updating humLowLim
def updateHumLowLim():
    #exit()
    global humLowLim
    humLowLim = Entry5.get()
    lbl27.config(text="Humidity Lower Limit : " + humLowLim + "%")
    updateConfig()

##each update needs to also update the CSV...
def updateConfig():
    with open('/home/pi/Adafruit_DHT/examples/config.txt', mode='w', newline='') as csv_file:
        log_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow([str(tempUpLim), str(tempLowLim), str(humUpLim), str(humLowLim)])

#Update button for EMAILS
Button1 = Button(window, text="Update", command=updateEmail)
Button1.grid(column=2, row=2)


#HUMIDITY IN PERCENTAGE
lbl9 = Label(window, text=lbl9Text)
lbl9.grid(column=0, row=3)

#HUMIDITY IN PERCENTAGE
lbl10 = Label(window, text=lbl10Text)
lbl10.grid(column=1, row=3)

#HUMIDITY IN PERCENTAGE
lbl11 = Label(window, text=lbl11Text)
lbl11.grid(column=2, row=3)

#HUMIDITY IN PERCENTAGE
lbl12 = Label(window, text=lbl12Text)
lbl12.grid(column=0, row=4)

#HUMIDITY IN PERCENTAGE
lbl13 = Label(window, text=lbl13Text)
lbl13.grid(column=1, row=4)


#HUMIDITY IN PERCENTAGE
lbl14 = Label(window, text=lbl14Text)
lbl14.grid(column=2, row=4)
lbl14.config(text=hrtDate)

#HUMIDITY IN PERCENTAGE
lbl15 = Label(window, text=lbl15Text)
lbl15.grid(column=0, row=5)

#HUMIDITY IN PERCENTAGE
lbl16 = Label(window, text=lbl16Text)
lbl16.grid(column=1, row=5)

#HUMIDITY IN PERCENTAGE
lbl17 = Label(window, text=lbl17Text)
lbl17.grid(column=2, row=5)
lbl17.config(text=lrtDate)
#HUMIDITY IN PERCENTAGE
lbl18 = Label(window, text=lbl18Text)
lbl18.grid(column=0, row=6)

#HUMIDITY IN PERCENTAGE
lbl19 = Label(window, text=lbl19Text)
lbl19.grid(column=1, row=6)

#HUMIDITY IN PERCENTAGE
lbl20 = Label(window, text=lbl20Text)
lbl20.grid(column=2, row=6)
lbl20.config(text=hrhDate)

#HUMIDITY IN PERCENTAGE
lbl21 = Label(window, text=lbl21Text)
lbl21.grid(column=0, row=7)

#HUMIDITY IN PERCENTAGE
lbl22 = Label(window, text=lbl22Text)
lbl22.grid(column=1, row=7)

#HUMIDITY IN PERCENTAGE
lbl23 = Label(window, text=lbl23Text)
lbl23.grid(column=2, row=7)
lbl23.config(text=lrhDate)

#temperature upper limit
lbl24 = Label(window, text=str(tempUpLim))
lbl24.grid(column=0, row=8)
lbl24.config(text="Temperature Upper Limit : " + str(tempUpLim) + "°C")
#UPDATE temperature upper limit
Entry2 = Entry(window, width = 40)
Entry2.insert(10,"Update Temperature Upper Limit Here")
Entry2.grid(column=1, row=8)
#Update button for temperature upper limit
Button2 = Button(window, text="Update", command=updateTempUpLim)
Button2.grid(column=2, row=8)


#temperature lower limit
lbl25 = Label(window, text=str(tempLowLim))
lbl25.grid(column=0, row=9)
lbl25.config(text="Temperature Lower Limit : " + str(tempLowLim) + "°C")

#UPDATE temperature lower limit
Entry3 = Entry(window, width = 40)
Entry3.insert(10,"Update Temperature Lower Limit Here")
Entry3.grid(column=1, row=9) 
#Update button for temperature lower limit
Button3 = Button(window, text="Update", command=updateTempLowLim)
Button3.grid(column=2, row=9)

#humidity upper limit
lbl26 = Label(window, text=str(humUpLim))
lbl26.grid(column=0, row=10)
lbl26.config(text="Humidity Upper Limit : " + str(humUpLim) + "%")

#UPDATE temperature lower limit
Entry4 = Entry(window, width = 40)
Entry4.insert(10,"Update Humidity Upper Limit Here")
Entry4.grid(column=1, row=10) 
Button4 = Button(window, text="Update", command=updateHumUpLim)
Button4.grid(column=2, row=10)

#humidity lower limit
lbl27 = Label(window, text=str(humLowLim))
lbl27.grid(column=0, row=11)
lbl27.config(text="Humidity Lower Limit : " + str(humLowLim) + "%")
#UPDATE temperature lower limit
Entry5 = Entry(window, width = 40)
Entry5.insert(10,"Update Humidity Lower Limit Here")
Entry5.grid(column=1, row=11) 
Button5 = Button(window, text="Update", command=updateHumLowLim)
Button5.grid(column=2, row=11)
##SHOW LOG BUTTON
Button6 = Button(window, text="Show Log", command=showLog)
Button6.grid(column=1, row=12)

def clock():
    time = datetime.datetime.now().strftime("Date/Time = %Y-%m-%d %H:%M:%S")
    lbl10.config(text=time)
    window.after(1000, clock)
def autoRefresh():
    refresh()
    ##refreshes every thirty seconds
    window.after(30000, autoRefresh)
autoRefresh()
clock()


##clicking buttons
##clicking enter
def func(event):
    print("You hit return.")
window.bind('<Return>', func)


window.mainloop()