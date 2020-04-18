from urllib.parse import urljoin

import requests

username = 'elikopeleg'
token = '242fa8569f24430b576c163b70545297a0652117'
pythonanywhere_host = "www.pythonanywhere.com"
api_base = "https://{pythonanywhere_host}/api/v0/user/{username}/".format(
    pythonanywhere_host=pythonanywhere_host,
    username=username,
)

fpath = "/home/la/Downloads/HtmlsaveToTxt/bot/searchBot.py"
with open(fpath, "r") as f:
    data = f.read()
resp = requests.post(
    urljoin(api_base, f"files/path/home/{username}/searchBot.py"),
    files={"content": data},
    headers={"Authorization": "Token {api_token}".format(api_token=token)}
)
