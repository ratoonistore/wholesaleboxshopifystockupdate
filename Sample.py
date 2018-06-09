import smtplib
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("ratoonistore@gmail.com", "RatooniStore@2017")
 
msg = "YOUR MESSAGE!"
server.sendmail("ratoonistore@gmail.com", "ratoonistore@gmail.com", msg)
server.quit()
