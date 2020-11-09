import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 

def sendMail(html, targetMail, subject):
    print("Send mail to " + targetMail)

    fromaddr = "EMAIL"
    toaddr = targetMail
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "" + subject; 
    
    msg.attach(MIMEText(html, 'html'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
