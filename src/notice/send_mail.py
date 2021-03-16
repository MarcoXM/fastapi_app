import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os



user_name = os.environ.get("USER_NAME")
pass_word = os.environ.get("PASS_WORD")

def send_mail(text = 'Email Body', subject = 'Hello World',from_email = user_name ,to_emails = None, html = None):
    assert isinstance(to_emails, list )

    ## msg_str
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    txt_part = MIMEText(text, "plain")
    msg.attach(txt_part)

    if html is not None:

        html_part = MIMEText(html,'html')
        msg.attach(html_part)

    msg_str = msg.as_string()

    ## 
    server = smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(user_name,pass_word)
    server.sendmail(from_email, to_emails,msg_str)
    server.quit