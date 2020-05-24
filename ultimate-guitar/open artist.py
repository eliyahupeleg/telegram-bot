import subprocess
import time

with open("/home/la/Desktop/bots/chords-bot/ultimate-guitar/all.txt", "r") as f:
    data = f.read().split("\n")

for i in data:
    p = subprocess.Popen(["google-chrome", i])
    time.sleep(2)


