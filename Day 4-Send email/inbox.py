import imaplib
import email

from decouple import config


username = config('username')
password = config('password')

mail = imaplib.IMAP4_SSL(host='imap.gmail.com')
mail.login(user=username, password=password)
mail.select('inbox')

_, search_data = mail.search(None, 'ALL')

for num in search_data[0].split():
    _, data = mail.fetch(num, '(RFC822)')
    # print(data[0])
    _, b = data[0]
    email_message = email.message_from_bytes(b)
    # print(email_message)

    for header in ['subject', 'to', 'from', 'date']:
        print(f'{header}: {email_message[header]}')

    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':
            body = part.get_payload(decode=True)
            print(body.decode(), '\n')

        elif part.get_content_type() == 'text/html':
            html_body = part.get_payload(decode=True)
            print(html_body.decode(), '\n')

mail.close()
