import glob
import hashlib
import os
import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler)

this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])
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
                   "0", "x", chr(32), chr(160), "/", "sus", "maj", "+", "aj", chr(8207)]

levels = [["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
          ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]]

to_remove = {i: "" for i in chars_to_remove}
to_remove = dict((re.escape(k), v) for k, v in to_remove.items())
saved = {}
print("defined")


def convert_line(line, key):
    print("converting started")
    key = int(float(key) * 2)
    new_line = ""
    print(line)
    current_level = []

    # למצוא את האות הראשונה. לבדוק אם זו שאחריה היא מול או דיאז. אם כן לחבר את שניהם. רק אז לחפש ברשימה ולהחליף.
    for i in range(0, len(line)):
        if line[i] in levels[0]:
            try:

                if line[i + 1] == "#":
                    print("dies: ", line[i:i + 2])
                    current_level = levels[0]
                    temp = line[i:i + 2]
                elif line[i + 1] == "b":
                    print("mol: ", line[i:i + 2])
                    current_level = levels[1]
                    temp = line[i:i + 2]
                else:
                    temp = line[i]
                    current_level = levels[0]
                print("try _______________________________\n\n\n\n\n")
            except IndexError:
                temp = line[i]
                print("except _______________________________\n\n\n\n\n")

            if current_level.index(temp) + key > 11:
                print("old: ", temp)
                print("new: ", current_level[(current_level.index(temp) + key) % 12])
                new_line += current_level[(current_level.index(temp) + key) % 12]
            else:
                print("old: ", temp)
                print("new: ", current_level.index(temp) + key)
                new_line += current_level[current_level.index(temp) + key]
            continue

        elif line[i] != "#" and line[i] != "b":
            print("Regular", line[i])
            new_line += line[i]
    new_line = new_line.replace("B#", "C").replace("Cb", "B").replace("E#", "F").replace("Fb", "E").replace("b#",
                                                                                                            "").replace(
        "#b", "")
    print(new_line)
    return new_line


def new_key(data, key):
    print("converting started")
    new_data = []

    pattern = re.compile("|".join(to_remove.keys()))

    for i in data:

        if i == "":
            new_data.append(i)
            print(i)
            continue

        print("before: ", i)
        j = pattern.sub(lambda m: to_remove[re.escape(m.group(0))], i)

        if j:
            print("regular: ", i)
            new_data.append(i)
        else:
            print("chords: ", i)
            new_data.append(convert_line(i, key))

    print("new data: ", new_data)
    return new_data


def karaoke_start(update, context):
    print("sending")
    context.bot.sendVideo(chat_id=update.message.chat_id,
                          video='https://www.video-cdn.com/video/show/a677a8b4a518616b807fbc485fa2fe22/0be5160c18eec7373e67a2ca996698ed?type=mp4')


def main_karaoke():
    print("karaoke started")

    updater = Updater("1223729088:AAHmZyVGZd6hDDjYYfvhuSqk3yWpqk4S57U", use_context=True,
                      request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    start_handler = CommandHandler('start', karaoke_start)

    dp.add_handler(start_handler)
    # Start the Bot
    updater.start_polling()

    updater.idle()


def h1(w):
    return hashlib.md5(w).hexdigest()[:9]


def by_hash(user_hash, update):
    print("user hash " + str(user_hash))
    files = saved[user_hash]
    print("len files:   " + str(len(files)))


    build_message(files, update)


def build_message(files, update):
    print("building")
    print(update.message.chat_id)

    if len(files) == 0 and update.message.chat_id != -1001126502216:
        print("no results")
        update.message.reply_text("פאדיחה, לא מצאנו כלום.. נסה שילוב אחר!")
        return

    keyboard = []

    if update.message.chat_id == -1001126502216:
        if "אקורדים" in update.message.text:
            user_hash = h1(update.message.from_user.username.encode())
            print(str(user_hash) + "---------------------------------------------")
            saved[user_hash] = files
            print("saved")
            replay_markup = InlineKeyboardMarkup([[InlineKeyboardButton(

                text="לחץ פה",

                url="https://t.me/Tab4usBot?start={}".format(str(user_hash)))]])

            update.message.reply_text('אקורדים ל "{}"'.format(update.message.text.replace("אקורדים ", "")),
                                      reply_markup=replay_markup)

        return

    if len(files) > 1:
        print("few results")
        for i in files:
            keyboard.append(i[len(this_folder)+10:-4])
        keyboard.append("חזור")
        update.message.reply_text("בחר..",
                                  reply_markup=ReplyKeyboardMarkup([[i] for i in keyboard]),
                                  one_time_keyboard=True,
                                  selective=True)
        return

    fname = this_folder + "/message-intro.txt"
    with open(fname, "r") as f:
        introB = f.read()

    fname =  this_folder + "/message-end.txt"
    with open(fname, "r") as f:
        endB = f.read()

    fpath = files[0]
    print("one results")
    with open(fpath, "r") as f:

        data = f.read().split('\n')
        print("to convert..")

        print("converted")
        intro = introB
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + "   \n" + data[0])
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + "   \n" + data[1])
        intro = intro.replace("capo", data[3])
        data[3] = intro
        data.append(endB)
        send_data(data[3:], update, True)


