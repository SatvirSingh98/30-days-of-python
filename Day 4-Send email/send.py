import requests
import sys
from formatting import format_msg


def send(name, website=None, verbose=False):
    if website is not None:
        msg = format_msg(my_name=name, my_website=website)
    else:
        msg = format_msg(my_name=name)
    if verbose is True:
        print(name, website)
        print(msg)
    r = requests.get('http://httpbin.org/json')
    if r.status_code == 200:
        return r.json()
    else:
        return 'There was an error.'


if __name__ == "__main__":
    print(sys.argv)
    name_from_terminal = 'Anonymous'
    if len(sys.argv) > 1:
        name_from_terminal = sys.argv[1]
    response = send(name=name_from_terminal, verbose=True)
    print(response)
