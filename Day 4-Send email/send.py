import sys

from formatting import format_msg
from send_mail import send_mail


def send(name, website=None, verbose=False, to_email=None):
    assert to_email is not None
    if website is not None:
        msg = format_msg(my_name=name, my_website=website)
    else:
        msg = format_msg(my_name=name)
    if verbose:
        print(name, website, to_email)
        print(msg)
    send_mail(text=msg, send_to=[to_email])


if __name__ == "__main__":
    print(sys.argv)
    name_from_terminal = 'Anonymous'
    if len(sys.argv) > 1:
        name_from_terminal = sys.argv[1]
    email_from_terminal = None
    if len(sys.argv) > 2:
        email_from_terminal = sys.argv[2]
    response = send(name=name_from_terminal, verbose=True,
                    to_email=email_from_terminal)
    print(response)
