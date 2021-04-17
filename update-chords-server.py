from urllib.parse import urljoin

import requests
import tokens

username = 'elikopeleg'
token = tokens.pythonanywhere
pythonanywhere_host = "www.pythonanywhere.com"
api_base = "https://{pythonanywhere_host}/api/v0/user/{username}/".format(
    pythonanywhere_host=pythonanywhere_host,
    username=username,
)

fpath = "/home/la/Desktop/bots/chords-bot/chordServer.py"
with open(fpath, "r") as f:
    data = f.read()
update_resp = requests.post(
    urljoin(api_base, f"files/path/home/{username}/chordServer.py"),
    files={"content": data},
    headers={"Authorization": "Token {api_token}".format(api_token=token)}
)
run_resp = requests.post(
    f"{api_base}/consoles/19561760/send_input/",
    data={"input": str(chr(3)) + "\npython3 chordServer.py \n"},
    headers={"Authorization": "Token {api_token}".format(api_token=token)}
)
