import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_message():
    msg = MIMEMultipart('alternative')
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.connect("smtp.gmail.com",587)
    s.ehlo()
    s.starttls()
    USERNAME = 'johnleerbp@gmail.com'
    PASSWORD = 'pieckcmrules1'
    emailFile = open('/home/pi/Adafruit_DHT/examples/email.txt', 'r')
    receivingEmail = str(emailFile.read())
    s.login(USERNAME, PASSWORD)

    toEmail, fromEmail = receivingEmail, 'johnleerbp@gmail.com'
    msg['Subject'] = 'Sensor Log'
    msg['From'] = fromEmail
    body = 'Attached is a log for the Server Sensor'

    content = MIMEText(body, 'plain')
    msg.attach(content)
    filename = "/home/pi/Adafruit_DHT/examples/log.txt"
    f = open(filename)
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename='log.txt')       
    msg.attach(attachment)
    s.sendmail(fromEmail, toEmail, msg.as_string())
    print("Success?")
send_message()