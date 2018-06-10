import smtplib, base64
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

def sendMail(mailSubject, mailBody):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("wirebuys@gmail.com", base64.b64decode("V2lyZUJ1eXNAMjAxNw=="))

    fromaddr = "wirebuys@gmail.com"
    toaddr = "ratoonistore@gmail.com"
    
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = mailSubject

    body = mailBody
    
    msg.attach(MIMEText(body, 'html'))

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
