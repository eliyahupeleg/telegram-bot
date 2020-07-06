import collections
import io
import pickle
import operator
import glob
import hashlib
import json
import os
import re
import threading
import time
from random import randrange

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler)

# using server and local python- don't need to change the locations of the files all the time.
this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])
chords_library = ["A" , "A5" , "A6" , "A7" , "A9" , "A_Ab" , "A_B" , "A_Bb" , "A_C#" , "A_C" , "A_D" , "A_E" , "A_Eb" , "A_F#" , "A_F" , "A_G" , "Aadd9" , "Aaug" , "Ab" , "Ab5" , "Ab6" , "Ab7" , "Ab9" , "Ab_A" , "Ab_Bb" , "Ab_C#" , "Ab_C" , "Ab_Eb" , "Ab_F#" , "Ab_G" , "Abadd9" , "Abaug" , "Abdim" , "Abdim7" , "Abm" , "Abm7" , "Abm7b5" , "Abm9" , "Abmaj7" , "Absus4" , "Adim" , "Adim7" , "Am" , "Am7" , "Am7b5" , "Am9" , "Am_Ab" , "Am_B" , "Am_Bb" , "Am_C" , "Am_D" , "Am_E" , "Am_Eb" , "Am_F#" , "Am_F" , "Am_G" , "Amaj7" , "Ammaj7" , "Asus4" , "B" , "B5_" , "B6" , "B7" , "B9_2" , "B_A" , "B_Ab" , "Badd9" , "Baug" , "Bb" , "Bb5" , "Bb6" , "Bb7" , "Bb9" , "Bb9_2" , "Bb_A" , "Bb_Ab" , "Bb_B" , "Bb_Eb" , "Bbadd9" , "Bbaug" , "Bbdim" , "Bbdim7" , "Bbm" , "Bbm7" , "Bbm7b5" , "Bbm9" , "Bbmaj7" , "Bbsus4" , "Bdim" , "Bdim7" , "Bm" , "Bm7" , "Bm7b5" , "Bm9" , "Bm_A" , "Bm_Ab" , "Bm_Bb" , "Bm_C#" , "Bm_C" , "Bm_F#" , "Bmaj7" , "Bsus4" , "C#" , "C#5" , "C#6" , "C#7" , "C#9_2" , "C#add9" , "C#aug" , "C#dim" , "C#dim7" , "C#m" , "C#m7" , "C#m7b5" , "C#m9" , "C#maj7" , "C#mmaj7" , "C#sus4" , "C" , "C5" , "C6" , "C7" , "C9_2" , "C_A" , "C_B" , "C_Bb" , "C_C#" , "C_G" , "Cadd9" , "Caug" , "Cdim" , "Cdim7" , "Cm" , "Cm7" , "Cm7b5" , "Cm9" , "Cmaj7" , "Csus4" , "D" , "D5" , "D6" , "D7" , "D9" , "D_A" , "D_B" , "D_Bb" , "D_C#" , "D_C" , "D_F#" , "Dadd9" , "Daug" , "Ddim" , "Ddim7" , "Dm" , "Dm7" , "Dm7b5" , "Dm9" , "Dm_A" , "Dm_B" , "Dm_C" , "Dmaj7" , "Dsus4" , "E" , "E5" , "E6" , "E7" , "E9" , "E_A" , "E_Ab" , "E_B" , "E_Bb" , "E_C#" , "E_C" , "E_D" , "E_Eb" , "E_F#" , "E_F" , "E_G" , "Eadd9" , "Eaug" , "Eb" , "Eb5" , "Eb6" , "Eb7" , "Eb9" , "Eb9_2" , "Ebadd9" , "Ebaug" , "Ebdim" , "Ebdim7" , "Ebm" , "Ebm7" , "Ebm7b5" , "Ebm9" , "Ebmaj7" , "Ebsus4" , "Edim" , "Edim7" , "Em" , "Em7" , "Em7b5" , "Em9" , "Em_A" , "Em_Ab" , "Em_B" , "Em_Bb" , "Em_C#" , "Em_C" , "Em_D" , "Em_Eb" , "Em_F#" , "Em_F" , "Em_G" , "Emaj7" , "Esus4" , "F#" , "F#5" , "F#6" , "F#7" , "F#9" , "F#_Ab" , "F#_B" , "F#_Bb" , "F#_C#" , "F#_E" , "F#_F" , "F#_G" , "F#add9" , "F#aug" , "F#dim" , "F#dim7" , "F#m" , "F#m7" , "F#m7b5" , "F#m9" , "F#m_E" , "F#m_F" , "F#m_G" , "F#maj7" , "F#sus4" , "F" , "F5" , "F6" , "F7" , "F9_2" , "F_A" , "F_Bb" , "F_C" , "F_D" , "F_E" , "F_Eb" , "F_F#" , "F_G" , "Fadd9" , "Faug" , "Fdim" , "Fdim7" , "Fm" , "Fm7" , "Fm7b5" , "Fm9" , "Fm_Ab" , "Fm_D" , "Fm_E" , "Fm_Eb" , "Fm_F#" , "Fmaj7" , "Fsus4" , "G" , "G5" , "G6" , "G7" , "G9" , "G_C" , "G_D" , "G_E" , "G_F#" , "G_F" , "Gadd9" , "Gaug" , "Gdim" , "Gdim7" , "Gm" , "Gm7" , "Gm7b5" , "Gm9" , "Gm_Ab" , "Gm_D" , "Gm_E" , "Gm_F" , "Gmaj7" , "Gsus4"]
# using for the convert. one
levels = [["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
          ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]]

