# to run flask app with gunicorn:
# gunicorn <filename>:<appname>
# eg:- gunicorn server1:app

# to run from shell script:
# 1. chmod +x run_server1.sh
# 2. ./run_server1.sh

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

from flask import Flask

from logs import trigger_log_save
from scrape import run as scrape_runner

app = Flask(__name__)


# http://localhost:8888/
@app.route('/', methods=['GET'])
def hello():
    return 'Go to "/scrape-boxofficemojo" for scrapping boxofficemojo'


# http://localhost:8888/abc
@app.route('/abc', methods=['GET'])
def abc():
    return 'abc view'


# http://localhost:8888/scrape-boxofficemojo
# we use 'POST' to trigger it with another request
@app.route('/scrape-boxofficemojo', methods=['POST'])
def scrape_view():
    trigger_log_save()
    scrape_runner()
    return {'msg': 'Done'}
