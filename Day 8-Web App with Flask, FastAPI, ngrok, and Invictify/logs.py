import os
from datetime import datetime


BASE_DIR = os.path.dirname(__file__)
logs_dir = os.path.join(BASE_DIR, 'logs')

os.makedirs(logs_dir, exist_ok=True)


def trigger_log_save():
    filename = f"{datetime.now()}.txt"
    filepath = os.path.join(logs_dir, filename)

    with open(filepath, 'w+') as f:
        f.write('')