def send_data(data, update, notificate):
    song = {0: ""}
    counter = 0

    for j in data:
        test = song[counter] + "%0A" + j + data[-1]
        if len(test) >= 4096:
            counter += 1
            song[counter] = ""
        song[counter] += "\n" + j

    keyboard = [[InlineKeyboardButton("+1", callback_data='+1'), InlineKeyboardButton("+0.5", callback_data='+0.5'),
                 InlineKeyboardButton("-0.5", callback_data='-0.5'),
                 InlineKeyboardButton("-1", callback_data='-1')],
                [InlineKeyboardButton("+2", callback_data='+2'), InlineKeyboardButton("+1.5", callback_data='+1.5'),
                 InlineKeyboardButton("-1.5", callback_data='-1.5'),
                 InlineKeyboardButton("-2", callback_data='-2')],
                [InlineKeyboardButton("+3", callback_data='+3'), InlineKeyboardButton("+2.5", callback_data='+2.5'),
                 InlineKeyboardButton("-2.5", callback_data='-2.5'),
                 InlineKeyboardButton("-3", callback_data='-3')]]
    reply_markup = ReplyKeyboardRemove()
    counter = 0

    for _ in song:
        if counter + 1 == len(song):
            reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(song[counter].replace(u'\xa0', u' '), reply_markup=reply_markup,
                                  disable_notification=notificate)
        counter += 1


def search_songs(update, context):
    print(update.message.text)
    data = update.message.text.replace("אקורדים ", "").replace("'", "")
    if data == "חזור":
        update.message.reply_text("חוזר..",
                                  reply_markup=ReplyKeyboardRemove(selective=True))
        return

    files = []
    data = data.title()
    for fpath in glob.glob(this_folder + "/uploaded/*"):
        cpath = fpath.replace("'", "")
        if data == cpath[len(this_folder)+10:-4]:
            files = [fpath]
            build_message(files, update)
            return
        if data in cpath:
            files.append(fpath)
    build_message(files, update)


def start(update, context):
    print(update.message.chat_id)
    if len(update.message.text[7:]) != 9:
        update.message.reply_text(
            "היי, ברוכים הבאים לרובוט האקורדים של ‏@tab4us - ISRACHORD.\nשילחו את השם המלא של השיר כדי לקבל אותו, או את של הלהקה לפתיחת רשימת השירים שלהם..\nלדיווח:\n@ADtmr")
        return
    print("_______" + update.message.text[7:] + "___________")
    print(len(update.message.text[7:]))
    by_hash(update.message.text[7:], update)


def button(update, context):
    query = update.callback_query
    print(update.callback_query)
    print(query.message.text)
    data = new_key(query.message.text.split('\n'), query.data)
    send_data(data, query, False)
    context.bot.delete_message(query.message.chat.id, query.message.message_id)

    # query.edit_message_text(text=song)


def main():
    print("/".join(os.path.realpath(__file__).split("/")[:-1]))
    updater = Updater("999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add message handler.
    start_handler = CommandHandler('start', start)
    key_button = CallbackQueryHandler(button)
    conv_handler = MessageHandler(Filters.text, search_songs)

    dp.add_handler(key_button)
    dp.add_handler(start_handler)
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print(len("/".join(os.path.realpath(__file__).split("/")[:-1]) + "/uploaded/*"))
    main()
