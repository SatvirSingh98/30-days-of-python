def my_print(txt):
    print(txt)


message = """Hello {name},
Thankyou for joining {website}. We are very happy to have you with us.
"""  # .format(name='stavir', website='cfe.sh')


def format_msg(my_name='Satvir Singh', my_website='cfe.sh'):
    my_msg = message.format(name=my_name, website=my_website)
    # print(my_msg)
    return my_msg


print(format_msg())

names = ['Puneet', 'Prince', 'Sagar']
for name in names:
    new_msg = format_msg(my_name=name)
    print(new_msg)
