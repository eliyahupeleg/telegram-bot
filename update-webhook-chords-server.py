from urllib.parse import urljoin

import requests

username = 'elikopeleg'
token = '242fa8569f24430b576c163b70545297a0652117'
pythonanywhere_host = "www.pythonanywhere.com"
api_base = "https://{pythonanywhere_host}/api/v0/user/{username}/".format(
    pythonanywhere_host=pythonanywhere_host,
    username=username,
)

fpath = "/home/la/Desktop/bots/chords-bot/chord_server_webhook.py"
with open(fpath, "r") as f:
    data = f.read()
    
update_resp = requests.post(
    urljoin(api_base, f"files/path/home/{username}/webhook_telegram_bot/chords_server_webhook.py"),
    files={"content": data},
    headers={"Authorization": "Token {api_token}".format(api_token=token)}
)


domain_name = "elikopeleg.pythonanywhere.com"
reload = requests.post(
    urljoin(api_base, f"/api/v0/user/{username}/webapps/{domain_name}/reload/"),
    files={"content": data},
    headers={"Authorization": "Token {api_token}".format(api_token=token)}
)