# all the chars that can be in chords line. using for recognise chords lines and convert them.
chars_to_remove = ["A#6add9", "Ab6add9", "A#add9", "A#dim7", "A#m7b5", "A#maj7", "A#maj9", "A#sus2", "A#sus4", "A6add9",
                   "Abadd9", "Abdim7", "Abm7b5", "Abmaj7", "Abmaj9", "Absus2", "Absus4", "A#7#5", "A#7b5", "A#7b9",
                   "A#aug",
                   "A#dim", "A#m11", "Aadd9", "Ab7#5", "Ab7b5", "Ab7b9", "Abaug", "Abdim", "Abm11", "Adim7", "Am7b5",
                   "Amaj7",
                   "Amaj9", "Asus2", "Asus4", "A#11", "A#13", "A#m6", "A#m7", "A#m9", "A7#5", "A7b5", "A7b9", "Aaug",
                   "Ab11",
                   "Ab13", "Abm6", "Abm7", "Abm9", "Adim", "Am11", "A#6", "A#7", "A#9", "A#m", "A11", "A13", "Ab6",
                   "Ab7", "Ab9",
                   "Abm", "Am6", "Am7", "Am9", "A#", "A6", "A7", "A9", "Ab", "Am", "A", "Bb6add9", "B6add9", "Bbadd9",
                   "Bbdim7",
                   "Bbm7b5", "Bbmaj7", "Bbmaj9", "Bbsus2", "Bbsus4", "Badd9", "Bb7#5", "Bb7b5", "Bb7b9", "Bbaug",
                   "Bbdim",
                   "Bbm11", "Bdim7", "Bm7b5", "Bmaj7", "Bmaj9", "Bsus2", "Bsus4", "B7#5", "B7b5", "B7b9", "Baug",
                   "Bb11", "Bb13",
                   "Bbm6", "Bbm7", "Bbm9", "Bdim", "Bm11", "B11", "B13", "Bb6", "Bb7", "Bb9", "Bbm", "Bm6", "Bm7",
                   "Bm9", "B6",
                   "B7", "B9", "Bb", "Bm", "B", "C#6add9", "C#add9", "C#dim7", "C#m7b5", "C#maj7", "C#maj9", "C#sus2",
                   "C#sus4",
                   "C6add9", "C#7#5", "C#7b5", "C#7b9", "C#aug", "C#dim", "C#m11", "Cadd9", "Cdim7", "Cm7b5", "Cmaj7",
                   "Cmaj9",
                   "Csus2", "Csus4", "C#11", "C#13", "C#m6", "C#m7", "C#m9", "C7#5", "C7b5", "C7b9", "Caug", "Cdim",
                   "Cm11",
                   "C#6", "C#7", "C#9", "C#m", "C11", "C13", "Cm6", "Cm7", "Cm9", "C#", "C6", "C7", "C9", "Cm", "C",
                   "C",
                   "D#6add9", "Db6add9", "D#add9", "D#dim7", "D#m7b5", "D#maj7", "D#maj9", "D#sus2", "D#sus4", "D6add9",
                   "Dbadd9", "Dbdim7", "Dbm7b5", "Dbmaj7", "Dbmaj9", "Dbsus2", "Dbsus4", "D#7#5", "D#7b5", "D#7b9",
                   "D#aug",
                   "D#dim", "D#m11", "Dadd9", "Db7#5", "Db7b5", "Db7b9", "Dbaug", "Dbdim", "Dbm11", "Ddim7", "Dm7b5",
                   "Dmaj7",
                   "Dmaj9", "Dsus2", "Dsus4", "D#11", "D#13", "D#m6", "D#m7", "D#m9", "D7#5", "D7b5", "D7b9", "Daug",
                   "Db11",
                   "Db13", "Dbm6", "Dbm7", "Dbm9", "Ddim", "Dm11", "D#6", "D#7", "D#9", "D#m", "D11", "D13", "Db6",
                   "Db7", "Db9",
                   "Dbm", "Dm6", "Dm7", "Dm9", "D#", "D6", "D7", "D9", "Db", "Dm", "D", "Eb6add9", "E6add9", "Ebadd9",
                   "Ebdim7",
                   "Ebm7b5", "Ebmaj7", "Ebmaj9", "Ebsus2", "Ebsus4", "Eadd9", "Eb7#5", "Eb7b5", "Eb7b9", "Ebaug",
                   "Ebdim",
                   "Ebm11", "Edim7", "Em7b5", "Emaj7", "Emaj9", "Esus2", "Esus4", "E7#5", "E7b5", "E7b9", "Eaug",
                   "Eb11", "Eb13",
                   "Ebm6", "Ebm7", "Ebm9", "Edim", "Em11", "E11", "E13", "Eb6", "Eb7", "Eb9", "Ebm", "Em6", "Em7",
                   "Em9", "E6",
                   "E7", "E9", "Eb", "Em", "E", "F#6add9", "F#add9", "F#dim7", "F#m7b5", "F#maj7", "F#maj9", "F#sus2",
                   "F#sus4",
                   "F6add9", "F#7#5", "F#7b5", "F#7b9", "F#aug", "F#dim", "F#m11", "Fadd9", "Fdim7", "Fm7b5", "Fmaj7",
                   "Fmaj9",
                   "Fsus2", "Fsus4", "F#11", "F#13", "F#m6", "F#m7", "F#m9", "F7#5", "F7b5", "F7b9", "Faug", "Fdim",
                   "Fm11",
                   "F#6", "F#7", "F#9", "F#m", "F11", "F13", "Fm6", "Fm7", "Fm9", "F#", "F6", "F7", "F9", "Fm", "F",
                   "G#6add9",
                   "Gb6add9", "G#add9", "G#dim7", "G#m7b5", "G#maj7", "G#maj9", "G#sus2", "G#sus4", "G6add9", "Gbadd9",
                   "Gbdim7",
                   "Gbm7b5", "Gbmaj7", "Gbmaj9", "Gbsus2", "Gbsus4", "G#7#5", "G#7b5", "G#7b9", "G#aug", "G#dim",
                   "G#m11",
                   "Gadd9", "Gb7#5", "Gb7b5", "Gb7b9", "Gbaug", "Gbdim", "Gbm11", "Gdim7", "Gm7b5", "Gmaj7", "Gmaj9",
                   "Gsus2",
                   "Gsus4", "G#11", "G#13", "G#m6", "G#m7", "G#m9", "G7#5", "G7b5", "G7b9", "Gaug", "Gb11", "Gb13",
                   "Gbm6",
                   "Gbm7", "Gbm9", "Gdim", "Gm11", "G#6", "G#7", "G#9", "G#m", "G11", "G13", "Gb6", "Gb7", "Gb9", "Gbm",
                   "Gm6",
                   "Gm7", "Gm9", "G#", "G6", "G7", "G9", "Gb", "Gm", "G", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                   "0", "x", chr(32), chr(160), "/", "sus", "maj", "+", "aj", chr(8207), "#"]
