import glob
import os
import time
import requests
import convert_right_left
from urllib.parse import urljoin


files = []
counter = 0
this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])
folder_len = len(f"{this_folder}/toUpload/")

for fpath in glob.glob("/home/la/Desktop/bots/chords-bot/toUpload/*"):
    files.append(fpath)

# for fname in files:
fname = f"{this_folder}/message-intro.txt"
with open(fname, "r") as f:
    introB = f.read()

fname = f"{this_folder}/message-end.txt"
with open(fname, "r") as f:
    endB = f.read()

counting = 1
if len(files) == 0:
    print("nothing to upload!")
else:
    print("uploading updates..")
username = 'elikopeleg'
token = '242fa8569f24430b576c163b70545297a0652117'
pythonanywhere_host = "www.pythonanywhere.com"
api_base = f"https://{pythonanywhere_host}/api/v0/user/{username}/"

for fpath in files:
    with open(fpath, "r") as f:
        data = f.read()
        os.replace(fpath, f"{this_folder}/uploaded/" + fpath[folder_len:])
        # no need to upload if running on the server.
        resp = requests.post(
            urljoin(api_base, f"files/path/home/{username}/uploaded/{fpath[folder_len:]}"),
            files={"content": data},
            headers={"Authorization": "Token {api_token}".format(api_token=token)}
        )

        print(fpath)
        data = data.split('\n')
        intro = introB
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(",",
                                                                                                                   "").replace(
                                  ".", "_") + "   \n" + data[0])
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(".",
                                                                                                                   "_").replace(
                                  ",", "") + "   \n" + data[1])
        intro = intro.replace("capo", data[3])
        song = {0: ""}
        counter = 0
        data[3] = intro
        data.append(endB)
        for j in data[3:]:
            test = song[counter] + "%0A" + j + endB
            if len(test.replace("#", "%23").replace('\n', '%0A')) >= 4096:
                counter += 1
                song[counter] = ""
            song[counter] += "%0A" + j

        counter = 0
        for i in song:

            url = "https://api.telegram.org/bot999605455:AAFkVPs2jTncditDCzMdGCkatrOfodsVGxE/sendMessage?chat_id=-1001410527666&text=" + \
                  song[counter]

            if counting % 20 == 0:
                time.sleep(65)

            try:

                r = requests.get(url.replace("#", "%23").replace('\n', '%0A'), timeout=None)
                if r.status_code != 200:
                    print("\n\nERROR\n\n", r.status_code)
                    exit()
                counting += 1
            except requests.Timeout as err:
                break
            r.connection.close()
            counter += 1
