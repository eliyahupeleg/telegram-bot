import os
import time
import urllib.request
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')

# start chrome browser
browser = webdriver.Chrome(chrome_options=options, executable_path="/home/la/chromedriver")

js_save_links = r'''artists = document.getElementsByClassName('_2hJom');
var links = "";
for ( var a of artists){
    links += a.children[0].children[0].children[0].href + "\n"
}
return links'''
js_check_next = '''if(document.getElementsByClassName("_2kTPR _1nJLO _3sEsO _2KJtL _1ofov kWOod").length > 0) return(document.getElementsByClassName("_2kTPR _1nJLO _3sEsO _2KJtL _1ofov kWOod")[0].href)'''
songs_links = ""
errors = []
with open("/home/la/Desktop/bots/chords-bot/ultimate-guitar/all_artists.txt", "r") as f:
    artist_links = f.read().split("\n")

for artist_link in artist_links:

    try:
        browser.get(artist_link)
        if browser.title == "יש לך אינטרנט עם הגנה":
            errors.append(artist_link)
            print(browser.title, artist_link)
            continue

        new = browser.execute_script(js_save_links)
        songs_links += new
        next_page = browser.execute_script(js_check_next)

        if next_page:
            artist_links.append(next_page)
            print("next: ", next_page)

        print("artist ", artist_link)
        print("new: ", new)
        print(artist_links.index(artist_link), "/", len(artist_links))

        if (artist_links.index(artist_link) + 1) % 400 == 0:
            print("400. waiting for reset network.")
            ip = urllib.request.urlopen("https://api.ipify.org").read().decode("utf-8")
            old_ip = urllib.request.urlopen("https://api.ipify.org").read().decode("utf-8")
            print("old ip: ", ip)
            while ip == old_ip:
                try:
                    urllib.request.urlopen(
                        "https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=change-ip")
                    ip = urllib.request.urlopen("https://api.ipify.org").read().decode("utf-8")
                    print("waiting... ip is: ", ip)
                    time.sleep(4)
                except Exception as e:
                    print(e)

            urllib.request.urlopen(f"https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=new-ip:{ip}")
            print("new ip: ", ip)

    except Exception as e:
        print(e, artist_link)
        errors.append(artist_link)

browser.quit()

with open("/home/la/Desktop/bots/chords-bot/ultimate-guitar/all_songs.txt", "w+") as f:
    f.write(songs_links)
    f.close()

fpath = "/home/la/Desktop/bots/chords-bot/ultimate-guitar/all_songs_errors.txt"
if not os.exists(fpath):
    os.mknod(fpath)

with open(fpath, "w+") as f:
    f.write("\n".join(errors))
    f.close()
