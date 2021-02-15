import os
import shutil
import requests


def download_file(url, directory, filename=None):
    if filename is None:
        filename = os.path.basename(url)
    dl_filename = os.path.join(directory, filename)
    with requests.get(url, stream=True) as r:
        with open(dl_filename, 'wb') as file_obj:
            shutil.copyfileobj(r.raw, file_obj)
    return dl_filename
