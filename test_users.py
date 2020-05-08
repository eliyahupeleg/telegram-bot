import os
import time

this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])
users = []
users_path = f'{this_folder}/users.txt'


def write_users():
    global users
    while True:
        print("now")
        with open(users_path, 'w+') as out:
            print("epened")
            out.write('\n'.join(users))
            print('\n'.join(users))
            out.close()
        users.append(input("input: \n"))
        print("sleep")
        time.sleep(5)


write_users()
