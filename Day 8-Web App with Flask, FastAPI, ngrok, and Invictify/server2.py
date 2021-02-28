# to run flask app with gunicorn:
# uvicorn <filename>:<appname>
# eg:- uvicorn server2:app

# to run from shell script:
# 1. chmod +x run_server2.sh
# 2. ./run_server2.sh

# to deploy on live server we will use ngrok
# and set it up on invictify for scheduled job for accesing url.
# 1. download ngrok
# 2. set alias for ngrok to access it from anywhere from your machine
# --- sudo nano ~/.zshrc
# --- alias ngrok='/path_to_ngrok/ngrok'
# --- source ~/.zshrc
# 3. ./ngrok authtoken <token>
# 4. run the file --> In this case run_server2.sh
# 5. ngrok http <port>
# 6. port has to be same for ngrok and server_file

from fastapi import FastAPI

from logs import trigger_log_save
from scrape import run as scrape_runner

app = FastAPI()


# http://localhost:8888/
@app.get('/')
def hello():
    return {'msg': 'Hello, World!'}


# http://localhost:8888/abc
@app.get('/abc')
def abc():
    return {'msg': 'abc view'}


# http://localhost:8888/scrape-boxofficemojo
# we use 'POST' to trigger it with another request
@app.post('/scrape-boxofficemojo')
def scrape_view():
    trigger_log_save()
    scrape_runner()
    return {'msg': 'Done'}
