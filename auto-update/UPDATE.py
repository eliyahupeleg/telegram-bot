import subprocess
from bs4 import BeautifulSoup
import time
import os
import webbrowser
import requests

fname = "/home/la/Downloads/HtmlsaveToTxt/tab4u/auto-update/lst.txt"
print("checking for updates..")
while True:
    with open(fname, "r") as f:
        lst = f.read()

    basic_url = "https://www.tab4u.com/songForMobile.php?id="

    search = "https://www.tab4u.com/resultsSimple?tab=songs&type=song&q=0&content=&max_chords=0"
    request = requests.get(search, timeout=None)
    soup = BeautifulSoup(request.content, "html.parser")
    # מספר התוצאות בחיפוש
    num = int(soup.find_all(class_="foundTxtTd")[0].getText().split(" ")[1])

    if int(lst) == int(num):
        print("up-to-date!!")
        break

    print("update coming..")

    # רק החדשים, פחות מה שנשמר.
    num = num - (num - int(lst))

    url = f"https://www.tab4u.com/resultsSimple?tab=songs&q=0&type=song&cat=&content=&max_chords=0&n=30&sort=&s={num}"
    request = requests.get(url, timeout=None)
    soup = BeautifulSoup(request.content, "html.parser")
    links = soup.select('.songTd1 .searchLink')

    # רשימת הלינקים של השירים החדשים
    links = [i['href'][11:] for i in links]

    for link in links:
        p = subprocess.Popen(["google-chrome", basic_url + link])

        while not os.path.exists("/home/la/Downloads/update.txt"):
            pass

        time.sleep(6)
        p.kill()
        with open("/home/la/Downloads/update.txt", "r+") as f:
            data = f.read().split('\n')

            os.replace("/home/la/Downloads/update.txt",
                       "/home/la/Downloads/HtmlsaveToTxt/bot/toUpload/" + data[1] + "- " + data[0] + ".txt")

        with open(fname, "r+") as f:
            f.seek(0)
            f.truncate()
            f.write(str(num+int(links.index(link))+1))
