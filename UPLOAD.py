import glob
import os
import time
from urllib.parse import urljoin

import requests

import tokens

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
token = tokens.pythonanywhere
pythonanywhere_host = "www.pythonanywhere.com"
api_base = f"https://{pythonanywhere_host}/api/v0/user/{username}/"

for fpath in files:
    print(fpath)
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

        if data.split("\n")[5] == "HE":
            data = data.replace("#]", "#ᶥ")

        data = data.replace("[", "").replace("]", "").replace("]", "")
        data = data.split('\n')

        intro = introB
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + f"   \n{data[0]}")
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + f"   \n{data[1]}")

        if "המערכת" == data[2]:
            intro = intro.replace("version", "⭐️ גרסה רשמית ⭐")
        else:
            intro = intro.replace("version", "")

        # כמה צריך להזיז כדי להגיע לגרסה קלה
        easy_key = data[3]

        # איפה לשים קאפו
        if "0" == data[4]:
            intro = intro.replace("capo", "")
        else:
            intro = intro.replace("capo", f"קאפו בשריג {data[4]}")

        # המידע בתחילת הקובץ לא נשלח, רק מ - data[3] ואילך.
        # ולכן מכניסים ל- data[3] את כל הפתיח הרשמי, והוא נשלח משם.
        data[5] = intro
        data.append(endB)

        song = {0: ""}
        counter = 0

        # מחלק את ההודעה לחלקים של פחות מ4096 בתים - האורך המקסימלי להודעה בטלגרם
        for j in data[5:]:
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