to_remove = {i: "" for i in chars_to_remove}
to_remove = dict((re.escape(k), v) for k, v in to_remove.items())
to_remove_lambda = lambda m: to_remove[re.escape(m.group(0))]
users = []
old_users = []

# saved: the saved messages, for users that came form the group.
saved = {}
# flags- is the link in the group used?
flags = {}
# the group messages ids- request and response. cleaning the group from spam.
to_delete = {}
# flag. when the language is hebrew, when converting message needed to move the "#" to the start of the line.
HEBREW = False

uploaded_path = this_folder + "/uploaded/"
users_path = f'{this_folder}/users.txt'

fname = f"{this_folder}/message-intro.txt"
with open(fname, "r") as f:
    introB = f.read()

fname = f"{this_folder}/message-end.txt"
with open(fname, "r") as f:
    endB = f.read()

# optimized. conclusions only once.
len_uploaded_path = len(uploaded_path)

uploaded_list = glob.glob(f"{uploaded_path}/*")

songs_list = []
artists_list = []

# one option keyboard, send me random song.

random_keyboard = ReplyKeyboardMarkup([["שיר אקראי"]])

# the "convert" keyboard that sends with every song that the bot sent.
default_keyboard = [[InlineKeyboardButton("+", callback_data="+"), InlineKeyboardButton("-", callback_data="-")]]

