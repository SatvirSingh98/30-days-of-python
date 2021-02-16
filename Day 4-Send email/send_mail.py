import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config

username = config('username')
passsword = config('password')


def send_mail(text='email body', subject='hello world',
              from_to=f"Satvir <{username}>",
              send_to=None, html=None):
    assert isinstance(send_to, list)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_to
    message["To"] = ', '.join(send_to)

    txt_part = MIMEText(text, 'plain')
    message.attach(txt_part)

    # html = """\
    # <html>
    # <body>
    #     <p>Hi,<br>
    #     How are you?<br>
    #     <a href="http://www.realpython.com">Real Python </a>
    #     has many great tutorials.
    #     </p>
    # </body>
    # </html>
    # """

    if html is not None:
        html_part = MIMEText(html, 'html')
        message.attach(html_part)

    try:
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.login(username, passsword)
        server.sendmail(from_to, send_to, message.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()
