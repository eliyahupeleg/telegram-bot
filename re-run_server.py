from urllib.parse import urljoin

import requests

username = 'elikopeleg'
token = '242fa8569f24430b576c163b70545297a0652117'
pythonanywhere_host = "www.pythonanywhere.com"
# https://www.pythonanywhere.com/api/v0/user/elikopeleg/consoles/16352775/send_input/
api_base = "https://{pythonanywhere_host}/api/v0/user/{username}/".format(
    pythonanywhere_host=pythonanywhere_host,
    username=username,
)
print(f"{api_base}/consoles/16352775/send_input/")
resp = requests.post(
    f"{api_base}/consoles/16352775/send_input/",
    data={"input": str(chr(3)) + "python3 chordServer.py \n"},
    headers={"Authorization": "Token {api_token}".format(api_token=token)}
)