# the "convert" keyboard that sends when the "-" button pressed in the default_keyboard.
keyboard_minus = [[InlineKeyboardButton("-1", callback_data='-1'),
                   InlineKeyboardButton("-2", callback_data='-2'),
                   InlineKeyboardButton("-3", callback_data='-3')]]

# the "convert" keyboard that sends when the "+" button pressed in the default_keyboard.
keyboard_plus = [[InlineKeyboardButton("+1", callback_data='+1'),
                  InlineKeyboardButton("+2", callback_data='+2'),
                  InlineKeyboardButton("+3", callback_data='+3')]]

# the "convert" keyboard that sends when the key converted by round number (1, 2, 3, -3, -2, -1)
keyboard_half = [[InlineKeyboardButton("+0.5", callback_data='+0.5'),
                  InlineKeyboardButton("-0.5", callback_data='-0.5')]]

statistics_path = f'{this_folder}/statistics.pkl'

try:
    if os.path.getsize(statistics_path) == 0 or not os.path.exists(statistics_path):
        with open(statistics_path, 'wb') as fp:
            pickle.dump({}, fp, protocol=pickle.HIGHEST_PROTOCOL)
            statistics = collections.OrderedDict()
    else:
        with open(statistics_path, 'rb') as fp:
            statistics = pickle.load(fp)
except FileNotFoundError:
    with open(statistics_path, 'wb') as fp:
        pickle.dump({}, fp, protocol=pickle.HIGHEST_PROTOCOL)
        statistics = collections.OrderedDict()


# if the name of the song or the artist is not UPPER, that mean that it should be in the format title().
# using function for optimized for loop to map function.
def get_song(song):
    try:
        return replace_to_filename(song).split(" - ")[1]
    except IndexError:
        print("index error", song)
    return


def get_artist(name):
    return replace_to_filename(name).split(" - ")[0]


def is_upper(i):
    if i.isupper():
        return i
    else:
        return i.title()


# used when there are few results. getting the file path, and returning the "artist - song" name.
def replace_to_filename(i):
    return i[len_uploaded_path:-4]


# True if all the chars in the str are hebrew. else False.
def is_hebrew(s):
    return any("\u0590" <= c <= "\u05EA" for c in s)


def write_users():
    with open(users_path, 'w+') as out:
        out.write('\n'.join(users))
        out.close()
        print("new user wrote")


# deleting the messages in the group by the "time_hash".
def delete(context, time_hash):
    print("deleting")

    # only after 40 seconds. users do not want to lose their links in one unsuccessfully presse.
    time.sleep(40)

    # if the link used, delete the messages.
    while True:
        if flags[time_hash]:
            break
    context.bot.delete_message(-1001126502216, to_delete[time_hash][0])
    context.bot.delete_message(-1001126502216, to_delete[time_hash][0] + 1)


