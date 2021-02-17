import imaplib
import email

from decouple import config


username = config('username')
password = config('password')


def get_inbox():
    mail = imaplib.IMAP4_SSL(host='imap.gmail.com')
    mail.login(user=username, password=password)
    mail.select('inbox')

    _, search_data = mail.search(None, 'ALL')
    my_messages = []

    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        # print(email_message)

        for header in ['subject', 'to', 'from', 'date']:
            print(f'{header}: {email_message[header]}')
            email_data[header] = email_message[header]

        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                print(body.decode(), '\n')
                email_data['body'] = body.decode()

            elif part.get_content_type() == 'text/html':
                html_body = part.get_payload(decode=True)
                print(html_body.decode(), '\n')
                email_data['body'] = html_body.decode()

    my_messages.append(email_data)
    mail.close()
    return my_messages


if __name__ == "__main__":
    my_inbox = get_inbox()
    print(my_inbox)
