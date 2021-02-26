import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config

from templates import Template

username = config('username')
password = config('password')


class Emailer:
    subject = ''
    send_to = []
    template_name = None
    template_html = None
    has_html = False
    test_send = False
    from_to = f"Satvir <{username}>"

    def __init__(self, subject='', template_name=None,
                 context={}, template_html=None, send_to=None,
                 test_send=False):
        if template_name is None and template_html is None:
            raise Exception('You must set a template.')
        assert isinstance(send_to, list)
        self.send_to = send_to
        self.subject = subject
        self.template_name = template_name
        self.context = context
        if template_html is not None:
            self.has_html = True
            self.template_html = template_html
        self.test_send = test_send

    def format_msg(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.from_to
        message["To"] = ', '.join(self.send_to)

        if self.template_name is not None:
            tmpl_str = Template(self.template_name, self.context)
            txt_part = MIMEText(tmpl_str.render(), 'plain')
            print(txt_part)
            message.attach(txt_part)

        if self.template_html is not None:
            tmpl_str = Template(self.template_html, self.context)
            html_part = MIMEText(tmpl_str.render(), 'html')
            print(html_part)
            message.attach(html_part)

        message = message.as_string()
        return message

    def send(self):
        did_send = False
        msg = self.format_msg()

        if not self.test_send:
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.login(username, password)
            try:
                server.sendmail(self.from_to, self.send_to, msg)
                did_send = True
            except Exception as e:
                print(e)
                did_send = False
        return did_send
