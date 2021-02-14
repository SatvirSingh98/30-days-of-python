message = """Hello {name},
Thankyou for joining {website}. We are very happy to have you with us.
"""


def format_msg(my_name='Anonymous', my_website='cfe.sh'):
    my_msg = message.format(name=my_name, website=my_website)
    return my_msg
