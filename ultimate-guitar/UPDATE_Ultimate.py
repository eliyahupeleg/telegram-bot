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

basic_url = "https://www.ultimate-guitar.com/explore?order=date_desc&&live[]=0&page="

js_save_links = r'''artists = document.getElementsByClassName('_2hJom');
var links = "";
for ( var a of artists){
	links += a.children[0].children[0].children[0].href + "\n"
}
return links'''



songs_f = open(f"{this_folder}/all_songs.txt", "r+")
new_songs_f = open(f"{this_folder}/new_songs.txt", "r+")

# if songs downloade but not uploaded, it'll be in "new songs", but not in "all_songs"
songs_links = songs_f.read().split("\n") + new_songs_f.read().split("\n")
songs_f.close()

for i in range(1, 21):
	try:
		print("page number ", i)
		link = basic_url + str(i)
		browser.get(link)

		#check if exist
		
		if browser.title == "":
			urllib.request.urlopen(f"https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=change-ip-update-ultimate")

			ip = get("https://api.ipify.org/").text
			while get("https://api.ipify.org/").text == ip:
				time.sleep(6)

			browser.get(artist_link)

			

		# get links
		new = browser.execute_script(js_save_links)[:-1].split('\n')

		new_afetr = []

		for song_link in new:

			# living only the new songs in "new" list
			if song_link not in songs_links:
				new_afetr.append(song_link)
				print("\n\n\n\n\n\n\n\n\n\n\n added to list\n\n\n", song_link)

		print("\n\n", len(new_afetr), " new songs\n\n")
		print(i, " / 20")
		print(100*(i/20), "%")
		if len(new_afetr) == 0:
			continue
		t0 = time.time()

		# addingd the new songs links to new_songs file.
		# when uploading, will be added to "all_songs"
		songs = '\n'.join(map(str, new_afetr)) + '\n'

		with open(f"{this_folder}//new_songs.txt", "a") as f:
			f.write(songs)
			f.close()

		d = time.time() - t0
		print ("\n\n\n\n\n\n\n\nwrote in: %.3f s. \n\n\n\n\n" % d)
		
	except Exception as e:
		print(e, artist_link)
		errors.append(artist_link)
		urllib.request.urlopen(f"https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=error-update-ultimate")			
		input("error. continue?\n")

	
browser.quit()
new_songs_f.close()
songs_f.close()
#download all - import download_song_ultimate
input()
