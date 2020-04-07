import glob
import hashlib

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler)

saved = {}


def h1(w):
    return hashlib.md5(w).hexdigest()[:9]


def by_hash(user_hash, update):
    print("user hash " + str(user_hash))
    files = saved[user_hash]
    print("len files:   " + str(len(files)))
    '''for i in glob.glob("/home/la/Downloads/HtmlsaveToTxt/uploaded/*"):
        print(h1(i.encode()))
        if saved == h1(i.encode()):
            files.append(i)'''

    build_message(files, update)


def build_message(files, update):
    print("building")
    print(update.message.chat_id)
    if len(files) == 0 and update.message.chat_id != -1001206432389:
        update.message.reply_text("פאדיחה, לא מצאנו כלום.. נסה שילוב אחר!")
        return

    keyboard = []

    if update.message.chat_id == -1001206432389:
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
        for i in files:
            keyboard.append(i[35:-4])
        keyboard.append("חזור")
        update.message.reply_text("בחר..",
                                  reply_markup=ReplyKeyboardMarkup([[i] for i in keyboard]),
                                  one_time_keyboard=True,
                                  selective=True)
        return

    fname = "/home/elikopeleg/message-intro.txt"
    with open(fname, "r") as f:
        introB = f.read()

    fname = "/home/elikopeleg/message-end.txt"
    with open(fname, "r") as f:
        endB = f.read()

    print("open and end")
    fpath = files[0]
    with open(fpath, "r") as f:

        data = f.read().split('\n')
        intro = introB
        intro = intro.replace("song",
                              data[0].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ",", "_") + "   \n" + data[0])
        intro = intro.replace("singer",
                              data[1].replace(" ", "_").replace('/', "").replace('&', "").replace("'", "").replace(
                                  ".", "_").replace(",", "_") + "   \n" + data[1])
        intro = intro.replace("capo", data[3])
        song = {0: ""}
        counter = 0
        data[3] = intro
        data.append(endB)
        for j in data[3:]:
            test = song[counter] + "%0A" + j + endB
            if len(test) >= 4096:
                counter += 1
                song[counter] = ""
            song[counter] += "\n" + j

        counter = 0
        for i in song:
            update.message.reply_text(song[counter],
                                      reply_markup=ReplyKeyboardRemove())
            counter += 1


def search_songs(update, context):
    print(update.message.chat_id)
    data = update.message.text.replace("אקורדים ", "")
    if data == "חזור":
        update.message.reply_text("חוזר..",
                                  reply_markup=ReplyKeyboardRemove(selective=True))
        return

    files = []
    data = data.title()
    for fpath in glob.glob("/home/elikopeleg/uploaded/uploaded/*"):
        if data == fpath[35:-4]:
            files = [fpath]
            build_message(files, update)
            return
        if data in fpath:
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


def main():
    updater = Updater("999605455:AAEZ3wPt6QyAqdoDa1gtUJzcWVuOk4UfsZU", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add message handler.
    start_handler = CommandHandler('start', start)

    conv_handler = MessageHandler(Filters.text, search_songs)

    dp.add_handler(start_handler)
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
