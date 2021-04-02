import glob
import os

this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])
uploaded_path = this_folder + "/uploaded/"
uploaded_list = glob.glob(f"{uploaded_path}/*")

for path in uploaded_list:
    with open(path, "r+") as f:
        data = f.read().replace(chr(1460), "")
        f.seek(0)
        f.truncate()
        f.write(data)