# converting chords line up or down by the key. the key if from 3 to -3' in steps of 0.5.
def convert_line(line, key):
    key = int(float(key) * 2)
    new_line = ""
    len_line = len(line)
    # the real start of the line
    first_index = -1
    # למצוא את האות הראשונה. לבדוק אם זו שאחריה היא מול או דיאז. אם כן לחבר את שניהם. רק אז לחפש ברשימה ולהחליף.
    # connecting "#" and "b" to the chord, and then replacing.
    for i in range(0, len_line):
        line_i = line[i]

        if line_i in levels[0]:
            if first_index == -1:
                first_index = i

            try:

                if line[i + 1] == "#":
                    current_level = levels[0]
                    temp = line[i:i + 2]

                elif line[i + 1] == "b":
                    current_level = levels[1]
                    temp = line[i:i + 2]

                else:
                    temp = line_i
                    current_level = levels[0]

            # if this is the last char in the line, there is no "b" or "#"
            except IndexError:
                current_level = levels[0]
                temp = line_i

            # back to the start if got the end of the chords (Ab or G#)
            if current_level.index(temp) + key > 11:
                new_line += current_level[(current_level.index(temp) + key) % 12]
            else:
                new_line += current_level[current_level.index(temp) + key]
            continue

        # the "#" and the "b" chars already used with their chords.
        elif line[i] != "#" and line[i] != "b":
            new_line += line_i

    # moving the dies to the start of the line in hebrew. the # jumping to the other side because of RLM and LRM
    # checking every "if" only once, fastest.
    if HEBREW:

        # more than one chord in the line.
        if len(list(filter(None, new_line.split(' ')))) != 1:
            # in hebrew, if the dies in the end of the line, should move it to the start.
            if new_line[- 1] == "#":

                # if in the last convert the "#" already moved, needs only to delete the "#" in the end.
                # impossible to have "#" in the start of the chord line.
                if new_line[first_index] == "#":
                    new_line = new_line[:-1]
                else:
                    # put the "#" in the start of the line, right after the spaces.
                    new_line = f"{new_line[:first_index]}#{new_line[first_index:-1]}"
            elif new_line[first_index] == "#":

                new_line = new_line[:-1]

    return new_line


def new_key(data, key):
    new_data = []
    global HEBREW
    pattern = re.compile("|".join(to_remove.keys()))
    HEBREW = is_hebrew(data[5])
    for i in data:

        if i == "":
            new_data.append(i)
            continue

        j = pattern.sub(to_remove_lambda, i)

        if j:
            new_data.append(i)
        else:
            new_data.append(convert_line(i, key))
    return new_data


def h1(w):
    return hashlib.md5(w).hexdigest()[:9]


def by_hash(time_hash, context, update):
    files = saved[time_hash]

    build_message(files, context, update)


def build_message(files, context, update):
    print(len(files), "results\n")
    len_files = len(files)
    if update.message.chat_id == -1001126502216 and len_files > 0:

        if "אקורדים" in update.message.text:
            time_hash = h1(str(time.time()).encode())
            saved[time_hash] = files
            replay_markup = InlineKeyboardMarkup([[InlineKeyboardButton(

                text="לחץ פה",

                url="https://t.me/Tab4usBot?start={}".format(str(time_hash)))]])

            data = update.message.text.replace("?", "")
            data = data.replace("לשיר ", "ל")
            data = data[data.index(" ל") + 2:]
            to_delete[time_hash] = [int(update.message.message_id)]
            update.message.reply_text('אקורדים ל "{}"'.format(data.replace("אקורדים ", "")), reply_markup=replay_markup)

            flags[time_hash] = False
            threading.Thread(target=delete, args=(context, time_hash)).start()
        return

    if len_files == 0:
        if update.message.chat_id == -1001126502216:
            return
        update.message.reply_text("פאדיחה, לא מצאנו כלום.. נסה שילוב אחר!", reply_markup=ReplyKeyboardRemove())
        return

    if len_files > 1:

        keyboard = sorted(list(map(replace_to_filename, files)))

        text = "בחר.."
        if len(files) > 179:
            keyboard = keyboard[:179]
            text = "החיפוש שלך כולל יותר מידי תוצאות, אז צמצמנו ל180 הראשונים.."
        keyboard.append("חזור")
        update.message.reply_text(text,
                                  reply_markup=ReplyKeyboardMarkup([[i] for i in keyboard]), resize_keyboard=True,
                                  one_time_keyboard=True,
                                  selective=True)
        return

    print("sending song..\n\n", files)
    fpath = files[0]
    with open(fpath, "r") as f:

        data = f.read().split('\n')
        intro = introB
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + f"   \n{data[0]}")
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + f"   \n{data[1]}")
        intro = intro.replace("capo", data[3])
        data[3] = intro
        data.append(endB)
        print("send data...")
        send_data(data[3:], update, True, context)


