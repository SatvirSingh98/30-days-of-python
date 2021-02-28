import requests

ngrok_url = '<ngrok_url>'
endpoint = f"{ngrok_url}/scrape-boxofficemojo"

r = requests.post(endpoint, json={})
print(r.json()['msg'])
