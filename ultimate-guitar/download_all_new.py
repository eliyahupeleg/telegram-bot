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
js_save_links = r'''artists = document.getElementsByClassName('_2hJom');
var links = "";
for ( var a of artists){
	links += a.children[0].children[0].children[0].href + "\n"
}
return links'''
js_check_next = '''if(document.getElementsByClassName("_2kTPR _1nJLO _3sEsO _2KJtL _1ofov kWOod").length > 0) return(document.getElementsByClassName("_2kTPR _1nJLO _3sEsO _2KJtL _1ofov kWOod")[0].href)'''


songs_f = open(f"{this_folder}//all_songs.txt", "r+")
songs_links = songs_f.read().split("\n")
new_songs = []
errors = []

with open(f"{this_folder}//all_artists.txt", "r") as f:
	artist_links = f.read().split("\n")
	f.close()

with open(f"{this_folder}//last.txt", "r") as f:
	read = f.read()
	if read:
		start = int(read)
	else:
		start = 0
	print(type(start))
	f.close()

counter = 0
while True:
	try:
		for artist_link in artist_links:
			counter += 1
			while True:
				try:
					if counter < start:
						if counter % 10 != 0:
							break
						elif counter + 10 < start:		
							break
						start = counter
						print("starting in ", counter)


					browser.get(artist_link)

					next_page = browser.execute_script(js_check_next)			

					if browser.title == "":
						urllib.request.urlopen(f"https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=400-ip")
						ip = get("https://api.ipify.org/").text
						while get("https://api.ipify.org/").text == ip:
							time.sleep(6)
						browser.get(artist_link)
						new = browser.execute_script(js_save_links)
						next_page = browser.execute_script(js_check_next)


					new = browser.execute_script(js_save_links)[:-1].split('\n')
					for song in new:
						if song not in songs_links and song != '':
							new_songs.append(song)
						
					
					if next_page:
						if next_page not in artist_links:
							artist_links.append(next_page)				
							with open(f"{this_folder}//all_artists.txt", "a") as f:
								f.write('\n' + next_page)
								f.close()
							print("next: ", next_page)

					print("artist: ", artist_link)
					print("num of new: \n", len(new))
					al = len(artist_links)
					print(counter, "/", al)
					print("%.3f" %(100*(counter/al)), "%")
					t0 = time.time()

					if counter % 20 == 0:
						songs = '\n'.join(map(str, new_songs)) + '\n'
						print(songs)
						songs_f.write(songs)
						new_songs = []
						d = time.time() - t0
						print ("\n\n\n\n\n\nwrote in: %.3f s. \n\n\n" % d)
					with open(f"{this_folder}//last.txt", "w") as f:
						f.write(str(counter))
						f.close()
					break
				except Exception as e:
					print(e, artist_link)
					errors.append(artist_link)
					urllib.request.urlopen(f"https://api.telegram.org/bot999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU/sendMessage?chat_id=386848836&text=error")			
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