def send_data(data, update, notificate, context, keyboard=InlineKeyboardMarkup(default_keyboard)):
    song = {0: ""}
    counter = 0

    for j in data:
        test = f"{song[counter]}%0A{j}{data[-1]}"
        if len(test) >= 4096:
            counter += 1
            song[counter] = ""
        song[counter] += f"\n{j}"

    update.message.reply_text(text="Wait..", reply_markup=random_keyboard, resize_keyboard=True)
    context.bot.delete_message(update.message.chat_id, update.message.message_id + 1)

    reply_markup = ReplyKeyboardRemove()
    counter = 0

    for _ in song:
        if counter + 1 == len(song):
            reply_markup = keyboard

        if update.message.chat_id == -1001126502216:
            reply_markup = ReplyKeyboardRemove()

        update.message.reply_text(song[counter].replace(u'\xa0', u' '), reply_markup=reply_markup,
                                  disable_notification=notificate)
        counter += 1

    update.message.reply_text(u'\u202B', reply_markup=random_keyboard, disable_notification=notificate, resize_keyboard=True)
    context.bot.delete_message(update.message.chat_id, update.message.message_id + len(song) - 2)


def message_handler(update, context):

    global statistics
    message = update.message.text.replace("/", "_").replace("\\", "_").replace("A#", "Bb") \
        .replace("Db", "C#").replace("D#", "Eb").replace("Gb", "F#").replace("G#", "Ab")

    chat_id = update.message.chat_id
    if str(update.message.from_user.id) not in users:
        users.append(str(update.message.from_user.id))
        write_users()

    if chat_id == -1001126502216:
        if "אקורד " in message:
            message = message.replace("אקורד ", "")
        else:
            if "אקורדים" in message:
                search_songs(update, context)
                return
            else:
                return

    # reporting the statistics to ADtmr by telegram message.
    if message.title() == "St" and chat_id == 386848836:

        # Ordered Dicd cause the sorted returns a list and not a dict.
        statistics = collections.OrderedDict(sorted(statistics.items(), key=lambda kv: kv[1]))

        # file= because the "print" printing well, but the "send" adding \n between the chars.
        strStream = io.StringIO()
        print(statistics, file=strStream)

        # not sending by "send_data" cause it is only text.
        update.message.reply_text(strStream.getvalue().replace("OrderedDict([", "").replace("])", "").replace("), (", ")\n ("))
        return

    # sending random song.
    if message == "שיר אקראי":
        send_random(update, context)
        return

    # sending full list of what the bot have.
    if "מה יש" in message:
        send_data(songs_list + artists_list, update, True, context)
        return

    if "רשימת שירים" in message:
        result = list(filter(lambda x: x.startswith(message.replace("רשימת שירים ", "")), songs_list))
        if not result:
            result = "פאדיחה, לא מצאנו כלום.. נסה שילוב אחר!"
        send_data(result, update, True, context)
        return

    if "רשימת אמנים" in message:
        result = list(filter(lambda x: x.startswith(message.replace("רשימת אמנים ", "")), songs_list))
        if not result:
            result = "פאדיחה, לא מצאנו כלום.. נסה שילוב אחר!"
        send_data(result, update, True, context)
        return

    chord = message.replace("_", "_ ").replace("#", "# P").title().replace("_ ", "_").replace("# P", "#")
    if chord in chords_library:
        # לתקן את הקריאה חוזרת להמרת אקורד ושליחת תמונה חדשה
        context.bot.send_photo(heigth=10, caption=message.replace("_", "/"),
                               chat_id=chat_id,
                               photo=open(f'{this_folder}/chords/{chord}.png', 'rb'), reply_markup=random_keyboard)
        print("chord pic sent")
        return
    else:
        search_songs(update, context)


