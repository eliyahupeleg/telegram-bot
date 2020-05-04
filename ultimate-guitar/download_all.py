import os
import time

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')

# start chrome browser
browser = webdriver.Chrome(chrome_options=options, executable_path="/home/la/chromedriver")

js = r'''artists = document.getElementsByClassName('_2hJom');
var links = "";
for ( var a of artists){
    links += a.children[0].children[0].children[0].href + "\n"
}
return links'''
songs_links = ""

with open("/home/la/Desktop/bots/chords-bot/ultimate-guitar/all_artists.txt", "r") as f:
    artist_links = f.read().split("\n")

for artist_link in artist_links:
    browser.get(artist_link)
    songs_links += browser.execute_script(js)
    print("artist finished")
    print(songs_links)

browser.quit()

with open("/home/la/Desktop/bots/chords-bot/ultimate-guitar/all_songs.txt", "w+") as f:
    f.write(songs_links)
    f.close()