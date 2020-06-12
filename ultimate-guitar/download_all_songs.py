from requests import get
import os
import time
import urllib.request
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')

this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])

# start chrome browser
browser = webdriver.Chrome(chrome_options=options, executable_path="/home/la/chromedriver")
browser.set_page_load_timeout(99999999999999999999999999999)

js_get_song_name = '''
song_name = document.getElementsByClassName("_2Glbj")[0].firstElementChild.textContent.replaceAll(" chords", "");
return(song_name)
'''

js_get_singer = '''
singer = "";
names = Array.from(document.getElementsByClassName("_2RB8K")[0].lastElementChild.children);
for( var i of names){singer += i.textContent + " & "}
singer = singer.slice(0, -3);
return(singer)
'''

js_get_song_chords = '''
song = document.getElementsByClassName("_3zygO")[0].textContent.slice(0, -1);
return(song)
'''
all_songs_f = open(f"{this_folder}//all_songs.txt", "r+")
songs_links_f = open(f"{this_folder}//songs_links.txt", "r+")
songs_links = songs_links_f.read().split("\n")
downloaded_songs = []

counter = 0
while True:
    try:
        for new_song in songs_links:
            counter += 1
            while True:
                try:
                    browser.get(new_song)

                    singer = browser.execute_script(js_get_singer)
                    chords = browser.execute_script(js_get_song_chords)
                    song = browser.execute_script(js_get_song_name)

                    fpath = f'{this_folder}/toUpload/{singer} - {song}.txt'
                    os.mknod(fpath)

                    if browser.title == "":
                        urllib.request.urlopen(
                            f"https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=400-ip")
                        ip = get("https://api.ipify.org/").text
                        while get("https://api.ipify.org/").text == ip:
                            time.sleep(6)
                        browser.get(new_song)

                    with open(fpath, "w+") as f:
                        f.write('\n'.join([song, singer, "גולש", "", "", "", chords]))
                        f.close()

                    print("song link: ", new_song)
                    print("song name: ", song)
                    al = len(songs_links)
                    print(counter, "/", al)
                    print("%.3f" % (100 * (counter / al)), "%")
                    t0 = time.time()

                    if counter % 20 == 0:
                        songs = '\n'.join(map(str, downloaded_songs)) + '\n'
                        print(songs)
                        all_songs_f.write(songs)
                        songs_links = []
                        d = time.time() - t0
                        print("\n\n\n\n\n\n wrote in: %.3f s. \n\n\n" % d)

                    else:
                        downloaded_songs.append(new_song)
                    break
                except Exception as e:
                    print(e, new_song)
                    urllib.request.urlopen(
                        f"https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=error\n{e}")
                    print(e, '\n')

        browser.quit()

        fpath = f"{this_folder}/all_songs_errors.txt"
        if not os.exist(fpath):
            os.mknod(fpath)

        with open(fpath, "a") as f:
            f.write("\n".join(errors))
            f.close()
        break
    except Exception as e:
        print(e)
