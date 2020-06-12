import os
import time

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')

# start chrome browser
browser = webdriver.Chrome(chrome_options=options, executable_path="/home/la/chromedriver")
this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])

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


with open("/home/la/Desktop/bots/chords-bot/ultimate-guitar/all_songs.txt", "r") as f:
    song_links = f.read().split("\n")

for song_link in song_links:
    browser.get(song_link)

    singer = browser.execute_script(js_get_singer)
    chords = browser.execute_script(js_get_song_chords)
    song = browser.execute_script(js_get_song_name)

    fpath = f'{this_folder}/toUpload/{singer} - {song}.txt'
    os.mknod(fpath)

    with open(fpath, "w+") as f:
        f.write('\n'.join([song, singer, "גולש", "", chords]))
        f.close()

    print("song wrote.")
    print(song_link)
    print(len(song_links), song_links.index(song_link))

browser.quit()

