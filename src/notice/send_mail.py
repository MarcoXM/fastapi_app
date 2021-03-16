import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from functools import lru_cache
from template import Template

@lru_cache()
def cached_dotenv():
    load_dotenv()


cached_dotenv()

user_name = os.environ.get("USER_NAME")
pass_word = os.environ.get("PASS_WORD")

class Emailer(object):

    from_email = user_name
    template_html = None

    def __init__(self, 
            subject = "",
            template_name = None,
            context = {},
            template_html = None,
            to_emails = None,
            test_send = False
        ):
        if template_html is None and template_name is None: 
            raise Exception("template file is needed ! ")

        assert isinstance(to_emails, list )
        self.subject = subject
        self.template_name = template_name
        self.context = context
        if template_html is not None:
            self.has_html = True
            self.template_html = template_html
        
        self.to_emails = to_emails
        self.test_send = test_send

    def format_msg(self):

        ## inital msg obj 
        msg = MIMEMultipart('alternative')
        msg['From'] = self.from_email
        msg['To'] = ", ".join(self.to_emails)
        msg['Subject'] = self.subject

        ## attach the txt information 
        if self.template_name is not None:
            text = Template(self.template_name, context= self.context)
            txt_part = MIMEText(text.render(), "plain")
            msg.attach(txt_part)

        if self.template_html is not None:
            html = Template(self.template_html, context= self.context)
            html_part = MIMEText(html.render(),'html')
            msg.attach(html_part)

        msg_str = msg.as_string()

        return msg_str


    def send(self):
        msg_str = self.format_msg()

        #
        did_send = False
        if not self.test_send:
            server = smtplib.SMTP(host='smtp.gmail.com',port=587)
            server.ehlo()
            server.starttls()
            server.login(self.from_email,pass_word)
            try:
                server.sendmail(user_name, self.to_emails,msg_str)
                did_send = True
            except:
                did_send = False
            server.quit()

        return did_send


if __name__ == "__main__":
    emailer = Emailer(subject="hello this is a test",
    template_name="hello.txt",context={"recipient_name":"Marco"},
    to_emails=['xwang423@fordham.edu'])
    print(emailer.send())
