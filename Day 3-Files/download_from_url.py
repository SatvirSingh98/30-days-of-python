import os
import requests
# import shutil

from download_util import download_file


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
downloaded_img_path = os.path.join(DOWNLOADS_DIR, '1.jpg')

url = 'https://images2.minutemediacdn.com/image/upload/c_fill\
,g_auto,/h_1248,w_2220/v1555922701/shape/mentalfloss/\
istock_000008977856_small.jpg'


# smallish item
r1 = requests.get(url)
r1.raise_for_status
with open(downloaded_img_path, 'wb') as f:
    f.write(r1.content)


# better method but cannot reuse it as it is not a function
# dl_filename = os.path.basename(url)
# new_dl_filename = os.path.join(DOWNLOADS_DIR, dl_filename)
# with requests.get(url, stream=True) as r2:
#     with open(new_dl_filename, 'wb') as file_obj:
#         shutil.copyfileobj(r2.raw, file_obj)

download_file(url, DOWNLOADS_DIR,)
download_file(url, DOWNLOADS_DIR, 'img+from+web.jpg')