def search_songs(update, context):

    data = update.message.text
    print(data)
    try:
        print(type(statistics))
        statistics[data] += 1

    except KeyError:
        statistics[data] = 1

    finally:
        with open(statistics_path, 'wb') as fp:
            pickle.dump(statistics, fp)

    print(update.message.chat_id)
    print(data)
    if update.message.chat_id == -1001126502216:
        data = data.replace("?", "")
        data = data.replace("לשיר ", "ל")
        data = data[data.index(" ל") + 2:]
    if data == "חזור":
        print("חזור")
        update.message.reply_text("חוזר..",
                                  reply_markup=random_keyboard, resize_keyboard=True,
                                  one_time_keyboard=True,
                                  selective=True)
        return

    files = []
    spilt = data.split(' - ')

    # if the singer name is UPPER
    tmp = list(map(is_upper, spilt))
    data = " - ".join(tmp)

    folder = f'{this_folder}/uploaded/*'
    try:
        data = data.replace(data[data.index("'"):data.index("'") + 2],
                            data[data.index("'"):data.index("'") + 2].lower())
    except ValueError:
        pass
    finally:
        pass

    glb = uploaded_list

    full_name = f"{folder[:-1]}{data}.txt"

    if full_name in glb:
        files = [glb[glb.index(full_name)]]
        build_message(files, context, update)
        return

    for fpath in glb:
        if data in fpath:
            files.append(fpath)

    print("done search")
    build_message(files, context, update)


def start(update, context):
    print("start")
    print(update.message.chat_id)
    if str(update.message.from_user.id) not in users:
        users.append(str(update.message.from_user.id))
        write_users()
        print(users)

    if len(update.message.text[7:]) != 9:
        update.message.reply_text(
            " היי, ברוכים הבאים לרובוט האקורדים של 🎶‏ISRACHORD🎶.\nשילחו שם  של שיר או אמן, וקבלו את האקורדים. כן, כזה פשוט..\nשלחו שם של אקורד (למשל A#m) כדי לקבל איצבוע לגיטרה..\n\nלדיווח:\n@ADtmr",
            reply_markup=random_keyboard, resize_keyboard=True,
            one_time_keyboard=True,
            selective=True)
        return
    time_hash = update.message.text[7:]
    flags[time_hash] = True
    by_hash(time_hash, context, update)


def send_random(update, context):
    song_name = uploaded_list[randrange(len(uploaded_list))]
    build_message([song_name], context, update)


def button(update, context):
    query = update.callback_query
    clicked = query.data
    print(clicked)

    if clicked == "+":
        print("+")
        context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                              message_id=update.callback_query.message.message_id,
                                              reply_markup=InlineKeyboardMarkup(keyboard_plus))
        return
    elif clicked == "-":
        print("-")
        context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                              message_id=update.callback_query.message.message_id,
                                              reply_markup=InlineKeyboardMarkup(keyboard_minus))
        return

    data = new_key(query.message.text.split('\n'), clicked)

    if clicked[1:] != "0.5":
        reply_keyboard = InlineKeyboardMarkup(keyboard_half)
        send_data(data, query, False, context, reply_keyboard)
        context.bot.delete_message(query.message.chat.id, query.message.message_id)
        return

    send_data(data, query, False, context)
    context.bot.delete_message(query.message.chat.id, query.message.message_id)
    # query.edit_message_text(text=song)


def main():
    global songs_list
    global artists_list
    global users

    songs_list = list(dict.fromkeys(list(map(get_song, uploaded_list))))
    artists_list = list(dict.fromkeys(list(map(get_artist, uploaded_list))))

    artists_list.sort()
    songs_list.sort()

    with open(users_path, 'r') as f:
        users = f.read().split('\n')

    updater = Updater("999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add message handler.
    start_handler = CommandHandler('start', start)
    key_button = CallbackQueryHandler(button)
    conv_handler = MessageHandler(Filters.text, message_handler)

    dp.add_handler(key_button)
    dp.add_handler(start_handler)
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
