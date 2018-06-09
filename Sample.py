#import libraries
import shopify, requests, json, math, time, os, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("ratoonistore@gmail.com", "RatooniStore@2017")

fromaddr = "jobrun@ratoonistore.com"
toaddr = "ratoonistore@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "WholesaleBox Job Run Report for : " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
 
body = """<html>
  <head></head>
  <body>
    <p><br><b>WholesaleBox Job Run Report for : """ + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + """</b><br><hr><br>""" + "" + """
       <br><br> <br><br>
    </p>
  </body>
</html>"""
msg.attach(MIMEText(body, 'html'))

text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
